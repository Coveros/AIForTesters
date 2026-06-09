---
description: "Use when performing application security analysis, vulnerability triage, or remediation planning in this repository. Includes evidence rules and standard mapping."
applyTo: ["app/**/*.py", "static/js/**/*.js", "templates/**/*.html", "docs/**/*.md"]
---

# AppSec Demo Workflow Instructions

## Scope

Apply these rules when analyzing security posture or generating remediation guidance.

## Invocation best practice

- Prefer explicit agent selection over implicit name matching.
- Prefer explicit skill invocation over passive inference.
- For suggestion-only steps, keep Copilot chat in Ask mode.
- For runtime edit application or auto-generated diffs, switch chat mode to Agent (or your custom agent mode in clients that separate mode and agent picker).
- In demos, use:
	- `AppSec Triage Agent` + `/vulnerability-discovery` for discovery.
	- `Remediation Coach Agent` + `/secure-patch-suggestion` for suggestion mode.
	- `Remediation Coach Agent` + `/runtime-remediation` for apply mode.
	- `Remediation Coach Agent` + `/remediation-validation` for re-validation.

## Findings format

For each finding, include:

- Title
- Severity: Critical | High | Medium | Low
- Evidence: exact file path and concise technical rationale
- Standard mapping: one or more control IDs from `docs/appsec-demo/appsec-baseline-standard.md`
- Remediation summary
- Validation checklist

## Analysis priorities

1. Input and prompt injection controls
2. Output encoding and rendering safety (XSS)
3. Authentication and authorization for sensitive actions
4. Error handling and sensitive data leakage
5. Configuration hardening (CORS, debug mode, rate limiting)

## Remediation style

- Prefer minimal edits with clear rollback path.
- Avoid broad refactors in demo outputs.
- Include risk tradeoffs if a recommendation changes behavior.
- In live demos, narrate mode switches out loud so the audience can distinguish planning mode (Ask) from change mode (Agent).

## Evidence rule

If there is not enough evidence in the code, mark the item as "Needs verification" instead of asserting a confirmed vulnerability.
