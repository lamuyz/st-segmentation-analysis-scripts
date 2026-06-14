# Scripts

## Overview

This folder contains shared post-processing and visualization scripts used after cell segmentation.

The scripts were used to construct expression matrices, summarize QC metrics, perform QC filtering, and generate figures for result checking.

## Input Data Notes

The main input files in this project were tissue or staining images in `.tif` format and transcript count tables in `.parquet` format.

For some workflows, the transcript table needed to be converted from `.parquet` to GEM format before running the software.

## Script List

| Script                                    | Purpose                                                                                |
| ----------------------------------------- | -------------------------------------------------------------------------------------- |
| `convert_parquet_to_gem.py`               | Converts transcript count data from `.parquet` to GEM format.                          |
| `build_h5ad_from_mask_and_transcripts.py` | Builds a cell-level `.h5ad` matrix from segmentation masks and transcript coordinates. |
| `summarize_h5ad_qc_metrics.py`            | Summarizes basic QC metrics from an `.h5ad` file.                                      |
| `plot_qc_histogram.py`                    | Plots histograms of QC metrics.                                                        |
| `plot_qc_violin_and_filter.py`            | Plots QC violin plots and generates a filtered `.h5ad` file.                           |
| `plot_spatial_qc_metrics.py`              | Plots spatial distributions of QC metrics.                                             |
| `plot_spatial_mapping_overview.py`        | Generates a 2×2 overview figure for checking image-mask-transcript mapping.            |

## Notes

Input paths, output paths, sample names, and figure names should be updated before running.

Large input files, complete masks, generated figures, `.h5ad` files, and logs are not stored in this repository.

---

# Scripts 中文说明

## 概述

本文件夹保存细胞分割之后使用的通用后处理和可视化脚本。

这些脚本用于构建表达矩阵、汇总 QC 指标、进行 QC 过滤，以及生成结果检查用的图。

## 输入数据说明

本项目中主要使用的输入文件包括 `.tif` 格式的组织图像或染色图像，以及 `.parquet` 格式的转录本计数表。

部分软件或流程需要 GEM 格式的转录本表，因此需要先将 `.parquet` 文件转换为 GEM 文件。

## 脚本列表

| 脚本                                        | 用途                                  |
| ----------------------------------------- | ----------------------------------- |
| `convert_parquet_to_gem.py`               | 将 `.parquet` 格式的转录本计数表转换为 GEM 格式。   |
| `build_h5ad_from_mask_and_transcripts.py` | 根据分割 mask 和转录本坐标构建细胞级 `.h5ad` 表达矩阵。 |
| `summarize_h5ad_qc_metrics.py`            | 汇总 `.h5ad` 文件中的基础 QC 指标。            |
| `plot_qc_histogram.py`                    | 绘制 QC 指标直方图。                        |
| `plot_qc_violin_and_filter.py`            | 绘制 QC 指标小提琴图，并生成过滤后的 `.h5ad` 文件。    |
| `plot_spatial_qc_metrics.py`              | 绘制 QC 指标的空间分布图。                     |
| `plot_spatial_mapping_overview.py`        | 生成 2×2 总览图，用于检查图像、mask 和转录本映射关系。    |

## 说明

实际运行前需要根据具体数据修改输入路径、输出路径、样本名称和图像名称。

大型输入文件、完整 mask、生成图片、`.h5ad` 文件和日志文件不保存在该仓库中。
