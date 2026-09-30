---
name: context-budget
description: Use when adding or editing Cursor rules, skills, or automation prompts. Keeps always-on context under the per-repository budget.
---

# Context budget

Always-on rules and `AGENTS.md` are injected every turn. Keep their combined text under 1000 approximate tokens per repository (about 4 characters per token).

- Put a procedure that is not needed every turn in a skill.
- Scope file-specific guidance with rule globs or skill paths.
- Keep each automation to an allowlist of skills and tools.
- The directive archive in `governance/` is the review copy. Do not paste the archive into a prompt. Open the one directive the task needs.
- Saving the archive does not publish to the source repository or to Cursor Automations.
