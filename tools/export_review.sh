#!/usr/bin/env bash
# Review exports only. No manufacturing release is implied.
set -euo pipefail
cd "$(dirname "$0")/.."
out=hardware/final_review_2026-11-09
mkdir -p "$out/pcb" "$out/schematic"
git rev-parse HEAD > "$out/source_commit.txt"
sha256sum hardware/kicad/panellog.kicad_{sch,pcb,pro,dru} > "$out/source_sha256.txt"
kicad-cli sch export pdf -o "$out/schematic/panellog.pdf" hardware/kicad/panellog.kicad_sch
kicad-cli sch export netlist --format kicadxml -o "$out/schematic/panellog.xml" hardware/kicad/panellog.kicad_sch
kicad-cli pcb export svg --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,F.Mask,F.SilkS,F.Fab --common-layers Edge.Cuts --mode-multi --fit-page-to-board --exclude-drawing-sheet -o "$out/pcb/" hardware/kicad/panellog.kicad_pcb
