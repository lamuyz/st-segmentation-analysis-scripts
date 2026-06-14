# Methods

## Overview

This folder contains method-specific records for the cell segmentation tools used in this project.

Each subfolder includes environment files, running scripts, command notes, or workflow notes, depending on how the method was actually run.

## Folder Structure

```text
methods/
├── cellpose/
├── cellbin2/
├── spateo_watershed/
└── stardist/
```

## Folder Notes

| Folder              | Description                                                                    |
| ------------------- | ------------------------------------------------------------------------------ |
| `cellpose/`         | Cellpose-related scripts and environment files, organized by Cellpose version. |
| `cellbin2/`         | CellBin2-related workflow notes and environment records.                       |
| `spateo_watershed/` | Spateo watershed command notes and environment records.                        |
| `stardist/`         | StarDist command notes and environment records.                                |

## Notes

Different segmentation tools were run in different ways, so the contents of each subfolder are not exactly the same.

Large input data, complete segmentation masks, intermediate outputs, and log files are not stored in this repository.

---

# Methods 中文说明

## 概述

本文件夹保存本项目中不同细胞分割工具对应的运行记录。

每个子文件夹根据实际运行方式保存对应的环境文件、运行脚本、命令记录或流程说明。

## 文件夹结构

```text
methods/
├── cellpose/
├── cellbin2/
├── spateo_watershed/
└── stardist/
```

## 文件夹说明

| 文件夹                 | 说明                                      |
| ------------------- | --------------------------------------- |
| `cellpose/`         | 保存 Cellpose 相关脚本和环境文件，并按 Cellpose 版本整理。 |
| `cellbin2/`         | 保存 CellBin2 相关流程说明和环境记录。                |
| `spateo_watershed/` | 保存 Spateo watershed 的命令记录和环境说明。         |
| `stardist/`         | 保存 StarDist 的命令记录和环境说明。                 |

## 说明

不同分割工具的运行方式并不完全相同，因此各子文件夹中保存的内容也不完全一样。

大型输入数据、完整分割 mask、中间结果和日志文件不保存在该仓库中。

