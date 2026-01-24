# alt-shift studio skills

This is a collection of agentic skills we've created for use on our Product & Design projects. We're sharing them publicly under the MIT license. We've designed these skills to be lightweight, and useful. They are easy on tokens, yet highly capable.

## Quick Start

1.  **Clone the repository**:
Download or clone this repository:
```bash<>
    git clone https://github.com/alt-shift-studio/skills.git
```

2.  **Install a Skill**:
Copy the desired skills from `/skills` folder into your agent's skills directory (global, or workspace-specific).
    
| Agent | Global Path | Workspace Path |  |
| :--- | :--- | :--- | :--- |
| **Google Antigravity** | `~/.gemini/antigravity/global_skills/` | `./.agent/skills/` | [Docs](https://antigravity.google/docs/skills) |
| **Claude Code** | `~/.claude/skills` | `./.claude/skills` | [Docs](https://code.claude.com/docs/en/skills) |
| **Codex** | `~/.codex/skills` | `./.codex/skills` | [Docs](https://developers.openai.com/codex/skills/) |

## Available Skills

| Skill | Description |
| :--- | :--- |
| [**Creativity**](./skills/creativity/SKILL.md) | Generates non-obvious ideas using Verbalized Sampling (VS-CoT). Best for qucikly generating diverse ideas. |
| [**Obsidian Canvas**](./skills/obsidian-canvas/SKILL.md) | Create and edit JSON Canvas files (`.canvas`) used in Obsidian. Uses custom Pythin CLI to avoid collisions and weird layouts. |