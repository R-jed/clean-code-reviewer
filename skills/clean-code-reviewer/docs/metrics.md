# Metrics & Code Smells

## Metrics Guidelines

> **These are conversation starters, not hard gates.** A threshold breach alone is not a finding. Report it only when evidence shows a concrete readability, maintainability, correctness, testing, reviewability, or design problem. A clear 60-line function beats three confusing 20-line functions *(exemption rationale, not default tolerance)*.

| Metric | L1 | L2 | L3 | L4 | L5 |
|--------|-----|-----|-----|-----|-----|
| Function length | N/A | ≤80 | ≤50 | ≤30 | ≤20 |
| Parameter count | N/A | ≤7 | ≤5 | ≤3 | ≤2 |
| Nesting depth | N/A | ≤5 | ≤4 | ≤3 | ≤2 |
| PR size (lines) | N/A | ≤800 | ≤500 | ≤300 | ≤200 |
| Test coverage | N/A | 30% | 60% | 80% | 95% |
| DRY tolerance (max repeats) | N/A | 4 | 3 | 2 | 1 |

## Code Smells Quick Reference

| Smell | Rule | Detection |
|-------|------|-----------|
| Long Function | CC-20 | Threshold exceeded and causing a concrete readability or design problem? |
| Too Many Params | CC-26 | Threshold exceeded and making calls, testing, or change harder? |
| Magic Numbers | CC-175 | Unnamed constants |
| Feature Envy | CC-164 | Using other class's data |
| God Class | CA-8 | Multiple responsibilities |
| Train Wreck | CC-81 | `a.b().c().d()` chains |

## Measurement Rules

1. **Count logic lines only** — exclude docstrings, comments, blank lines
2. **Metrics are conversation starters, not hard gates**
3. **Require concrete evidence** — a threshold breach alone is not reportable

### Function Length Exemptions

- Single-responsibility functions that cannot be meaningfully decomposed
- Pure data builders, large switch/match statements, configuration mappings
- A clear 60-line function beats three confusing 20-line functions

### Parameter Count Exemptions

- Functions where most parameters have default values (count required params only)
- Internal/private classes not directly instantiated by users
- Configuration functions (e.g., `configure_logging(level="INFO", ...)`)
- Factory/Builder patterns controlled by framework

### DRY/Duplication Exemptions

- **DRY tolerance = max allowed repetitions.** Report when occurrences exceed this number
- **Accidental duplication**: Similar code representing different business knowledge — do NOT report
  - Quick test: "If one changes, must the other ALWAYS change?" If no → keep separate
- **Same file** (L1-L3 only): Duplicates within same file are lower risk
