---
name: create-skill
user-invocable: true
description: "Create or update a workspace skill definition (SKILL.md) for programming workflows by identifying scope, clarifying requirements, and validating the final skill file."
---

# Create Skill

## When to use

Use this skill when you need a reusable agent workflow for creating or refining VS Code skill definitions in this workspace.

This skill is appropriate when the request is:
- "Create a SKILL.md for this task"
- "Help me package a multi-step workflow into a skill"
- "Generate a workspace skill that guides future skill authors"

## What it does

1. Determines the desired outcome and scope (workspace or personal).
2. Identifies whether a skill is the right primitive vs prompt, instruction, or custom agent.
3. Collects the workflow steps, decision points, and quality criteria.
4. Drafts a `SKILL.md` file with frontmatter, structure, and example prompts.
5. Verifies the resulting skill file for correct YAML frontmatter and useful description.

## Recommended workflow

- Ask the user: "What outcome should this skill produce?" and "Should it be workspace-scoped or personal?"
- If no clear workflow exists, ask whether the skill should be:
  - a quick checklist for a common task
  - a full multi-step workflow with validation
- Draft the skill around the user-defined goal.
- Save the file under `.github/skills/<skill-name>/SKILL.md` for workspace sharing.
- Confirm the file location and verify the `description` is clear and actionable.

## Quality criteria

A good skill should include:
- `name` that matches the folder and is stable
- `user-invocable: true` for workspace skills that should appear in chat
- a clear `description` with trigger phrases and use cases
- a step-by-step process with decision logic
- examples of how to invoke the skill
- validation guidance for the created file

## Example prompts

- "Create a skill for converting a bug report into a test plan."
- "Draft a `SKILL.md` to help me build database migration instructions."
- "Help me package my multi-step feature design workflow as a workspace skill."

## Notes

- Prefer `SKILL.md` for reusable, multi-step workflows with explicit outcomes.
- Use prompts for narrow tasks, and instructions for always-on guidance.
- If the workflow requires isolated tool restrictions or separate stages, consider a custom agent instead.
