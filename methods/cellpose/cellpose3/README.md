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

## Software Version and Parameters

### Software version

- Main software: `Cellpose 3.1.1`
- Python: `3.10.19`
- PyTorch: `2.9.1`
- Environment file: `environment_cellpose3.yml`

### Models used

- `cyto3`
- `nuclei`

### Key parameters

- Batch examples use `--pretrained_model cyto3` or `--pretrained_model nuclei`
- `--save_tif`
- Tile-mode default `tile_size=4096`
- Tile-mode default `overlap=256`

### Running mode

- Batch scripts were used for directory-level processing of `.tif` / `.tiff` images.
- Tile scripts were used for large-image segmentation followed by mask merging.

Both `cyto3` and `nuclei` were run mainly with default Cellpose parameters, so that the results could be compared with other segmentation methods under a similar setting.

## Notes

* `batch` scripts process all `.tif` / `.tiff` images under an input directory.
* `tile` scripts are used for large images that require tiled processing and mask merging.
* Input and output paths should be adjusted before running.
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

## 软件版本与参数

### 软件版本

- 主软件：`Cellpose 3.1.1`
- Python：`3.10.19`
- PyTorch：`2.9.1`
- 环境文件：`environment_cellpose3.yml`

### 使用模型

- `cyto3`
- `nuclei`

### 关键参数

- 批处理示例使用 `--pretrained_model cyto3` 或 `--pretrained_model nuclei`
- `--save_tif`
- 切块模式默认 `tile_size=4096`
- 切块模式默认 `overlap=256`

### 运行方式

- `batch` 脚本用于目录级 `.tif` / `.tiff` 图像处理。
- `tile` 脚本用于大图切块分割和 mask 合并。

`cyto3` 和 `nuclei` 基本使用 Cellpose 默认参数运行，这样可以让结果更适合与其他分割方法进行比较。

## 说明

* `batch` 脚本用于处理输入目录下的所有 `.tif` / `.tiff` 图像。
* `tile` 脚本用于大图切块分割和 mask 合并。
* 实际运行前需要根据本地环境调整输入路径和输出路径。
* 大型输入图像、完整 mask 和日志文件不保存在该仓库中。

