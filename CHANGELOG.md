# Changelog

All notable changes to this project will be documented in this file.

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
