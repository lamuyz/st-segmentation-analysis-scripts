```bash
#!/usr/bin/env bash
set -euo pipefail

# Example queue script that waits for an existing process to finish
# before starting additional CellBin2 samples.

WAIT_PID="${1:-}"
QUEUE_LOG="${2:-/path/to/cellbin2/queue_after_pid.log}"

if [[ -z "${WAIT_PID}" ]]; then
  echo "usage: $0 <wait_pid> [queue_log]" >&2
  exit 1
fi

echo "[$(date -u '+%F %T')] queue start, waiting for PID ${WAIT_PID}" >> "${QUEUE_LOG}"

while kill -0 "${WAIT_PID}" 2>/dev/null; do
  sleep 30
done

echo "[$(date -u '+%F %T')] PID ${WAIT_PID} finished, starting queued samples" >> "${QUEUE_LOG}"

run_sample() {
  local name="$1"
  local script_path="$2"

  echo "[$(date -u '+%F %T')] start ${name}" >> "${QUEUE_LOG}"
  bash "${script_path}"
  echo "[$(date -u '+%F %T')] finish ${name}" >> "${QUEUE_LOG}"
}

run_sample "sample_1" "/path/to/cellbin2/sample_1/run_cellbin2_single_sample.sh"
run_sample "sample_2" "/path/to/cellbin2/sample_2/run_cellbin2_single_sample.sh"
run_sample "sample_3" "/path/to/cellbin2/sample_3/run_cellbin2_single_sample.sh"

echo "[$(date -u '+%F %T')] queue finished" >> "${QUEUE_LOG}"
```
