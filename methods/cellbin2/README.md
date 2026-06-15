# CellBin2

## Overview

This folder records the CellBin2 environment, patched runner, and example running scripts used in this project.

CellBin2 was included as one of the segmentation methods in the comparison. In this project, CellBin2 was run with sample-specific parameter files. A patched runner was used for some datasets to improve compatibility with the input matrix format and to make the workflow more robust.

## Files

```text
cellbin2/
├── environment_cellbin2.yml
├── run_cellbin_pipeline_patched_signed_gem.py
├── run_cellbin2_single_sample.sh
├── run_cellbin2_queue_example.sh
└── run_cellbin2_after_pid_example.sh
```

## File Notes

| File                                         | Description                                                                |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| `environment_cellbin2.yml`                   | Conda environment record for running CellBin2.                             |
| `run_cellbin_pipeline_patched_signed_gem.py` | Patched CellBin2 runner used for compatibility fixes in this project.      |
| `run_cellbin2_single_sample.sh`              | Example script for running one CellBin2 sample.                            |
| `run_cellbin2_queue_example.sh`              | Example script for running multiple samples sequentially.                  |
| `run_cellbin2_after_pid_example.sh`          | Example script for starting queued samples after another process finishes. |

## Adaptation Notes

Some compatibility changes were made to run CellBin2 on the datasets used in this project.

The main changes included:

* supporting GEM files without `#OffsetX` / `#OffsetY` header lines;
* reading count columns written as float values and rounding them before accumulation;
* limiting visual GEF generation to safer bin sizes;
* reusing an existing readable temporary tissue GEF when available;
* handling naming mismatch between legacy `*_mask_adjust.tif` files and the expected `*_cell_mask.tif` files;
* adding a fallback when matrix feature detection failed during `extract4stitched()`;
* adding a fallback when registration returned `None` and downstream code still attempted to access `info.offset`.

These changes were made to improve workflow robustness for the dataset collection used in this project. They were not intended to change the core CellBin2 segmentation model itself.

## Notes

These scripts are simplified examples based on the actual CellBin2 running records.

Input paths, output paths, sample names, parameter files, and environment paths should be updated before running.

Large input data, complete CellBin2 outputs, masks, intermediate files, and log files are not stored in this repository.

---

# CellBin2 中文说明

## 概述

本文件夹保存本项目中 CellBin2 相关的运行环境、适配性修改后的 runner 和示例运行脚本。

CellBin2 是本项目比较的细胞分割方法之一。在实际运行中，CellBin2 使用样本对应的参数文件。部分数据使用了修改后的 runner，以适配输入矩阵格式并提高流程稳定性。

## 文件说明

```text
cellbin2/
├── environment_cellbin2.yml
├── run_cellbin_pipeline_patched_signed_gem.py
├── run_cellbin2_single_sample.sh
├── run_cellbin2_queue_example.sh
└── run_cellbin2_after_pid_example.sh
```

## 文件用途

| 文件                                           | 说明                            |
| -------------------------------------------- | ----------------------------- |
| `environment_cellbin2.yml`                   | 记录运行 CellBin2 使用的 conda 环境。   |
| `run_cellbin_pipeline_patched_signed_gem.py` | 本项目中用于适配性修改的 CellBin2 runner。 |
| `run_cellbin2_single_sample.sh`              | 单个样本运行 CellBin2 的示例脚本。        |
| `run_cellbin2_queue_example.sh`              | 多个样本串行运行的示例脚本。                |
| `run_cellbin2_after_pid_example.sh`          | 等待已有进程结束后再启动后续样本的示例脚本。        |

## 适配性修改说明

为了在本项目的数据上顺利运行 CellBin2，对部分流程做了适配性修改。

主要包括：

* 支持没有 `#OffsetX` / `#OffsetY` 头部信息的 GEM 文件；
* 支持将 count 列中以浮点形式记录的数值读取后四舍五入再累加；
* 将 visual GEF 的生成限制在更安全的 bin size 范围内；
* 当已有可读取的临时 tissue GEF 文件时，复用该文件，避免重复生成；
* 处理 legacy `*_mask_adjust.tif` 与流程期望的 `*_cell_mask.tif` 之间的命名不一致问题；
* 当 `extract4stitched()` 中矩阵特征点检测失败时，增加兜底逻辑，避免流程直接中断；
* 当 registration 返回 `None`、但下游仍访问 `info.offset` 时，增加 no-registration fallback 逻辑。

这些修改主要是为了提高流程在本项目数据集上的稳定性，并不是对 CellBin2 核心分割模型本身进行修改。

## 说明

这些脚本是根据实际 CellBin2 运行记录整理后的简化示例。

实际运行前需要根据本地环境修改输入路径、输出路径、样本名称、参数文件和环境路径。

大型输入数据、完整 CellBin2 输出结果、mask、中间文件和日志文件不保存在该仓库中。

