# Observability-first digital physiome framework

Minimal public companion package for the manuscript:

> An observability-first digital physiome framework for clinical digital twins

This repository provides a compact, review-oriented demonstration of the
manuscript's core methods-framework idea: clinical digital twins should begin
from observable state packets, event logs, sensor-quality degradation and
forbidden-output boundaries before claiming individualized physiological
simulation.

## Included

- `demo/minimal_observability_demo.py`: a standard-library Python demo that
  converts synthetic observation windows into state packets.
- `demo/sample_observations.csv`: fictional sample rows for V0 dry-run only.
- `schemas/state_packet_minimal.schema.json`: minimal state-packet schema.
- `schemas/quality_rules_minimal.csv`: quality-gate and forbidden-output rules.
- `docs/methods_framework_box.md`: concise methods box.
- `CITATION.cff`, `LICENSE.md` and this README.

## Quick Start

```bash
python3 demo/minimal_observability_demo.py
```

The script writes:

- `demo/outputs/state_packets.jsonl`
- `demo/outputs/validation_summary.md`

## Boundary

No real participant data are included. All rows are synthetic or illustrative.
This repository is not a fitted physiological model, not a validated digital
twin, not a medical device, not a diagnostic tool and not a treatment-support
system.

Passing the demo only means that the minimal state-packet, event, quality-gate
and validation-summary workflow runs on synthetic rows. It does not establish
measurement agreement, physiological validity, individualized calibration,
clinical utility, regulatory readiness or safety.

## Citation

Please cite the accompanying manuscript or use the metadata in `CITATION.cff`.
