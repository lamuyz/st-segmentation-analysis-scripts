# Cellpose4

## Overview

This folder records the Cellpose4 environment and scripts used in this project.

The Cellpose4 workflow used the `cpsam` model.

## Files

```text
cellpose4/
├── environment_cellpose4.yml
├── run_cellpose4_cpsam_batch.sh
└── run_cellpose4_cpsam_tile.py
```

## Software Version and Parameters

### Software version

- Main software: `Cellpose 4.0.9`
- Python: `3.9.25`
- PyTorch: `2.8.0`
- Environment file: `environment_cellpose4.yml`

### Model used

- `cpsam`

### Key parameters

- `--pretrained_model cpsam`
- `--save_tif`
- Tile-mode default `tile_size=4096`
- Tile-mode default `overlap=256`

### Running mode

- Batch scripts were used for directory-level processing.
- Tile scripts were used for large-image segmentation and mask merging.

`cpsam` was run mainly with default Cellpose parameters, so that the results could be compared with other segmentation methods under a similar setting.

## Notes

* The `batch` script processes all `.tif` / `.tiff` images under an input directory.
* The `tile` script is used for large images that require tiled processing and mask merging.
* Input and output paths should be adjusted before running.
* Large input images, complete masks, and log files are not stored in this repository.

---

# Cellpose4 中文说明

## 概述

本文件夹保存本项目中 Cellpose4 相关的环境文件和运行脚本。

Cellpose4 流程使用的是 `cpsam` 模型。

## 文件说明

```text
cellpose4/
├── environment_cellpose4.yml
├── run_cellpose4_cpsam_batch.sh
└── run_cellpose4_cpsam_tile.py
```

## 软件版本与参数

### 软件版本

- 主软件：`Cellpose 4.0.9`
- Python：`3.9.25`
- PyTorch：`2.8.0`
- 环境文件：`environment_cellpose4.yml`

### 使用模型

- `cpsam`

### 关键参数

- `--pretrained_model cpsam`
- `--save_tif`
- 切块模式默认 `tile_size=4096`
- 切块模式默认 `overlap=256`

### 运行方式

- `batch` 脚本用于目录级处理。
- `tile` 脚本用于大图切块分割和 mask 合并。

`cpsam` 基本使用 Cellpose 默认参数运行，这样可以让结果更适合与其他分割方法进行比较。

## 说明

* `batch` 脚本用于处理输入目录下的所有 `.tif` / `.tiff` 图像。
* `tile` 脚本用于大图切块分割和 mask 合并。
* 实际运行前需要根据本地环境调整输入路径和输出路径。
* 大型输入图像、完整 mask 和日志文件不保存在该仓库中。

