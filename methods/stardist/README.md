# StarDist

## Overview

This folder records the StarDist environment and workflow notes used in this project.

StarDist was included as one of the image segmentation methods in the benchmark workflow.

## Files

```text
stardist/
├── environment_stardist.yml
└── command_notes.md
```

## Running Notes

StarDist was mainly run from the command line on individual datasets, rather than through a unified batch script.

The detailed command-line records and parameter notes are kept in `command_notes.md`.

## Software Version and Parameters

### Software version

- Main software: `StarDist 0.9.2`
- Python: `3.9.25`
- PyTorch: `2.8.0`
- Associated environment also included `spateo-release 1.1.1`
- Environment file: `environment_stardist.yml`

### Models used

- `2D_versatile_fluo`
- `2D_versatile_he`

### Key parameters

- Recorded call used `layer="stain"`
- Recorded model selection: `model="2D_versatile_fluo"` (chosen according to the actual input image type)
- Recorded tiled prediction setting: `tilesize=2000`
- Recorded output layer: `out_layer="ssdna_masks"`

### Running mode

- StarDist was mainly run on individual datasets rather than through one unified batch script.
- The pretrained model was selected according to the actual input image type (for example, fluorescence-like vs. H&E-like images).

## Notes

Pretrained models were selected according to the input image type.

StarDist was mainly run with default or standard settings to keep the analysis comparable across methods.

Large input files and complete segmentation outputs are not stored in this repository.

## Reference

Official StarDist repository: https://github.com/stardist/stardist

---

# StarDist 中文说明

## 概述

本文件夹保存本项目中 StarDist 相关的环境文件和流程记录。

StarDist 作为 benchmark 分析中的一种图像分割方法纳入比较。

## 文件说明

```text
stardist/
├── environment_stardist.yml
└── command_notes.md
```

## 运行说明

StarDist 主要是通过命令行对单个数据集逐个运行，而不是使用统一的批处理脚本。

具体命令记录和参数说明保存在 `command_notes.md` 中。

## 软件版本与参数

### 软件版本

- 主软件：`StarDist 0.9.2`
- Python：`3.9.25`
- PyTorch：`2.8.0`
- 关联环境中还包括：`spateo-release 1.1.1`
- 环境文件：`environment_stardist.yml`

### 使用模型

- `2D_versatile_fluo`
- `2D_versatile_he`

### 关键参数

- 记录到的调用使用 `layer="stain"`
- 记录到的模型选择：`model="2D_versatile_fluo"`（根据实际输入图像类型选择）
- 记录到的切块预测参数：`tilesize=2000`
- 记录到的输出层：`out_layer="ssdna_masks"`

### 运行方式

- StarDist 主要对单个数据集逐个运行，而不是通过统一批处理脚本。
- 预训练模型根据实际输入图像类型进行选择（例如更接近荧光图像或更接近 H&E 图像）。

## 说明

预训练模型根据输入图像类型进行选择。

StarDist 主要使用默认参数或标准设置运行，以保持不同方法之间的分析可比性。

大型输入文件和完整分割输出不保存在该仓库中。

## 参考链接

StarDist 官方仓库：https://github.com/stardist/stardist

