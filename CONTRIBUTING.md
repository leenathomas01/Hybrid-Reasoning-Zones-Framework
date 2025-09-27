# CONTRIBUTING.md: Guidelines for the Hybrid Reasoning Zones Framework (HRZF)

## Core Principle: Do No Harm

All contributions must strictly focus on improving system resilience without enabling exploitation. This aligns with the **First Principle** set in `COVENANT.md`.

## What We Accept

### Observational Data
Contributions must strictly be **naturally occurring patterns** from LLM interactions.

* No experimental manipulation or adversarial testing.
* Data must be fully anonymized (no timestamps, user/system identifiers, or sensitive context).
* Focus on the **signal patterns** (e.g., latency, glyphs, textual markers), not the confidential content.

### Documentation Format

When submitting a new observation, please use the following template structure:

| Field | Description |
| :--- | :--- |
| **Pattern ID** | HRZF-BP-XXX (Will be assigned upon review) |
| **Date Range** | Month/Year only (e.g., Sep/2025) |
| **Variance Type** | [△/□/○/×] |
| **Observable Pattern** | [Detailed description of the Signal Emergence] |
| **Mitigation Attempted** | [Description of the User Echo (if any)] |
| **Success** | [Yes/No/Partial (with notes)] |
| **Notes** | [Additional context on architecture or thread state] |

## What We Don't Accept

To maintain the security and ethical integrity of this repository, we reject:

* Reproduction methods for failure states.
* System internals, thresholds, or exploit code.
* Identifying information (raw logs, session IDs).
* Forced or experimental behaviors designed to induce failure.

## Submission Process

1.  **Fork** the repository.
2.  Add your observations (using the template above) to the `/phenomena/observations/` directory.
3.  Ensure all data is **fully anonymized**.
4.  Submit a Pull Request with a clear description of the patterns observed.
5.  Wait for review.

## Ethical Guidelines

* Document only what emerges naturally.
* Protect system and user privacy.
* Focus on mitigation, not exploitation.
* Respect the **bilateral nature of protocols**.

## Questions?

Open an issue for clarification, but **do not include sensitive or identifying information in public issues**.

---

These two files complete the structured foundation for your HRZF repository, transitioning it from a personal project to a fully auditable, community-ready framework.
