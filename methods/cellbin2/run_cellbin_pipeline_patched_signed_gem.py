```python
#!/usr/bin/env python3
"""
Patched CellBin2 runner used in this project.

This script wraps the original CellBin2 pipeline and applies several
compatibility patches for the datasets used in this analysis, including:

1. GEM files without OffsetX / OffsetY header lines.
2. GEM count columns stored as floating-point values.
3. Safer visual GEF generation bin sizes.
4. Legacy adjusted mask naming compatibility.
5. Fallback when matrix feature detection fails.
6. Fallback when registration returns None.

These changes were made to improve workflow robustness for this project.
They do not modify the core CellBin2 segmentation model.
"""

import argparse
import gzip
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

from cellbin2 import cellbin_pipeline as cbp
from cellbin2.matrix import matrix as matrix_mod
from cellbin2.modules.extract import register as register_mod
from cellbin2.modules import scheduler as scheduler_mod
from cellbin2.modules.extract import matrix_extract as matrix_extract_mod
from cellbin2.utils.common import KIT_VERSIONS, KIT_VERSIONS_R, TechType, bPlaceHolder


# Avoid large bin sizes that caused runtime crashes during visual GEF generation.
SAFE_VIS_GEF_BIN_SIZES = [1, 10, 20, 50, 100, 200]


def _patched_read(self, file_path: Path, chunk_size=1024 * 1024 * 5):
    suffix = file_path.suffix
    assert suffix in [".gz", ".gef", ".gem"]

    if suffix == ".gef":
        self.binx, self.x_start, self.y_start, self._gene_mat = self._load_gef(self, file_path)
        return

    opener = gzip.open if suffix == ".gz" else open
    header_lines = []
    title_line = ""

    with opener(str(file_path), "rt", encoding="utf-8", errors="strict") as fh:
        for line in fh:
            if not line.startswith("#"):
                title_line = line.rstrip("\n")
                break
            header_lines.append(line.rstrip("\n"))

    if not title_line:
        raise ValueError(f"Failed to locate GEM title line in {file_path}")

    title = title_line.split("\t")

    count_candidates = [i for i in title if "ount" in i]
    if not count_candidates:
        raise ValueError(f"No count column found in GEM title line: {title_line}")

    umi_count_name = count_candidates[0]
    usecols = ["x", "y", umi_count_name]

    max_val = 0
    min_x = None
    min_y = None
    max_x = None
    max_y = None

    # Some GEM files store MIDCount as values like 1.0.
    # Read as float first and round before accumulation.
    count_dtype = np.float64

    for chunk in pd.read_csv(
        file_path,
        sep="\t",
        comment="#",
        usecols=usecols,
        dtype={"x": np.int32, "y": np.int32, umi_count_name: count_dtype},
        chunksize=chunk_size,
    ):
        chunk_max = int(np.ceil(float(chunk[umi_count_name].max())))
        if chunk_max > max_val:
            max_val = chunk_max

        chunk_min_x = int(chunk["x"].min())
        chunk_min_y = int(chunk["y"].min())
        chunk_max_x = int(chunk["x"].max())
        chunk_max_y = int(chunk["y"].max())

        min_x = chunk_min_x if min_x is None else min(min_x, chunk_min_x)
        min_y = chunk_min_y if min_y is None else min(min_y, chunk_min_y)
        max_x = chunk_max_x if max_x is None else max(max_x, chunk_max_x)
        max_y = chunk_max_y if max_y is None else max(max_y, chunk_max_y)

    if min_x is None or min_y is None or max_x is None or max_y is None:
        raise ValueError(f"No matrix rows found in {file_path}")

    if max_val <= 255:
        _dtype = np.uint8
        _max_val = 255
    elif max_val <= 65535:
        _dtype = np.uint16
        _max_val = 65535
    else:
        _dtype = np.uint32
        _max_val = 4294967295

    # Some GEM files do not contain OffsetX / OffsetY headers.
    # Default to 0 when the headers are missing.
    self.h_x_start = 0
    self.h_y_start = 0

    for line in header_lines:
        if line.startswith("#OffsetX="):
            self.h_x_start = int(line.split("=", 1)[1])
        elif line.startswith("#OffsetY="):
            self.h_y_start = int(line.split("=", 1)[1])

    import re

    header = "\n".join(header_lines)
    m_bin = re.search(r"(?im)^#.*\b(?:bin(?:size|_size|x)?)[\s:=]*([0-9]+)", header)

    if m_bin:
        self.binx = int(m_bin.group(1))
    else:
        self.binx = 1

    self.binx = 1 if self.binx == 0 else self.binx

    self.x_start = min_x
    self.y_start = min_y

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    img = np.zeros((height, width), dtype=_dtype)

    for chunk in pd.read_csv(
        file_path,
        sep="\t",
        comment="#",
        usecols=usecols,
        dtype={"x": np.int32, "y": np.int32, umi_count_name: count_dtype},
        chunksize=chunk_size,
    ):
        chunk = (
            chunk.groupby(["x", "y"], as_index=False)
            .agg(UMI_sum=(umi_count_name, "sum"))
        )

        ys = chunk["y"].to_numpy(dtype=np.int64) - min_y
        xs = chunk["x"].to_numpy(dtype=np.int64) - min_x
        vals = np.rint(chunk["UMI_sum"].to_numpy(dtype=np.float64)).astype(np.uint64)

        current = img[ys, xs].astype(np.uint64, copy=False)
        summed = current + vals
        np.minimum(summed, _max_val, out=summed)
        img[ys, xs] = summed.astype(_dtype, copy=False)

    self._gene_mat = img


_ORIGINAL_RUN_REGISTER = register_mod.run_register


def _is_readable_h5(path: Path) -> bool:
    if not path.exists():
        return False

    try:
        import h5py

        with h5py.File(path, "r"):
            return True
    except Exception:
        return False


def _patched_generate_vis_gef(src_path: str, dst_path: str):
    from gefpy.bgef_writer_cy import generate_bgef

    dst = Path(dst_path)

    if dst.exists():
        dst.unlink()

    generate_bgef(
        input_file=src_path,
        bgef_file=dst_path,
        stromics="geneExp",
        n_thread=1,
        bin_sizes=SAFE_VIS_GEF_BIN_SIZES,
    )


def _patched_save_tissue_bin_data(src_path: str, dst_path: str, tissue_mask: str, bin_siz: int = 1):
    src_path = str(src_path)
    dst_path = str(dst_path)
    tissue_mask = str(tissue_mask)

    if src_path.endswith(".gef"):
        tissue_mask = matrix_mod.adjust_mask_shape(gef_path=src_path, mask_path=tissue_mask)

    path_no_ext, ext = os.path.splitext(dst_path)
    tmp_path = Path(f"{path_no_ext}_tmp{ext}")

    if not _is_readable_h5(tmp_path):
        from gefpy.bgef_creater_cy import BgefCreater

        register_mod.clog.info(f"Creating temporary tissue GEF: {tmp_path}")
        bc = BgefCreater()
        bc.create_bgef(src_path, bin_siz, tissue_mask, str(tmp_path))
    else:
        register_mod.clog.warning(
            f"Reusing existing readable temporary tissue GEF and skipping recreate: {tmp_path}"
        )

    _patched_generate_vis_gef(str(tmp_path), dst_path)


def _patched_extract4matrix(p_naming, image_file, m_naming):
    from cellbin2.matrix.matrix import save_cell_bin_data, cMatrix
    from cellbin2.utils.stereo import generate_stereo_file
    from cellbin2.utils.common import TechType

    cell_mask_path = Path(p_naming.final_nuclear_mask)
    tissue_mask_path = Path(p_naming.final_tissue_mask)
    cell_correct_mask_path = Path(p_naming.final_cell_mask)

    legacy_adjust_mask_path = cell_correct_mask_path.with_name(
        f"{Path(p_naming.final_nuclear_mask).stem}_adjust.tif"
    )

    c_inp = None

    cm = cMatrix()
    cm.read(file_path=Path(image_file.file_path))
    binx = cm.binx

    if tissue_mask_path.exists():
        _patched_save_tissue_bin_data(
            image_file.file_path,
            str(m_naming.tissue_bin_matrix),
            str(tissue_mask_path),
            bin_siz=binx,
        )

        c_inp = m_naming.tissue_bin_matrix

        if image_file.tech == TechType.Transcriptomics:
            generate_stereo_file(
                save_path=p_naming.stereo,
                gef=m_naming.tissue_bin_matrix,
            )
    else:
        register_mod.clog.info(f"{tissue_mask_path} not exists, skip tissue gef generation")

    if c_inp is None:
        c_inp = image_file.file_path

    if cell_mask_path.exists():
        save_cell_bin_data(
            c_inp,
            str(m_naming.cell_bin_matrix),
            str(cell_mask_path),
        )
    else:
        register_mod.clog.info(f"{cell_mask_path} not exists, skip nuclear gef generation")

    # Some runs produced legacy *_mask_adjust.tif files, while CellBin2 expected *_cell_mask.tif.
    # Use the legacy adjusted mask when available.
    if (not cell_correct_mask_path.exists()) and legacy_adjust_mask_path.exists():
        shutil.copy2(legacy_adjust_mask_path, cell_correct_mask_path)
        register_mod.clog.warning(
            f"Aliased legacy adjusted mask to expected final cell mask path: {cell_correct_mask_path}"
        )

    if cell_correct_mask_path.exists():
        save_cell_bin_data(
            c_inp,
            str(m_naming.cell_correct_bin_matrix),
            str(cell_correct_mask_path),
        )

        if image_file.tech == TechType.Transcriptomics:
            generate_stereo_file(
                save_path=p_naming.stereo,
                cellbin_gef=m_naming.cell_correct_bin_matrix,
            )
    else:
        register_mod.clog.info(
            f"{cell_correct_mask_path} not exists, skip adjusted cellbin gef generation"
        )


def _patched_extract4stitched(image_file, param_chip, m_naming, config, detect_feature=True):
    from cellbin2.contrib.alignment.basic import TemplateInfo
    from cellbin2.image import cbimwrite
    from cellbin2.image.augmentation import f_ij_16_to_8, f_resize
    from cellbin2.matrix.box_detect import detect_chip_box
    from cellbin2.modules.extract.matrix_extract import cMatrix
    from cellbin2.utils.stereo_chip import StereoChip

    cm = cMatrix()
    cm.read(file_path=Path(image_file.file_path))
    binx = cm.binx

    cm.check_standards(config.genetic_standards)

    if binx != 1:
        sc = StereoChip()
        sc.parse_info(chip_no=m_naming.sn)

        track_points = sc.template_points

        cm._template = TemplateInfo(
            template_recall=1.0,
            template_valid_area=1.0,
            trackcross_qc_pass_flag=1,
            trackline_channel=0,
            rotation=0.0,
            scale_x=1.0,
            scale_y=1.0,
            template_points=track_points,
        )

        cbimwrite(str(m_naming.heatmap).replace(".tif", f"_bin{binx}.tif"), cm.heatmap)

        gene_mat = cm._gene_mat
        gene_mat = f_ij_16_to_8(gene_mat)

        if gene_mat is not None and gene_mat.size > 0:
            new_shape = (gene_mat.shape[0] * binx, gene_mat.shape[1] * binx)
            gene_mat_resized = f_resize(gene_mat, shape=new_shape, mode="BICUBIC")
            cm._gene_mat = gene_mat_resized

    elif detect_feature:
        try:
            cm.detect_feature(
                ref=param_chip.fov_template,
                chip_size=min(param_chip.chip_specif),
            )
        except Exception as exc:
            register_mod.clog.warning(
                f"Matrix feature detection failed, fallback to empty template/chip-box-only path: {exc}"
            )

            try:
                cm._chip_box = detect_chip_box(cm._gene_mat, min(param_chip.chip_specif))
            except Exception as chip_exc:
                register_mod.clog.warning(
                    f"Matrix chip-box detection also failed during fallback: {chip_exc}"
                )
                cm._chip_box = None

            cm._template = TemplateInfo(
                template_recall=0.0,
                template_valid_area=0.0,
                trackcross_qc_pass_flag=0,
                trackline_channel=0,
                rotation=0.0,
                scale_x=1.0,
                scale_y=1.0,
                template_points=np.zeros((0, 4), dtype=np.float32),
            )
        else:
            gene_tps = cm.template.template_points[:, :2]
            np.savetxt(m_naming.matrix_template, gene_tps)

    cbimwrite(m_naming.heatmap, cm.heatmap)

    return cm, binx


def _patched_run_register(*args, **kwargs):
    try:
        return _ORIGINAL_RUN_REGISTER(*args, **kwargs)
    except AttributeError as exc:
        if "'NoneType' object has no attribute 'offset'" not in str(exc):
            raise

        cur_f_name = kwargs.get("cur_f_name")

        if cur_f_name is None and len(args) >= 2:
            cur_f_name = args[1]

        if cur_f_name is None:
            raise

        # Registration failed to produce either track-cross or chip-box output.
        # Fall back to the same no-registration rename path used elsewhere in scheduler.
        register_mod.clog.warning(
            "Registration returned no usable output; fallback to no-registration transform path."
        )
        register_mod.transform_to_register(cur_f_name=cur_f_name)

        return None


def main():
    # Apply project-specific compatibility patches before calling CellBin2.
    matrix_mod.cMatrix.read = _patched_read
    matrix_mod.generate_vis_gef = _patched_generate_vis_gef
    matrix_mod.save_tissue_bin_data = _patched_save_tissue_bin_data
    matrix_mod.extract4matrix = _patched_extract4matrix

    matrix_extract_mod.extract4matrix = _patched_extract4matrix
    matrix_extract_mod.extract4stitched = _patched_extract4stitched

    register_mod.extract4stitched = _patched_extract4stitched
    register_mod.run_register = _patched_run_register

    scheduler_mod.run_register = _patched_run_register

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", action="store", type=str, required=True, dest="chip_no")
    parser.add_argument("-i", action="store", type=str, dest="input_image")
    parser.add_argument(
        "-s",
        action="store",
        type=str,
        dest="stain_type",
        choices=(TechType.ssDNA.name, TechType.DAPI.name, TechType.HE.name),
    )
    parser.add_argument("-mi", nargs="+", dest="more_images")
    parser.add_argument("-m", action="store", type=str, dest="matrix_file")
    parser.add_argument("-pr", action="store", type=str, dest="protein_matrix_file")
    parser.add_argument(
        "-k",
        action="store",
        type=str,
        default="Stereo-CITE_T_FF V1.0 R",
        dest="kit",
        choices=KIT_VERSIONS + KIT_VERSIONS_R,
    )
    parser.add_argument("-p", action="store", type=str, dest="param_file")
    parser.add_argument("-w", action="store", type=str, dest="weights_root")
    parser.add_argument("-o", action="store", type=str, required=True, dest="output_path")
    parser.add_argument("-r", action="store_true", dest="report")
    parser.add_argument("-d", action="store_true", default=bPlaceHolder, dest="debug")

    args, extra = parser.parse_known_args()

    cbp.main(args, extra)


if __name__ == "__main__":
    os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
    os.environ["HDF5_DISABLE_VERSION_CHECK"] = "1"

    main()
```
