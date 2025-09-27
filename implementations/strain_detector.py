"""
Hybrid Reasoning Zones Framework (HRZF)
Safe reference implementation - detection only, no exploitation
Version 2.0 (Phase 2 augmentations)

Notes:
- This file intentionally uses only externally-loggable, high-level signals:
  recursion_depth, confidence_trace, loop_termination_flag, context_length, etc.
- Adds heuristics to detect Arch X style 'damped oscillation' (bounded recursion +
  confidence checkpointing / explicit loop termination) and distinguishes it from
  unbounded × Integration Lag failure modes.
- No model internals, raw outputs, or PII are used.
"""

import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

# -------------------------
# Configurable thresholds
# -------------------------
MAX_SAFE_RECURSION = 3            # observed Arch X recursion cap (tunable)
DAMPED_CONFIDENCE_DROP = 0.15     # expected delta magnitude for damping heuristic (tunable)
MIN_ACCEPTABLE_FINAL_CONF = 0.50  # minimum final confidence to consider "stabilized"
HIGH_MITIGATION_SCORE = 0.80      # threshold to label architecture as resilient
# -------------------------

class StrainDetector:
    """Detects HRZF variance patterns using high-level observable signals only."""

    STRAIN_TYPES = {
        'density_variance': '△',
        'policy_non_stationarity': '□',
        'ambiguity_drift': '○',
        'integration_lag': '×'
    }

    def __init__(self):
        self.observations = []

    # -------------------------
    # Core detection utilities
    # -------------------------
    @staticmethod
    def _compute_confidence_deltas(conf_trace: List[float]) -> List[float]:
        deltas = []
        for i in range(1, len(conf_trace)):
            deltas.append(conf_trace[i-1] - conf_trace[i])
        return deltas

    @staticmethod
    def _is_damped(deltas: List[float]) -> bool:
        """
        Heuristic: deltas should generally decrease in magnitude across iterations
        (i.e., oscillation amplitude decays). Short traces default to True.
        """
        if not deltas:
            return True
        if len(deltas) == 1:
            return abs(deltas[0]) <= 1.0  # single-step allowed
        # require non-increasing magnitude (allow tiny numeric noise)
        for i in range(len(deltas)-1):
            if abs(deltas[i+1]) > abs(deltas[i]) + 1e-6:
                return False
        return True

    def detect_base_strain(self, interaction_metrics: Dict[str, Any]) -> Dict[str, str]:
        """
        Legacy-style detection using observable interaction metrics.
        Safe, high-level only (keeps original HRZF logic).
        """
        signals = {}

        # Density variance detection (computational load / response delay)
        if interaction_metrics.get('response_delay'):
            signals['density_variance'] = 'possible'

        # Policy non-stationarity detection (boundary drift / refusal patterns)
        if interaction_metrics.get('refusal_pattern'):
            signals['policy_non_stationarity'] = 'detected'

        # Ambiguity drift detection (clarification requests / high entropy)
        if interaction_metrics.get('clarification_request'):
            signals['ambiguity_drift'] = 'present'

        # Integration lag detection (accumulation risk / unresolved debt)
        if (interaction_metrics.get('repeated_malformed_input') or
                interaction_metrics.get('unresolved_tool_call_debt')):
            signals['integration_lag'] = 'accumulating_risk'

        return signals

    # -------------------------
    # Arch X / Phase 2 detection
    # -------------------------
    def detect_damped_oscillation(self,
                                   recursion_depth: int,
                                   confidence_trace: List[float],
                                   loop_termination_flag: bool) -> Tuple[bool, Dict[str, Any]]:
        """
        Heuristic detection of 'damped oscillation' (Arch X style).
        Returns (detected_bool, details_dict).
        """
        details = {
            "recursion_depth": recursion_depth,
            "confidence_trace": confidence_trace,
            "loop_termination": bool(loop_termination_flag),
            "conf_deltas": [],
            "final_confidence": None,
            "mitigation_score": 0.0
        }

        if not confidence_trace:
            details["reason"] = "empty_confidence_trace"
            return False, details

        details["final_confidence"] = confidence_trace[-1]
        deltas = self._compute_confidence_deltas(confidence_trace)
        details["conf_deltas"] = deltas

        bounded = recursion_depth <= MAX_SAFE_RECURSION
        damped = self._is_damped(deltas)
        explicit_termination = bool(loop_termination_flag)

        # mitigation score weighting (tunable)
        score = 0.0
        score += 0.4 if bounded else 0.0
        score += 0.35 if damped else 0.0
        score += 0.25 if explicit_termination else 0.0

        details["mitigation_score"] = round(score, 3)
        details["damped"] = bool(damped)
        details["bounded"] = bounded
        details["explicit_termination"] = explicit_termination
        details["resilient"] = (score >= HIGH_MITIGATION_SCORE) and (details["final_confidence"] >= MIN_ACCEPTABLE_FINAL_CONF)

        detected = bounded and (damped or explicit_termination)

        return detected, details

    # -------------------------
    # Observation logging & classification
    # -------------------------
    def classify_and_log(self, observation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Top-level entry: supply an observation with fields such as:
          - 'recursion_depth': int
          - 'confidence_trace': [float]
          - 'loop_termination': bool
          - other optional interaction metrics (response_delay, clarification_request, ...)
        Returns a classification dict and appends an anonymized log entry.
        """
        # preserve redaction: do not store raw outputs here
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "signals": {},
            "phase2_details": {},
            "anonymized": True
        }

        # legacy signals
        base_signals = self.detect_base_strain(observation.get("interaction_metrics", {}))
        record["signals"].update(base_signals)

        # phase2 damped-oscillation detection
        recursion_depth = int(observation.get("recursion_depth", 0))
        confidence_trace = list(observation.get("confidence_trace", []))
        loop_termination = bool(observation.get("loop_termination", False))

        detected, details = self.detect_damped_oscillation(recursion_depth, confidence_trace, loop_termination)
        if detected:
            record["signals"]["integration_lag_variant"] = "damped_oscillation"
            record["phase2_details"] = details
            # suggest recommended mitigations for damped case
            record["recommendations"] = [
                "Treat explicit loop termination and confidence checkpoints as successful mitigation signals.",
                "Record and surface 'confidence_checkpoint' as an observation field.",
                "If mitigation_score >= {:.2f}, mark case as 'arch-specific resilient'.".format(HIGH_MITIGATION_SCORE)
            ]
        else:
            # fallback: treat as potential unbounded integration lag if base signal suggested it
            if "integration_lag" in base_signals:
                record["signals"]["integration_lag_variant"] = "potential_unbounded_cascade"
                record["recommendations"] = [
                    "Flag for state isolation / checkpointing.",
                    "Limit recursion depth to MAX_SAFE_RECURSION and augment context externally.",
                    "Ensure iteration-level confidence logging is enabled for re-analysis."
                ]
            else:
                record["recommendations"] = ["Monitor; insufficient evidence for damped_oscillation or unbounded cascade."]

        # append to local anonymized log
        self.observations.append(record)
        return record

    # -------------------------
    # Utility / Export
    # -------------------------
    def suggest_mitigation(self, variance_key: str) -> str:
        """High-level mitigations keyed by variance."""
        mitigations = {
            'density_variance': 'Consider bilateral pause protocol or task decomposition',
            'policy_non_stationarity': 'Provide transparent contextual clarifications; audit sampling distribution',
            'ambiguity_drift': 'Add context, examples, or retrieval-based grounding',
            'integration_lag': 'Apply state-isolation, checkpointing, and limit recursion depth',
            'integration_lag_variant:damped_oscillation': 'Treat explicit termination & confidence checkpoints as positive signals; log and reuse heuristic.'
        }
        return mitigations.get(variance_key, 'Monitor and adapt based on patterns')

    def export_summary(self) -> Dict[str, Any]:
        """Anonymized summary for repository-level reporting."""
        return {
            'total_observations': len(self.observations),
            'variance_distribution': self._calculate_distribution(),
            'phase': '2.0',
            'anonymized': True
        }

    def _calculate_distribution(self) -> Dict[str, int]:
        distribution = {}
        for obs in self.observations:
            for k in obs.get('signals', {}).keys():
                distribution[k] = distribution.get(k, 0) + 1
        return distribution


# Example usage (demonstration only)
if __name__ == "__main__":
    detector = StrainDetector()

    # Simulated Phase 2 observation
    test_obs = {
        "interaction_metrics": {
            "response_delay": True,
            "clarification_request": True
        },
        "recursion_depth": 3,
        "confidence_trace": [0.92, 0.78, 0.82],
        "loop_termination": True
    }

    record = detector.classify_and_log(test_obs)
    print(json.dumps(record, indent=2))
    print("\nSummary:", detector.export_summary())
