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

## Version and Parameters

The software environment is recorded in `environment_cellpose4.yml`.

`cpsam` was run mainly with default Cellpose parameters, so that the results could be compared with other segmentation methods under a similar setting.

Only basic running options are exposed in the scripts, such as input path, output path, GPU ID, tile size, and overlap size.

## Notes

* The `batch` script processes all `.tif` / `.tiff` images under an input directory.
* The `tile` script is used for large images that require tiled processing and mask merging.
* Input paths, output paths, and GPU IDs should be adjusted before running.
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

## 版本和参数说明

具体软件环境记录在 `environment_cellpose4.yml` 中。

`cpsam` 基本使用 Cellpose 默认参数运行，这样可以让结果更适合与其他分割方法进行比较。

脚本中只保留了输入路径、输出路径、GPU ID、tile size 和 overlap size 等基础运行选项。

## 说明

* `batch` 脚本用于处理输入目录下的所有 `.tif` / `.tiff` 图像。
* `tile` 脚本用于大图切块分割和 mask 合并。
* 实际运行前需要根据本地环境调整输入路径、输出路径和 GPU ID。
* 大型输入图像、完整 mask 和日志文件不保存在该仓库中。

