# Public release manifest

Release name: `observability-first-digital-physiome`

Release date: 2026-07-13

Author: Xingshuo Dong

Zenodo concept DOI: `https://doi.org/10.5281/zenodo.20773419`

Release version: `0.1.1`

License: MIT License

## Included

- Minimal schemas required by the manuscript methods framework.
- Synthetic Tier 0 generator and validation summary.
- Synthetic eight-system generator and validation summary.
- Tier 1 form/import layer with sample CSV rows.
- Manifest-driven device CSV adapter and illustrative device-export rows.
- Dry-run validation endpoint definitions, sample anchors and output examples.
- Methods-box documentation and Supplementary Table S18 positioning table.
- Repository README, citation metadata and non-clinical-use boundary.

## Excluded

- Draft manuscripts and internal reviews.
- Zotero PDF extractions and full-text reading notes.
- Patent drafts and invention-disclosure materials.
- Ethics application drafts not required to run the code.
- Any real human participant data.
- Any browser/session/authentication material.
- Binary figure exports and submission PDFs.
- Large generated JSONL/CSV outputs that are reproducible from the included
  scripts, including full state-packet streams and synthetic-window tables.

## Minimal file-to-claim map

| Manuscript claim area | Public files |
|---|---|
| State-packet schema | `schemas/digital_human_state_packet_v0.1.schema.json` |
| Event ontology | `schemas/event_ontology_v0.1.csv` |
| Device-observation model | `schemas/device_observation_model_v0.1.csv` |
| Quality degradation | `schemas/sensor_quality_rules_v0.2.csv`; prototype validation summaries |
| Formal state-space framing | `schemas/formal_state_space_model_v0.1.csv`; `docs/formal_state_space_validation_framework.md` |
| Identifiability boundary | `schemas/identifiability_matrix_v0.1.csv` |
| Tier 0 synthetic workflow | `prototypes/digital_human_tier0/` |
| Eight-system linked workflow | `prototypes/digital_human_eight_system/` |
| Tier 1 import and CSV adapter | `prototypes/digital_human_real_import/` |
| Validation closure dry-run | `validation/`; `scripts/run_digital_human_real_validation.py` |
| Literature positioning table | `docs/table_s18_npj_digital_twin_positioning.csv` |

## Boundary statement

This release is a methods-framework companion package. It supports inspection of
workflow logic and reproducibility plumbing only. It is not evidence of a fitted
clinical model, individualized digital twin, validated physiology simulator or
clinical decision-support system.

The MIT License permits software reuse, but the package remains non-clinical:
it is not a medical device, diagnostic tool, treatment recommendation system,
patient-monitoring product or substitute for professional medical judgment.
