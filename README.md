## Spatial Transcriptomics Cell Segmentation Analysis Scripts

## Overview

This repository collects selected scripts, environment files, and workflow notes used for cell segmentation analysis in subcellular-resolution spatial transcriptomics data.

The goal is to keep a lightweight and traceable record of the analysis workflow, including method-specific running scripts, software environments, and shared downstream analysis utilities. It is not intended to serve as a complete public benchmark or a full data-reproduction repository.

## Workflow

The overall workflow includes input data preparation, segmentation tool comparison, post-processing and matrix construction, QC analysis, and visualization.

![Workflow](figures/workflow.png)

For a more detailed workflow description, see [docs/workflow.md](docs/workflow.md).

## Repository Structure

```text
st-segmentation-analysis-scripts/
├── README.md
├── methods/
│   ├── cellpose/
│   ├── cellbin2/
│   ├── spateo_watershed/
│   └── stardist/
├── scripts/
├── docs/
│   ├── workflow.md
│   ├── data_description.md
│   └── notes_on_parameters.md
├── figures/
│   └── workflow.png
└── .gitignore
```

## Directory Description

### `methods/`

Method-specific scripts, environment files, and notes.

Each subfolder contains a separate README with details about the corresponding tool, including selected models, running scripts, environment files, command notes, or workflow notes.

### `scripts/`

Shared post-processing and visualization scripts.

These scripts are not tied to a single segmentation method. They were used for format conversion, expression matrix construction, QC metric calculation, QC filtering, spatial visualization, and mapping overview plots.

### `docs/`

Additional workflow and data notes.

This folder includes the overall workflow description, data description, and notes on parameter choices.

### `figures/`

Small figures used in the README or documentation, such as the workflow diagram.

## Software Links

Original software repositories:

* Cellpose: https://github.com/MouseLand/cellpose
* CellBin2: https://github.com/STOmics/cellbin2
* Spateo: https://github.com/aristoteleo/spateo-release
* StarDist: https://github.com/stardist/stardist

Please refer to the original repositories and publications for installation instructions, documentation, and citation information.

## Environment Notes

Different tools require different software environments. Environment files or dependency records are kept under the corresponding method folders.

## Data and Output Notes

To keep the repository lightweight and easy to maintain, large files are not uploaded, including:

* raw spatial transcriptomics data
* large tissue or staining images
* complete segmentation masks
* complete expression matrices
* large intermediate files
* complete HTML reports
* server logs and temporary debugging files

The repository mainly keeps:

* finalized running scripts
* environment files
* workflow notes
* shared analysis scripts
* small documentation figures

## Usage

Scripts are mainly provided for workflow traceability and code reference.

When running the scripts, update input and output paths according to the local computing environment. Method-specific usage notes are provided in each subfolder under `methods/`.

---

# 空间转录组细胞分割分析脚本

## 概述

这个项目整理了亚细胞分辨率空间转录组数据细胞分割分析中使用到的部分脚本、环境文件和流程记录。

主要目的是保存一个轻量、清晰、可追溯的分析流程记录，包括不同方法的运行脚本、软件环境，以及后续通用分析脚本。这里不是完整公开 benchmark，也不是完整数据复现仓库。

## 分析流程

整体流程包括输入数据整理、分割工具比较、分割后处理与矩阵构建、QC 分析和可视化。

更详细的流程说明见 [docs/workflow.md](docs/workflow.md)。

## 仓库结构

```text
st-segmentation-analysis-scripts/
├── README.md
├── methods/
│   ├── cellpose/
│   ├── cellbin2/
│   ├── spateo_watershed/
│   └── stardist/
├── scripts/
├── docs/
│   ├── workflow.md
│   ├── data_description.md
│   └── notes_on_parameters.md
├── figures/
│   └── workflow.png
└── .gitignore
```

## 文件夹说明

### `methods/`

保存不同分割方法相关的运行脚本、环境文件和说明。

每个子文件夹下有单独的 README，用来说明对应工具的模型选择、运行脚本、环境文件、命令记录或流程说明。

### `scripts/`

保存通用后处理和可视化脚本。

这些脚本通常不是某一个方法专属的，而是用于格式转换、表达矩阵构建、QC 指标统计、QC 过滤、空间可视化和 mapping overview 图生成。

### `docs/`

保存补充流程和数据说明。

该文件夹包括整体 workflow、数据说明和参数记录等文档。

### `figures/`

保存 README 或文档中使用的小型图片，例如 workflow 流程图。

## 软件链接

相关软件的原始仓库：

* Cellpose: https://github.com/MouseLand/cellpose
* CellBin2: https://github.com/STOmics/cellbin2
* Spateo: https://github.com/aristoteleo/spateo-release
* StarDist: https://github.com/stardist/stardist

具体安装方式、官方文档和引用信息请参考对应软件的原始仓库和论文说明。

## 环境说明

不同工具依赖的软件环境不同。环境文件或依赖记录分别放在对应的 `methods/` 子文件夹中。

## 数据和结果说明

为了让仓库保持轻量、清晰，以下大文件不上传：

* 原始空间转录组数据
* 大型组织图像或染色图像
* 完整分割 mask
* 完整表达矩阵
* 大型中间结果
* 完整 HTML 报告
* 服务器日志和临时调试文件

这里主要保存：

* 最终整理后的运行脚本
* 环境文件
* 流程记录
* 通用分析脚本
* 小型文档图片

## 使用说明

这些脚本主要用于流程溯源和代码查阅。

实际运行时，需要根据本地计算环境修改输入和输出路径。每个方法的具体使用说明见 `methods/` 下对应子文件夹的 README。
