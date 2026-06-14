#!/bin/bash

set -eo pipefail

# Run Cellpose3-nuclei on all tif/tiff images under an input directory.
#
# Usage:
#   bash run_cellpose3_nuclei_batch.sh <input_root> <output_root> <log_root> [gpu_id]
#
# Example:
#   bash run_cellpose3_nuclei_batch.sh \
#     /path/to/input_images \
#     /path/to/output/cellpose3_nuclei_default \
#     /path/to/logs/cellpose3_nuclei_default \
#     1

if [ "$#" -lt 3 ]; then
    echo "Usage: bash $0 <input_root> <output_root> <log_root> [gpu_id]"
    exit 1
fi

INPUT_ROOT="$1"
OUTPUT_ROOT="$2"
LOG_ROOT="$3"
GPU_ID="${4:-1}"

MODEL_NAME="nuclei"
CONDA_ENV="cellpose3"
CPU_THREADS="${CPU_THREADS:-20}"

mkdir -p "$OUTPUT_ROOT"
mkdir -p "$LOG_ROOT"

export CUDA_VISIBLE_DEVICES="$GPU_ID"
export OMP_NUM_THREADS="$CPU_THREADS"
export MKL_NUM_THREADS="$CPU_THREADS"
export OPENBLAS_NUM_THREADS="$CPU_THREADS"
export NUMEXPR_NUM_THREADS="$CPU_THREADS"

source /etc/profile
module load Anaconda/2024.10-1
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV"

MAIN_LOG="$LOG_ROOT/run_all_$(date +%Y%m%d_%H%M%S).log"

echo "========================================" | tee -a "$MAIN_LOG"
echo "Cellpose3-nuclei batch run" | tee -a "$MAIN_LOG"
echo "Start time: $(date)" | tee -a "$MAIN_LOG"
echo "Node: $(hostname)" | tee -a "$MAIN_LOG"
echo "Input root: $INPUT_ROOT" | tee -a "$MAIN_LOG"
echo "Output root: $OUTPUT_ROOT" | tee -a "$MAIN_LOG"
echo "Log root: $LOG_ROOT" | tee -a "$MAIN_LOG"
echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES" | tee -a "$MAIN_LOG"
echo "CPU threads: $CPU_THREADS" | tee -a "$MAIN_LOG"
echo "Conda environment: $CONDA_ENV" | tee -a "$MAIN_LOG"
echo "========================================" | tee -a "$MAIN_LOG"

if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi | tee -a "$MAIN_LOG"
else
    echo "nvidia-smi not found; skip GPU status check." | tee -a "$MAIN_LOG"
fi

python - <<'PY' | tee -a "$MAIN_LOG"
import torch
from cellpose import core
import importlib.metadata as metadata

print("torch:", torch.__version__)
print("cuda available:", torch.cuda.is_available())
print("cuda version:", torch.version.cuda)
print("gpu count:", torch.cuda.device_count())
if torch.cuda.is_available():
    print("gpu name:", torch.cuda.get_device_name(0))
print("cellpose:", metadata.version("cellpose"))
print("cellpose use_gpu:", core.use_gpu())
PY

mapfile -t TIF_FILES < <(
    find "$INPUT_ROOT" -type f \( -iname "*.tif" -o -iname "*.tiff" \) \
    ! -iname "*mask*" \
    ! -iname "*masks*" \
    ! -iname "*overlay*" \
    ! -iname "*seg*" \
    ! -iname "*label*" \
    | sort
)

echo "Found ${#TIF_FILES[@]} tif/tiff input files." | tee -a "$MAIN_LOG"

if [ "${#TIF_FILES[@]}" -eq 0 ]; then
    echo "No tif/tiff files found. Exit." | tee -a "$MAIN_LOG"
    exit 0
fi

RUN_COUNT=0
SKIP_COUNT=0
FAIL_COUNT=0

for IMAGE_PATH in "${TIF_FILES[@]}"; do
    REL_PATH="${IMAGE_PATH#$INPUT_ROOT/}"
    REL_DIR="$(dirname "$REL_PATH")"
    BASENAME="$(basename "$IMAGE_PATH")"
    STEM="${BASENAME%.*}"

    OUT_DIR="$OUTPUT_ROOT/$REL_DIR/${STEM}_cellpose3_${MODEL_NAME}"
    IMG_LOG="$LOG_ROOT/$REL_DIR/${STEM}.log"
    DONE_FLAG="$OUT_DIR/.done"

    mkdir -p "$OUT_DIR"
    mkdir -p "$(dirname "$IMG_LOG")"

    if [ -f "$DONE_FLAG" ] || find "$OUT_DIR" -maxdepth 1 -type f \( -iname "*_masks.tif" -o -iname "*_seg.npy" \) | grep -q .; then
        echo "SKIP existing result: $IMAGE_PATH" | tee -a "$MAIN_LOG"
        SKIP_COUNT=$((SKIP_COUNT + 1))
        continue
    fi

    echo "" | tee -a "$MAIN_LOG"
    echo "----------------------------------------" | tee -a "$MAIN_LOG"
    echo "Running image: $IMAGE_PATH" | tee -a "$MAIN_LOG"
    echo "Output dir: $OUT_DIR" | tee -a "$MAIN_LOG"
    echo "Image log: $IMG_LOG" | tee -a "$MAIN_LOG"
    echo "Start: $(date)" | tee -a "$MAIN_LOG"
    echo "----------------------------------------" | tee -a "$MAIN_LOG"

    {
        echo "========================================"
        echo "Image: $IMAGE_PATH"
        echo "Output: $OUT_DIR"
        echo "Start time: $(date)"
        echo "CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
        echo "CPU threads: $CPU_THREADS"
        echo "Cellpose model: $MODEL_NAME"
        echo "========================================"
    } > "$IMG_LOG" 2>&1

    set +e

    python -m cellpose \
        --image_path "$IMAGE_PATH" \
        --pretrained_model "$MODEL_NAME" \
        --use_gpu \
        --save_tif \
        --savedir "$OUT_DIR" \
        --verbose >> "$IMG_LOG" 2>&1

    EXIT_CODE=$?

    set -e

    {
        echo "Exit code: $EXIT_CODE"
        echo "End time: $(date)"
        echo "========================================"
    } >> "$IMG_LOG" 2>&1

    if [ "$EXIT_CODE" -eq 0 ]; then
        touch "$DONE_FLAG"
        RUN_COUNT=$((RUN_COUNT + 1))
        echo "FINISHED: $IMAGE_PATH" | tee -a "$MAIN_LOG"
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "FAILED: $IMAGE_PATH" | tee -a "$MAIN_LOG"
        echo "Exit code: $EXIT_CODE" | tee -a "$MAIN_LOG"
        echo "Check log: $IMG_LOG" | tee -a "$MAIN_LOG"
        echo "---- Last 80 lines of image log ----" | tee -a "$MAIN_LOG"
        tail -n 80 "$IMG_LOG" | tee -a "$MAIN_LOG"
        echo "------------------------------------" | tee -a "$MAIN_LOG"
        echo "Continue to next image." | tee -a "$MAIN_LOG"
    fi
done

echo "" | tee -a "$MAIN_LOG"
echo "========================================" | tee -a "$MAIN_LOG"
echo "All Cellpose3-nuclei jobs finished." | tee -a "$MAIN_LOG"
echo "End time: $(date)" | tee -a "$MAIN_LOG"
echo "Run count: $RUN_COUNT" | tee -a "$MAIN_LOG"
echo "Skip count: $SKIP_COUNT" | tee -a "$MAIN_LOG"
echo "Fail count: $FAIL_COUNT" | tee -a "$MAIN_LOG"
echo "Main log: $MAIN_LOG" | tee -a "$MAIN_LOG"
echo "========================================" | tee -a "$MAIN_LOG"
