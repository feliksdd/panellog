#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p hardware/review_2026-11-09
kicad-cli version
kicad-cli sch erc --format json --severity-all --exit-code-violations -o hardware/review_2026-11-09/ERC.json hardware/kicad/panellog.kicad_sch
erc_rc=$?
cat hardware/review_2026-11-09/ERC.json
kicad-cli pcb drc --format json --severity-all --exit-code-violations --refill-zones --schematic-parity -o hardware/review_2026-11-09/DRC.json hardware/kicad/panellog.kicad_pcb
drc_rc=$?
cat hardware/review_2026-11-09/DRC.json
if (( erc_rc != 0 || drc_rc != 0 )); then exit 1; fi
