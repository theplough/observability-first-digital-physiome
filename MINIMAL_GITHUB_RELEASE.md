# Minimal GitHub release scope

This file records the subset selected for direct GitHub publication when local
Git push is unavailable.

Repository:

`https://github.com/theplough/observability-first-digital-physiome`

The public repository should contain only the smallest review-useful materials:

- `README.md`
- `LICENSE.md`
- `CITATION.cff`
- `demo/minimal_observability_demo.py`
- `demo/sample_observations.csv`
- `schemas/state_packet_minimal.schema.json`
- `schemas/quality_rules_minimal.csv`
- `docs/methods_framework_box.md`

Large generated outputs and full internal prototype trees are intentionally not
uploaded. The demo regenerates compact JSONL packets and a validation summary
locally.
