# Cellpose2

## Overview

This folder records the Cellpose2 environment and command used in this project.

Cellpose2 was used with the pretrained `cyto2` model for general cell segmentation.

## Files

```text
cellpose2/
├── environment_cellpose2.yml
└── README.md
```

## Command Used

Cellpose2 was run through the official command-line interface:

```bash
python -m cellpose \
  --dir /path/to/input_images \
  --pretrained_model cyto2 \
  --chan 0 \
  --save_tif
```

In the actual analysis, `/path/to/input_images` was replaced by the corresponding dataset folder.

## Notes

The command above processes image files under the input directory and saves segmentation masks in `.tif` format.

Large input images, complete masks, and log files are not stored in this repository.

---

# Cellpose2 中文说明

## 概述

本文件夹保存本项目中 Cellpose2 相关的环境文件和运行命令。

Cellpose2 使用预训练的 `cyto2` 模型进行通用细胞分割。

## 文件说明

```text
cellpose2/
├── environment_cellpose2.yml
└── README.md
```

## 运行命令

Cellpose2 通过官方命令行接口运行：

```bash
python -m cellpose \
  --dir /path/to/input_images \
  --pretrained_model cyto2 \
  --chan 0 \
  --save_tif
```

在实际分析中，`/path/to/input_images` 替换为对应数据集的图像文件夹。

## 说明

上述命令会处理输入目录下的图像文件，并保存 `.tif` 格式的分割 mask。

大型输入图像、完整 mask 和日志文件不保存在该仓库中。

