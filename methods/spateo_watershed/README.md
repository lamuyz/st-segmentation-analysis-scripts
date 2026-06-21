# Spateo Watershed

## Overview

This folder records the Spateo environment and workflow notes used in this project.

The segmentation was performed with the built-in watershed-based workflow provided by Spateo.

## Files

```text
spateo_watershed/
├── environment_spateo.yml
└── command_notes.md
```

## Running Notes

Spateo was mainly run from the command line on individual datasets, rather than through a unified batch script.

The detailed command-line records and parameter notes are kept in `command_notes.md`.

## Software Version and Parameters

### Software version

- Main software: `spateo-release 1.1.1`
- Python: `3.9.25`
- PyTorch: `2.8.0`
- Environment file: `environment_spateo.yml`

### Workflow used

- Built-in Spateo watershed-based segmentation workflow
- Label expansion step applied after watershed segmentation

### Key parameters

- `st.cs.find_peaks_from_mask(adata, "stain", 7)`: detect seed points from the stain image mask; `7` controls the peak detection neighborhood scale.
- `st.cs.watershed(adata, "stain", 5, out_layer="watershed_labels")`: run watershed segmentation on the stain image; `5` controls the smoothing or structuring scale used in the workflow.
- `st.cs.expand_labels(..., distance=5, max_area=400, out_layer="watershed_labels_expanded")`: expand watershed labels outward; `distance=5` controls the expansion radius and `max_area=400` limits over-expansion of very large regions.

### Running mode

- Spateo was mainly run on individual datasets from the command line or an interactive Python session.
- Expanded masks were exported as `.tif` files after segmentation.

## Notes

The watershed workflow was mainly run with the standard settings described in the Spateo documentation.

Cell expansion was included as part of the Spateo workflow using the official default values `distance=5` and `max_area=400`.

Large input files and complete segmentation outputs are not stored in this repository.

## Reference

Official Spateo repository: https://github.com/aristoteleo/spateo-release

---

# Spateo 内置 Watershed 中文说明

## 概述

本文件夹保存本项目中 Spateo 相关的环境文件和流程记录。

细胞分割使用的是 Spateo 提供的内置 watershed-based workflow。

## 文件说明

```text
spateo_watershed/
├── environment_spateo.yml
└── command_notes.md
```

## 运行说明

Spateo 主要是通过命令行对单个数据集逐个运行，而不是使用统一的批处理脚本。

具体命令记录和参数说明保存在 `command_notes.md` 中。

## 软件版本与参数

### 软件版本

- 主软件：`spateo-release 1.1.1`
- Python：`3.9.25`
- PyTorch：`2.8.0`
- 环境文件：`environment_spateo.yml`

### 使用流程

- Spateo 内置 watershed-based segmentation workflow
- 在 watershed 之后执行扩细胞步骤

### 关键参数

- `st.cs.find_peaks_from_mask(adata, "stain", 7)`：从 stain 图像掩膜中检测 seed points，`7` 控制峰值检测的邻域尺度。
- `st.cs.watershed(adata, "stain", 5, out_layer="watershed_labels")`：基于 stain 图像执行 watershed 分割，`5` 控制流程中使用的平滑或结构尺度。
- `st.cs.expand_labels(..., distance=5, max_area=400, out_layer="watershed_labels_expanded")`：对 watershed 标签向外扩张，`distance=5` 控制扩张距离，`max_area=400` 用于限制过大的扩张区域。

### 运行方式

- Spateo 主要通过命令行或交互式 Python 会话对单个数据集运行。
- 分割后会将 expanded mask 导出为 `.tif` 文件。

## 说明

Watershed 流程主要按照 Spateo 官方文档中的标准设置运行。

扩细胞步骤作为 Spateo 流程的一部分，使用官方默认参数 `distance=5` 和 `max_area=400` 完成。

大型输入文件和完整分割输出不保存在该仓库中。

## 参考链接

Spateo 官方仓库：https://github.com/aristoteleo/spateo-release

