# alt-shift studio skills

This is a collection of agent skills we've created for use on our Product & Design projects. We're sharing them publicly under the MIT license. We've designed these skills to be lightweight, and useful. They are easy on tokens, yet highly capable.

## Install skills

### 1. **Recommended**: Add via CLI
The fastest way to install our skills into your agent's global or workspace directory:
```bash
npx skills add altshiftstudio/skills
```

### 2. Manual Installation
If you prefer to do it manually:

1. Download or clone the repository via
    ```bash
    git clone https://github.com/altshiftstudio/skills.git
    ```
2. Copy desired skills from this repository into your agent's skills directory (global, or workspace-specific).
    
    | Agent | Global Path | Workspace Path |  |
    | :--- | :--- | :--- | :--- |
    | **Google Antigravity** | `~/.gemini/antigravity/global_skills/` | `./.agent/skills/` | [Docs](https://antigravity.google/docs/skills) |
    | **Claude Code** | `~/.claude/skills` | `./.claude/skills` | [Docs](https://code.claude.com/docs/en/skills) |
    | **Codex** | `~/.codex/skills` | `./.codex/skills` | [Docs](https://developers.openai.com/codex/skills/) |

## Available Skills

| Skill | Description |
| :--- | :--- |
| [**Creativity**](./skills/creativity/SKILL.md) | Generates non-obvious ideas using Verbalized Sampling (VS-CoT). Best for qucikly generating diverse ideas. |
| [**Design Brief**](./skills/design-brief/SKILL.md) | Create strategic design briefs that empower designers. Includes problem formula, success criteria, and edge cases logic. |
| [**Obsidian Canvas**](./skills/obsidian-canvas/SKILL.md) | Create and edit JSON Canvas files (`.canvas`) used in Obsidian. Uses custom Pythin CLI to avoid collisions and weird layouts. |
| [**Pen Design**](./skills/pen-design/SKILL.md) | Guide for working with Pencil (`.pen`) design files. Reading, creating, or modifying UI layouts, typography, or styling. |