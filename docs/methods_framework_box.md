# Methods Framework Box

## State-space framing

For a subject and observation window, let latent physiological state be:

`x_t = {gas_exchange, input_response, inflammation_state, context}`

and observed signals be:

`y_t = {SpO2, EtCO2, perfusion_index, motion_score, CGM, meal_event, core_temperature, CRP}`

The minimal demo does not fit a physiological model. It implements a transparent
V0 dry-run estimator:

`state_t = f(y_t, events_t, quality_t)`

with explicit degradation and forbidden-output fields.

## Quality-gated update

1. Read synthetic observation rows.
2. Compute a window-quality score from sensor and context rules.
3. Emit state packets with confidence bounded by quality.
4. Add degradation labels when observations are weak or missing.
5. Add forbidden-output labels when a claim would exceed observability.
6. Validate that every packet contains events, quality and forbidden-output
   fields.

## Validation boundary

The demo is **V0 synthetic dry-run only**. Passing it demonstrates schema and
workflow plumbing, not measurement agreement, physiological validity,
individualized calibration, clinical utility or safety.
