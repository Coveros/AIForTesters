---
name: runtime-remediation
description: 'Use when you want live, controlled code edits during an AppSec demo: apply minimal hardening changes, validate outcomes, and provide rollback commands.'
argument-hint: 'Provide finding IDs, target files, and confirmation to run in apply mode'
user-invocable: true
---

# Runtime Remediation Skill

## When to use

Use for live demonstrations where Copilot should edit code during the session.

## Safety constraints

- Only apply edits after explicit user request.
- Keep changes minimal and scoped to confirmed findings.
- Do not perform destructive operations.
- Always include rollback commands.

## Procedure

1. Confirm findings and mapped controls.
2. Restate scope and apply minimal edit set.
3. Summarize all changed files and why they changed.
4. Run lightweight validation checks if available.
5. Report residual risk and rollback commands.

## Required output

- `mode`: apply
- `changed_files`: list
- `control_ids`: list
- `validation_summary`: text
- `rollback_commands`: list

## Rollback guidance

Prefer Git rollback commands for tracked files and clear manual restoration notes for untracked files.
