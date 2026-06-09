---
name: secure-patch-suggestion
description: 'Use when you need targeted security patch suggestions or controlled patch application from confirmed findings, including minimal diffs, validation checks, and rollback notes.'
argument-hint: 'Provide finding IDs and files to patch and say suggestion mode or apply mode'
user-invocable: true
---

# Secure Patch Suggestion Skill

## When to use

Use after findings are confirmed.

Modes:

- Suggestion mode: produce diffs/snippets only.
- Apply mode: make reversible runtime edits when explicitly requested.

## Inputs

- Confirmed finding IDs
- Target files
- Constraints (minimal edits, no behavior change where possible)

## Procedure

1. Restate the risk and objective.
2. Propose the smallest viable code change.
3. In suggestion mode, provide diff-style patch suggestion.
4. In apply mode, apply minimal edits and record changed files.
5. Explain side effects and compatibility concerns.
6. Provide validation and rollback checklist.

## Patch quality rules

- Keep each patch scoped to one risk.
- Avoid unrelated refactors.
- Note if additional tests are required.
- In apply mode, include explicit rollback commands.

## Output sections

1. Objective
2. Suggested or applied patch
3. Validation checklist
4. Residual risk
5. Rollback plan
