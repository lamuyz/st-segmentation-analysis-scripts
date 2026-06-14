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

## Parameters

The watershed workflow was mainly run with the standard settings described in the Spateo documentation.

Cell expansion was included as part of the Spateo workflow according to the documented parameter settings.

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

## 参数说明

Watershed 流程主要按照 Spateo 官方文档中的标准设置运行。

扩细胞步骤作为 Spateo 流程的一部分，按照文档提供的参数设置完成。

大型输入文件和完整分割输出不保存在该仓库中。

## 参考链接

Spateo 官方仓库：https://github.com/aristoteleo/spateo-release

