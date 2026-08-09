# Review Foundation and Authority Model

This document defines how Clean Code Reviewer turns source principles into reportable findings. It describes the review system's authority model; it is not another checklist.

## Foundation Layers

```text
Clean Code                Clean Architecture                The Pragmatic Programmer
    \                            |                                  /
     +-------------------- Source rule catalogs ------------------+
                                |
                    Principle conflict mediation
                    (principles-spectrum.md)
                                |
                    Language/paradigm applicability
                    (language-adjustments.md)
                                |
                    Project strictness calibration
                         (positioning.md)
                                |
                    Executable review contract
                            (SKILL.md)
                                |
                    Evidence-backed findings
                                |
                 Severity / Effort / Benefit / Verdict
```

The source-numbering spaces total 350 IDs: 202 Clean Code, 48 Clean Architecture, and 100 Pragmatic Programmer. Clean Code rules CC-64 through CC-77 are formatting rules intentionally delegated to automated tooling, leaving 336 active human-review rules.

## Authority by Concern

Each file owns one concern. Convenience documents may summarize an authority, but they must not redefine it.

| Concern | Authority | Responsibility |
|---------|-----------|----------------|
| Review workflow, reportability, severity, report format, verdict | `SKILL.md` | Executable review contract |
| Level mapping and strictness thresholds | `positioning.md` | L1-L5 calibration |
| Language/paradigm applicability | `language-adjustments.md` | Language- and paradigm-specific adjustment |
| DRY/YAGNI/abstraction timing and heuristic conflicts | `principles-spectrum.md` | Competing heuristic resolution |
| CC rule identity and review point | `clean-code.md` | Clean Code rule catalog |
| CA rule identity and review point | `clean-architecture.md` | Clean Architecture rule catalog |
| PP rule identity and review point | `pragmatic-programmer.md` | Pragmatic Programmer rule catalog |
| Symptom discovery and principle definitions | `quick-lookup.md`, `principles-glossary.md` | Indexes only |
| Human-facing feature and metric explanation | `docs/` | Documentation only |

When two files disagree, resolve the disagreement according to the concern they govern. For example, `SKILL.md` owns verdict behavior, while a source catalog owns the meaning of a CC/CA/PP rule code.

## Finding Decision Pipeline

A reportable finding must survive every applicable step:

1. **Observe evidence.** Identify a concrete implementation fact. For correctness, security, data-loss, or state-consistency concerns, trace the actual execution path.
2. **Check applicability.** Apply language and paradigm adjustments before treating a source rule as relevant.
3. **Calibrate context.** Apply the selected L1-L5 level and explicit exemptions.
4. **Resolve heuristic conflicts.** Use the principle spectrum when DRY, YAGNI, AHA, WET, KISS, or future-proofing pull in different directions.
5. **Establish impact.** Explain the concrete correctness, safety, readability, maintainability, testing, reviewability, or design harm. A threshold, smell label, or citation alone is insufficient.
6. **Verify the rule mapping.** Use the catalog that owns the cited CC/CA/PP code.
7. **Classify and conclude.** Apply severity, Effort/Benefit, and verdict rules from `SKILL.md`.

```text
Evidence + Applicability + Context + Concrete Impact + Valid Rule Mapping
                                |
                                v
                         Reportable Finding
```

## Non-Negotiable Properties

- **Evidence before labels.** A smell name is a search hint, not proof.
- **Behavior before metrics.** Thresholds trigger investigation; they do not independently create findings.
- **Context before dogma.** L1-L5 calibration changes tolerance without changing factual correctness.
- **Language before pattern matching.** OOP guidance must not be forced onto paradigms where it is non-idiomatic.
- **Rules support judgment.** Rule IDs explain and trace a finding; they are not a quota for generating findings.
- **Indexes do not own policy.** Quick lookups and feature docs can aid discovery without becoming a second execution contract.

## Change Discipline

When review behavior changes:

1. Update the file that owns the decision first.
2. Update summaries or indexes that repeat that decision.
3. Run repository integrity tests and both skill validators.
4. Review the diff for contradictions with this authority model.

Explanatory documentation must not silently alter executable review behavior.
