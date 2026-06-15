```bash
#!/usr/bin/env bash
set -euo pipefail

# Example queue script for running multiple CellBin2 samples sequentially.
# Update ROOT and sample script paths before running.

ROOT="/path/to/cellbin2"
QUEUE_LOG="${ROOT}/queue_cellbin2_$(date +%Y%m%d).log"

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "${QUEUE_LOG}"
}

log "queue start"

log "start sample_1"
bash "${ROOT}/sample_1/run_cellbin2_single_sample.sh"
log "finish sample_1"

log "start sample_2"
bash "${ROOT}/sample_2/run_cellbin2_single_sample.sh"
log "finish sample_2"

log "queue finished"
```
