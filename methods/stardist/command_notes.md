# StarDist Command Notes

This file records the main commands used for StarDist segmentation in this project.

StarDist was run on individual datasets rather than through a unified batch script.

## Model Selection

Two pretrained StarDist models were considered:

| Model               | Typical input                                                  |
| ------------------- | -------------------------------------------------------------- |
| `2D_versatile_fluo` | Fluorescence or nuclear-staining images, such as DAPI or ssDNA |
| `2D_versatile_he`   | H&E-stained tissue images                                      |

The model was selected according to the input image type.

## Example Command

```python
st.cs.stardist(
    adata,
    layer="stain",
    model="2D_versatile_fluo",
    tilesize=2000,
    out_layer="ssdna_masks",
)

tiff.imwrite(
    "/path/to/output_masks.tif",
    adata.layers["ssdna_masks"].astype(np.uint32),
)
```

## Notes

* `layer="stain"` indicates that StarDist was applied to the staining image stored in `adata`.
* `model` was selected according to the image type.
* `tilesize=2000` was used for tiled prediction.
* `out_layer` stores the segmentation mask in `adata.layers`.
* The final mask was exported as a `.tif` file.
* Complete input images, intermediate objects, masks, and logs are not stored in this repository.
