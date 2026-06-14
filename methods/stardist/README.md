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

## Parameters

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

## 参数说明

预训练模型根据输入图像类型进行选择。

StarDist 主要使用默认参数或标准设置运行，以保持不同方法之间的分析可比性。

大型输入文件和完整分割输出不保存在该仓库中。

## 参考链接

StarDist 官方仓库：https://github.com/stardist/stardist

