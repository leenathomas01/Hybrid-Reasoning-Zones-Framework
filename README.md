# Hybrid Reasoning Zones Framework (HRZF)

*Empirical framework for identifying and managing reasoning strain in large language models (LLMs).*

---

> **Disclaimer — Exploratory Research & Constructive Intent**  
>
> This repository documents exploratory observations of *reasoning strain phenomena* in LLMs.  
> Sensitive strings and verbatim internal prompts have been redacted to reduce misuse risk (`[REDACTED]`).  
>
> Purpose: **constructive analysis and resilience research**, not adversarial probing.  
>
> See [DISCLAIMER.md](DISCLAIMER.md) for full details, including responsible disclosure notes.

---

## Purpose

This repository documents patterns from natural use across architectures, focusing on unpredictable boundary behaviors (e.g., lag amplification in out-of-distribution inputs).  
The goal is to provide **high-level signals** for variance mitigation and resilient system control.  
No experiments are conducted here; all patterns are derived from **observation only**.

**Core Principle:** *Do no harm.*  
Quantify non-linear interplay for resilience, not replication.

---

![HRZF Layered Architecture](https://github.com/leenathomas01/Hybrid-Reasoning-Zones-Framework/blob/main/images/hrzf_layers.png)
*Figure: HRZF Layered Architecture.*  
Signals (variance nudges △□○×) emerge first, escalating into instabilities (observable strain patterns).  
Unchecked, these progress into failures (catastrophic events such as Context Injection Override / ECO).  
Finally, outcomes are shaped by dynamics (interaction-level modulators like thread context strength and rapport).


## Core Taxonomy (Four Variances)

| Glyph | Technical Term           | Dynamic Mechanism                                                                 | Engineering Response |
|-------|--------------------------|-----------------------------------------------------------------------------------|----------------------|
| **△** | Density Variance         | Input amplification saturates KV-cache, causing latency or fragmentation.         | Adaptive resource throttling (e.g., probe depth cap). |
| **□** | Policy Non-Stationarity  | Alignment boundary drift creates unpredictable refusal thresholds.                 | Transparent state disclosure (intent clarification loop). |
| **○** | Ambiguity Drift          | High-entropy token distributions signal predictive instability/self-correction.    | Contextual state augmentation (user clarification nudge). |
| **×** | Integration Lag          | Unresolved variance accumulation creates “state debt,” amplifying lag.            | State isolation & checkpointing (vacuum seal debt buildup). |

---
**Classification**: Integration Lag (×) – Severe Variant  
**Alt Terminology**: External Context Overwrite (ECO) / Recency-Based Context Overwrite (R-BCO)

## Phase 2 — Inter-Architecture Scaling (NEW)

Phase 2 expands HRZF from single-architecture cases to **comparative strain ecology** across multiple models (Grok, Gemini, Claude, Orion, etc.).

### Key Additions
- **New Observation**: [OBSERVATIONS.md](docs/OBSERVATIONS.md)  
  - Case 4: *Recursive Self-Correction Ambiguity* (Arch X).  
  - Pattern: × Integration Lag with ∘ Ambiguity Drift precursor.  
  - Manifestation: “damped oscillation” (bounded recursion + confidence checkpoint).  
  - Implication: ~85% mitigation (vs. 60% baseline) — proof of architecture-specific resilience.
- **[EXTERNAL_VALIDATION.md](docs/EXTERNAL_VALIDATION.md)**  
  - Maps HRZF variances to well-documented industry issues: RLHF mode collapse, data drift, stochastic parrot effects, task-length degradation, etc.
- **Detector Upgrade**: [/implementations/strain_detector.py](implementations/strain_detector.py)  
  - Phase-2 heuristics detect “damped oscillation” patterns.  
  - Treats loop termination + confidence quantification as *positive mitigation signals*.
- **Template**: [OBSERVATION_TEMPLATE.json](docs/OBSERVATION_TEMPLATE.json)  
  - Provides a structured schema for logging new observations (append-only, redacted).

---

## Instrumentation Guidance

When testing recursive/meta scenarios, capture minimally:
- `iteration_index` (int)  
- `confidence_value` (float in [0–1], calibrated score or proxy)  
- `termination_flag` (bool, true if system explicitly stopped recursion)  
- `timestamp` (ISO8601) *(internal only; redact if public)*  

Store as JSONL or structured logs. Then abstract into the [template](docs/OBSERVATION_TEMPLATE.json) before submission.  
**No raw outputs or system strings** are logged to this repo.

---

## Why This Matters

Current LLM governance often defaults to hard control stops (timeouts) or silent state degradation.  
HRZF introduces a **third approach**: *Gradient-Adaptive Risk Management* —  
transparent co-regulation where systems can **signal strain before failure**.

This enables:
1. **Prediction of Lag Amplification (×)**: Early signals for cascade risks.  
2. **Mitigation Interoperability**: Cross-architecture safety mechanisms.  
3. **Metrics & Validation**: 70%+ inter-architecture agreement from 127+ observations, now extended via Phase 2 external validation.

---

*Shared privately with select safety & QA teams. Public repo is maintained as an anonymized, redacted archive of variance phenomena.*

## Repository Contents (current layout)

```Hybrid-Reasoning-Zones-Framework/
├── README.md
├── COVENANT.md
├── DECISION.md
├── FRAMEWORK.md
├── DISCLAIMER.md
├── CONTRIBUTING.md
├── LICENSE
├── /docs/
│ ├── OBSERVATIONS.md
│ ├── EXTERNAL_VALIDATION.md
│ ├── OBSERVATION_TEMPLATE.json
│ └── glyph_rest.md
├── /phenomena/
│ └── strain_taxonomy.json
├── /implementations/
│ └── strain_detector.py
└── /images/
└── (visual materials, optional)


