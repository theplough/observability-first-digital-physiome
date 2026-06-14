#!/usr/bin/env python3
"""Minimal observability-first digital physiome demonstration.

This script is a review-oriented companion for the manuscript:

An observability-first digital physiome framework for clinical digital twins

It demonstrates four framework ideas only:

1. state packets;
2. event-aware observation windows;
3. quality degradation and forbidden-output gates;
4. V0 dry-run validation closure.

It uses synthetic/sample rows only. It is not a fitted physiological model, not
a medical device, not a clinical decision-support system and not a validated
digital twin.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PATH = ROOT / "demo" / "sample_observations.csv"
OUTPUT_DIR = ROOT / "demo" / "outputs"


def to_float(value: Any, default: float = math.nan) -> float:
    text = str(value or "").strip()
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def signal(row: dict[str, str], key: str, unit: str) -> dict[str, Any]:
    value = to_float(row.get(key))
    return {
        "signal_id": key,
        "value": None if math.isnan(value) else value,
        "unit": unit,
        "quality": to_float(row.get(f"{key}_quality"), 1.0),
    }


def quality_gate(row: dict[str, str]) -> tuple[float, list[str], list[str]]:
    """Return window quality, degradation labels and forbidden outputs."""

    degradations: list[str] = []
    forbidden: list[str] = []

    perfusion_index = to_float(row.get("perfusion_index"), 2.5)
    motion_score = to_float(row.get("motion_score"), 0.0)
    etco2 = to_float(row.get("etco2_mmhg"))
    meal_carb = to_float(row.get("meal_carb_g"))
    crp = to_float(row.get("crp_mg_l"))

    quality = 1.0
    if perfusion_index < 0.6:
        quality -= 0.25
        degradations.append("degrade_ppg_spo2_low_perfusion")
        forbidden.append("oxygen_delivery_sufficiency_from_spo2_alone")
    if motion_score > 0.55:
        quality -= 0.20
        degradations.append("degrade_motion_sensitive_wearable_signals")
    if math.isnan(etco2):
        quality -= 0.15
        degradations.append("degrade_gas_exchange_without_co2_observation")
        forbidden.append("ventilation_state_without_co2_or_anchor")
    if math.isnan(meal_carb):
        quality -= 0.10
        degradations.append("degrade_glucose_interpretation_without_meal_event")
        forbidden.append("insulin_action_claim_without_input_context")
    if math.isnan(crp):
        quality -= 0.10
        degradations.append("inflammation_proxy_without_recent_lab_anchor")
        forbidden.append("infection_diagnosis_from_vitals")

    return max(0.0, round(quality, 3)), degradations, sorted(set(forbidden))


def estimate_states(row: dict[str, str], quality: float) -> dict[str, dict[str, Any]]:
    """A transparent rule-based estimator used only for dry-run plumbing."""

    spo2 = to_float(row.get("spo2_pct"))
    etco2 = to_float(row.get("etco2_mmhg"))
    cgm = to_float(row.get("cgm_mg_dl"))
    meal_carb = to_float(row.get("meal_carb_g"))
    core_temp = to_float(row.get("core_temp_c"))
    crp = to_float(row.get("crp_mg_l"))

    if not math.isnan(etco2) and etco2 > 48:
        gas_state = "co2_retention_proxy"
    elif not math.isnan(spo2) and spo2 < 93:
        gas_state = "oxygenation_deficit_or_artifact"
    else:
        gas_state = "normal_gas_exchange_proxy"

    if not math.isnan(cgm) and not math.isnan(meal_carb) and meal_carb > 0 and cgm > 140:
        input_state = "postprandial_glucose_rise_proxy"
    elif math.isnan(meal_carb):
        input_state = "input_context_missing"
    else:
        input_state = "resting_or_fasting_input_proxy"

    if not math.isnan(core_temp) and core_temp >= 38.0 and not math.isnan(crp) and crp > 10:
        inflammation_state = "inflammatory_fever_proxy"
    elif math.isnan(crp):
        inflammation_state = "thermal_vital_proxy_only"
    else:
        inflammation_state = "no_inflammatory_signal_proxy"

    return {
        "gas_exchange_packet": {
            "state": gas_state,
            "confidence": round(0.35 + 0.55 * quality, 3),
        },
        "input_packet": {
            "state": input_state,
            "confidence": round(0.30 + 0.55 * quality, 3),
        },
        "inflammation_packet": {
            "state": inflammation_state,
            "confidence": round(0.25 + 0.55 * quality, 3),
        },
    }


def make_packet(row: dict[str, str]) -> dict[str, Any]:
    quality, degradations, forbidden = quality_gate(row)
    return {
        "packet_id": f"minimal-{row['subject_id']}-{row['window_id']}",
        "framework_version": "minimal_v0.1",
        "validation_level": "V0_synthetic_dry_run",
        "subject_context": {
            "subject_id": row["subject_id"],
            "population_boundary": "synthetic_or_template_row_only",
        },
        "event_log": [
            event.strip()
            for event in row.get("events", "").split(";")
            if event.strip()
        ],
        "observed_signal_frame": [
            signal(row, "spo2_pct", "%"),
            signal(row, "etco2_mmhg", "mmHg"),
            signal(row, "perfusion_index", "index"),
            signal(row, "motion_score", "0-1"),
            signal(row, "cgm_mg_dl", "mg/dL"),
            signal(row, "meal_carb_g", "g"),
            signal(row, "core_temp_c", "degC"),
            signal(row, "crp_mg_l", "mg/L"),
        ],
        "state_packets": estimate_states(row, quality),
        "quality": {
            "window_quality": quality,
            "degradations": degradations,
            "forbidden_outputs": forbidden,
        },
        "claim_boundary": (
            "Demonstrates data plumbing only; does not establish physiological "
            "validity, individual calibration, clinical utility or safety."
        ),
    }


def validate(packets: list[dict[str, Any]]) -> dict[str, Any]:
    missing_quality = [p["packet_id"] for p in packets if "quality" not in p]
    missing_events = [p["packet_id"] for p in packets if "event_log" not in p]
    missing_forbidden = [
        p["packet_id"]
        for p in packets
        if "forbidden_outputs" not in p.get("quality", {})
    ]
    mean_quality = mean(p["quality"]["window_quality"] for p in packets)
    return {
        "packets": len(packets),
        "mean_quality": round(mean_quality, 3),
        "missing_quality_blocks": missing_quality,
        "missing_event_logs": missing_events,
        "missing_forbidden_output_fields": missing_forbidden,
        "status": "PASS" if not (missing_quality or missing_events or missing_forbidden) else "FAIL",
    }


def write_outputs(packets: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUTPUT_DIR / "state_packets.jsonl").open("w", encoding="utf-8") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n")
    lines = [
        "# Minimal Observability Demo Validation Summary",
        "",
        "This is a V0 synthetic dry-run only.",
        "",
        f"- Packets: {summary['packets']}",
        f"- Mean quality: {summary['mean_quality']}",
        f"- Missing quality blocks: {len(summary['missing_quality_blocks'])}",
        f"- Missing event logs: {len(summary['missing_event_logs'])}",
        f"- Missing forbidden-output fields: {len(summary['missing_forbidden_output_fields'])}",
        f"- Overall status: {summary['status']}",
        "",
        "Passing this check only means that the minimal state-packet and quality",
        "gate workflow runs on synthetic rows. It is not clinical validation.",
        "",
    ]
    (OUTPUT_DIR / "validation_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = read_rows(SAMPLE_PATH)
    packets = [make_packet(row) for row in rows]
    summary = validate(packets)
    write_outputs(packets, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if summary["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
