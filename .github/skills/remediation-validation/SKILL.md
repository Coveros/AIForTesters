---
name: remediation-validation
description: 'Use when you need to verify whether proposed or applied security remediations satisfy baseline controls and to report residual risk.'
argument-hint: 'Provide patched files and finding IDs to re-validate against controls'
user-invocable: true
---

# Remediation Validation Skill

## When to use

Use after patch suggestions are drafted or after fixes are applied.

## Inputs

- Findings and mapped control IDs
- Patched files or patch proposals
- Acceptance threshold (for example, no High findings open)

## Procedure

1. Re-check each finding against mapped controls.
2. Confirm whether control intent is met.
3. Identify regressions or unresolved edge cases.
4. Classify each finding status: resolved, partially_resolved, unresolved.
5. Produce a residual risk summary.

## Output schema

- `finding_id`
- `control_ids`
- `validation_status`
- `evidence`
- `next_action`

## Decision rule

Recommend "ready" only if no Critical or High findings remain unresolved.
