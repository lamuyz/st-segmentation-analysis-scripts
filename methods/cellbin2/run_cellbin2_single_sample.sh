```bash
#!/usr/bin/env bash
set -euo pipefail

# Example single-sample CellBin2 running script.
# Update paths and sample names before running.

BASE_DIR="/path/to/cellbin2/sample_name"
OUTPUT_DIR="${BASE_DIR}/output_default"

PYTHON_BIN="/path/to/miniconda3/envs/cellbin2/bin/python"
PIPELINE_PY="/path/to/cellbin2/tools/run_cellbin_pipeline_patched_signed_gem.py"

PARAMS_JSON="${PARAMS_JSON:-${OUTPUT_DIR}/sample_params.json}"
CHIP_NAME="sample_name"
LOG_FILE="${LOG_FILE:-${OUTPUT_DIR}/run_cellbin2.log}"

source "/path/to/cellbin2/tools/cellbin2_runtime_env.sh"

export OMP_NUM_THREADS=60
export OPENBLAS_NUM_THREADS=60
export MKL_NUM_THREADS=60
export NUMEXPR_NUM_THREADS=60
export VECLIB_MAXIMUM_THREADS=60
export CELLBIN2_ONNX_INTRA_OP_THREADS=60
export CELLBIN2_ONNX_INTER_OP_THREADS=1

mkdir -p "${OUTPUT_DIR}"

"${PYTHON_BIN}" "${PIPELINE_PY}" \
  -c "${CHIP_NAME}" \
  -p "${PARAMS_JSON}" \
  -o "${OUTPUT_DIR}" \
  -d \
  >> "${LOG_FILE}" 2>&1
```
