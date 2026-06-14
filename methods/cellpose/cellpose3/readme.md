# Cellpose3

## Overview

This folder records the Cellpose3 environment and scripts used in this project.

Two Cellpose3 models were used:

| Model    | Use                       |
| -------- | ------------------------- |
| `cyto3`  | General cell segmentation |
| `nuclei` | Nuclear segmentation      |

## Files

```text
cellpose3/
├── environment_cellpose3.yml
├── run_cellpose3_cyto3_batch.sh
├── run_cellpose3_cyto3_tile.py
├── run_cellpose3_nuclei_batch.sh
└── run_cellpose3_nuclei_tile.py
```

## Version and Parameters

The software environment is recorded in `environment_cellpose3.yml`.

Both `cyto3` and `nuclei` were run mainly with default Cellpose parameters, so that the results could be compared with other segmentation methods under a similar setting.

Only basic running options are exposed in the scripts, such as input path, output path, GPU ID, tile size, and overlap size.

## Notes

* `batch` scripts process all `.tif` / `.tiff` images under an input directory.
* `tile` scripts are used for large images that require tiled processing and mask merging.
* Input paths, output paths, and GPU IDs should be adjusted before running.
* Large input images, complete masks, and log files are not stored in this repository.

---

# Cellpose3 中文说明

## 概述

本文件夹保存本项目中 Cellpose3 相关的环境文件和运行脚本。

这里包括两个 Cellpose3 模型：

| 模型       | 用途     |
| -------- | ------ |
| `cyto3`  | 通用细胞分割 |
| `nuclei` | 细胞核分割  |

## 文件说明

```text
cellpose3/
├── environment_cellpose3.yml
├── run_cellpose3_cyto3_batch.sh
├── run_cellpose3_cyto3_tile.py
├── run_cellpose3_nuclei_batch.sh
└── run_cellpose3_nuclei_tile.py
```

## 版本和参数说明

具体软件环境记录在 `environment_cellpose3.yml` 中。

`cyto3` 和 `nuclei` 基本使用 Cellpose 默认参数运行，这样可以让结果更适合与其他分割方法进行比较。

脚本中只保留了输入路径、输出路径、GPU ID、tile size 和 overlap size 等基础运行选项。

## 说明

* `batch` 脚本用于处理输入目录下的所有 `.tif` / `.tiff` 图像。
* `tile` 脚本用于大图切块分割和 mask 合并。
* 实际运行前需要根据本地环境调整输入路径、输出路径和 GPU ID。
* 大型输入图像、完整 mask 和日志文件不保存在该仓库中。

