# CellBin2

This folder contains the CellBin2-related environment record, patched runner, example parameter file, and example running scripts used in this project.

CellBin2 was run with sample-specific parameter files. A project-local patched runner was used to improve compatibility with different input formats and to make the workflow more robust across datasets.

## Files

```text
cellbin2/
├── README.md
├── environment_cellbin2.yml
├── run_cellbin_pipeline_patched_signed_gem.py
├── cellbin2_example_params.json
├── run_cellbin2_single_sample.sh
├── run_cellbin2_queue_example.sh
├── run_cellbin2_after_pid_example.sh
└── cellbin2_patch_notes.md
```

## File Description

| File                                                           | Description                                                                   |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `environment_cellbin2.yml`                                     | Conda environment record used for CellBin2.                                   |
| `run_cellbin_pipeline_patched_signed_gem.py`                   | Project-local patched CellBin2 runner used in this project.                   |
| [`cellbin2_example_params.json`](cellbin2_example_params.json) | Example parameter file showing the configuration format used in this project. |
| `run_cellbin2_single_sample.sh`                                | Example script for running CellBin2 on one sample.                            |
| `run_cellbin2_queue_example.sh`                                | Example script for running multiple CellBin2 samples sequentially.            |
| `run_cellbin2_after_pid_example.sh`                            | Example script for starting CellBin2 jobs after another process finishes.     |
| [`cellbin2_patch_notes.md`](cellbin2_patch_notes.md)           | Brief notes on the local compatibility changes made to the CellBin2 runner.   |

## Software Environment

The CellBin2 workflow was run in a separate conda environment.

Main environment information:

```text
CellBin2: 1.2.1
Python: 3.8.20
PyTorch: 2.4.1+cu118
```

The full environment record is provided in:

```text
environment_cellbin2.yml
```

## Usage Notes

The scripts and parameter file in this folder are simplified records of the actual running workflow.

Before reuse, users should update:

* input image path
* input transcriptomics matrix path
* output directory
* sample name
* CellBin2 parameter file
* conda environment path

For an example parameter file, see [`cellbin2_example_params.json`](cellbin2_example_params.json).

For details about local compatibility changes, see [`cellbin2_patch_notes.md`](cellbin2_patch_notes.md).

## Notes

This folder is intended for workflow traceability rather than full data reproduction.

Large files are not included in this repository, including:

* raw spatial transcriptomics data
* large tissue or staining images
* complete CellBin2 output folders
* segmentation masks
* GEF files
* complete expression matrices
* intermediate files and logs

Please refer to the original CellBin2 repository and documentation for official installation instructions, full workflow details, and citation information.

---

# CellBin2 中文说明

本文件夹保存本项目中 CellBin2 相关的运行环境、修改后的 runner、参数文件示例和运行脚本示例。

在实际运行中，CellBin2 使用样本对应的参数文件。由于不同数据集的输入格式和中间结果情况并不完全一致，本项目使用了本地修改后的 runner，以提高流程的兼容性和稳定性。

## 文件结构

```text
cellbin2/
├── README.md
├── environment_cellbin2.yml
├── run_cellbin_pipeline_patched_signed_gem.py
├── cellbin2_example_params.json
├── run_cellbin2_single_sample.sh
├── run_cellbin2_queue_example.sh
├── run_cellbin2_after_pid_example.sh
└── cellbin2_patch_notes.md
```

## 文件说明

| 文件                                                             | 说明                               |
| -------------------------------------------------------------- | -------------------------------- |
| `environment_cellbin2.yml`                                     | 运行 CellBin2 使用的 conda 环境记录。      |
| `run_cellbin_pipeline_patched_signed_gem.py`                   | 本项目中使用的本地修改版 CellBin2 runner。    |
| [`cellbin2_example_params.json`](cellbin2_example_params.json) | CellBin2 参数文件示例，用于展示本项目使用的配置格式。  |
| `run_cellbin2_single_sample.sh`                                | 单个样本运行 CellBin2 的示例脚本。           |
| `run_cellbin2_queue_example.sh`                                | 多个样本顺序运行 CellBin2 的示例脚本。         |
| `run_cellbin2_after_pid_example.sh`                            | 等待已有进程结束后再启动后续 CellBin2 任务的示例脚本。 |
| [`cellbin2_patch_notes.md`](cellbin2_patch_notes.md)           | CellBin2 runner 本地适配性修改的简要说明。    |

## 软件环境

CellBin2 使用单独的 conda 环境运行。

主要环境信息如下：

```text
CellBin2: 1.2.1
Python: 3.8.20
PyTorch: 2.4.1+cu118
```

完整环境记录见：

```text
environment_cellbin2.yml
```

## 使用说明

本文件夹中的脚本和参数文件是根据实际运行流程整理后的简化示例。

实际复用前需要根据本地环境修改：

* 输入图像路径
* 输入转录组矩阵路径
* 输出目录
* 样本名称
* CellBin2 参数文件
* conda 环境路径

参数文件示例见 [`cellbin2_example_params.json`](cellbin2_example_params.json)。

本地适配性修改说明见 [`cellbin2_patch_notes.md`](cellbin2_patch_notes.md)。

## 说明

本文件夹主要用于记录分析流程，方便追溯运行方式，而不是用于完整数据复现。

本仓库不包含大型文件，包括：

* 原始空间转录组数据
* 大型组织图像或染色图像
* 完整 CellBin2 输出目录
* 分割 mask
* GEF 文件
* 完整表达矩阵
* 中间文件和运行日志

正式安装、完整流程和引用信息请参考 CellBin2 官方仓库和官方文档。


