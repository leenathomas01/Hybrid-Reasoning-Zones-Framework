# EXTERNAL_VALIDATION.md — HRZF Relevance Index

Documenting mappings between the HRZF Variance Taxonomy (△, □, ○, ×) and observed industry phenomena from open sources. This file serves as a relevance index connecting HRZF concepts to documented LLM/production behaviors and research findings.

## Core Principle
HRZF patterns (△ Density Variance, □ Policy Non-Stationarity, ○ Ambiguity Drift, × Integration Lag) map to widely observed LLM failure / stress modes (mode collapse, data drift, hallucination, recursive cascade). This document records exemplar mappings and suggested implications for Phase 2 validation.

### Table: External Pattern Mapping

| Source / Phenomenon | HRZF Variance | Key Implication |
| :--- | :--- | :--- |
| **RLHF Mode Collapse** (Rohan Paul / community threads) | Integration Lag (×) | Accumulated variance from training updates may push models toward low-diversity attractor states. Validate by comparing pre/post-RLHF diversity metrics across architectures. |
| **On-Policy vs. Offline Sampling** (Nathan Lambert / posts) | Policy Non-Stationarity (□) | Fine-tuning sampling schemes shift policy manifolds; stale or biased sampling leads to boundary drift. Test mitigation (Contextual Clarification) under diverse fine-tuning regimes. |
| **Data Drift / RAG Noise** (Hamel Husain / engineering notes) | Ambiguity Drift (○) | Domain shifts and noisy retrieval lead to predictive uncertainty. Add drift-detection to strain_detector and include RAG provenance checks as augmentation. |
| **Adaptive Recurrence / LHRMs** (research papers) | Density Variance (△) | Recurrence and repeated latent iteration raises KV/cache pressure on context handling. Bilateral Pause Protocols can reduce KV saturation. |
| **Task Length / Complexity Drop** (Daniel Kaiser / analyses) | Integration Lag (×) | Cascade risk increases with task length; early △/○ detection recommended to preempt × escalation. |
| **Stochastic Parrot / Hallucination Analyses** (various) | Ambiguity Drift (○) + Policy Non-Stationarity (□) | Hallucinations arise from ungrounded probabilistic chains; RAG or stronger contextual augmentation mitigates. |
| **g-factor Observations (LLM performance correlations)** (community & exploratory analyses) | Composite / Overall | Suggests a unified "g-strain" composite metric could capture dominant variance across tasks. Use as a diagnostic baseline for inter-architecture comparisons. |

## Suggested Use
- Add this file to `/docs/` or repo root for quick reference during audits.  
- Use as the canonical mapping when filing new OBSERVATIONS entries (linking external evidence to internal cases).  
- Use citations in the repo to link each row to saved post/article/paper snapshots (auditability).

## Next Steps (Phase 2)
1. Use the table to prioritize inter-architecture tests that replicate mapped phenomena (e.g., RLHF-induced × experiments; RAG noise → ○ drift tests).  
2. Expand table rows as new literature / posts are curated. Keep snapshots or DOI/URL references in a separate `/evidence/` folder.  
3. Consider deriving a composite "g-strain" metric (weighted combination of △/□/○/× features) and benchmark across models (Grok, Gemini, Claude, ChatGPT).
