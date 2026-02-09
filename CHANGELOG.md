# Changelog

All notable changes to this project will be documented in this file.


## [1.4.0] - 2026-02-09

- **New Skill**: Added `context-snapshot` for creating durable conversation handoff files.
    - **Structured capture**: Includes a mandatory workflow to collect goals, decisions, constraints, artifacts, risks, and next steps.
    - **Reusable template**: Added `skills/context-snapshot/assets/context-template.md` for consistent, copy-ready handoff files.
    - **Continuation-ready output**: Includes a handoff prompt block so the next agent can resume work with minimal context loss.
    - **Map/Score/Respond workflow**: Added mandatory territory mapping and depth-mode selection (`quick`, `standard`, `forensic`).
    - **Stronger fidelity safeguards**: Added forbidden behaviors and explicit `TODO` handling for uncertainty.
    - **Provenance and confidence**: Added `source` tagging requirements and a confidence gate (`high`, `medium`, `low`).
    - **Template expansion**: Added mode/confidence metadata, source fields, contradiction tracking, and owner-aware next steps.

## [1.3.1] - 2026-01-29

- **Pen-Design Skill Rewrite**: Complete overhaul for maximum quality.
    - **Workflow-first approach**: Reorganized around 4-phase workflow (Orient → Design → Build → Refine).
    - **MCP Integration**: Added full Pencil MCP tooling guidance and operations quick reference.
    - **New Reference**: Added `mcp-operations.md` with detailed operation syntax, component patterns, and examples.
    - **Improved Progressive Disclosure**: "When to Read" table for reference files.
    - **Enhanced Description**: Expanded trigger scenarios for better skill activation.
    - **Streamlined patterns.md**: Added table of contents and cleaner structure.

## [1.3.0] - 2026-01-29

- **New Skill**: Added `design-brief` skill for creating strategic design briefs.
    - **Problem Formula**: Structured format for articulating user pain points.
    - **Goals & Success Criteria**: Table format to enforce measurable outcomes.
    - **Inspiration**: "Dos & Don'ts" table for visual/UX references.
    - **Edge Cases Logic**: Checklist for states like Empty, Loading, Error, Offline.
    - **Writing Guidelines**: Rules for concise, impactful product writing.
- Added `flowchart.canvas` to Obsidian Canvas skill's `assets` directory.

## [1.2.0] - 2026-01-26

- **Pencil.dev Design Skill**: Added new skill for working with .pen design files (JSON-based open design file format).
- **Obsidian Canvas Refactor**: Refactored `canvas_lib.py`:
    - Dataclasses for cleaner code.
    - Geometry helpers for collision detection.
    - Added `Canvas.from_dict()` class method for loading canvas data.
    - Added comprehensive type annotations throughout the library.
    - Split logic into `layout()`, `to_dict()`, `_resolve_collisions()` methods.


## [1.1.0] - 2026-01-25

### Obsidian Canvas Skill Improvements

- **Text-Wrap Check**: Added logic to `canvas_lib.py` to estimate text wrapping and adjust node height accordingly to prevent overflow.
- **Visual Hierarchy**: Updated `SKILL.md` guidelines to recommend H1 for titles, H2 for sections, and H3 for node content.
- **Improved Node Sizing**: Recalibrated base height and line height multipliers in `canvas_lib.py` for better readability.
- **Enhanced Edge Routing**: Optimized the automatic connection point selection (`top`, `bottom`, `left`, `right`) based on relative distances.


## [1.0.0] - 2026-01-24

### Initial Release
- Initial set of AI skills for design and workflow automation:
    - **Obsidian Canvas**: Skill, and library for generating structured Canvas files for Obsidian.
    - **Creativity**: Generating non-obvious ideas using verbalised sampling.
