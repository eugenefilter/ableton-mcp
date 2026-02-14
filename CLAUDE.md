# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP (Model Context Protocol) server for controlling Ableton Live via AbletonOSC. Focused on AI-driven music generation (goa trance, psytrance, DNB, breaks). The project is in early development — follow `DEVELOPMENT_PLAN.md` for current progress and next steps.

## Target Architecture

```
src/ableton_mcp/
├── server/        # MCP server, tools, prompts
├── ableton/       # OSC client, track/clip/device/mixer/transport control
├── generators/    # AI generators: melody, harmony, rhythm, bass, arrangement
├── music/         # Music theory: scales, chords, patterns
├── styles/        # Genre plugins (goa_trance, psytrance, etc.)
├── utils/         # Config (pydantic), logger, MIDI utils, validators
└── exceptions.py
```

## Key Technical Decisions

- **Communication with Ableton:** via AbletonOSC (OSC protocol, python-osc library)
- **MCP SDK:** Python MCP SDK (`mcp` package)
- **Config:** Pydantic Settings with .env files
- **Music theory:** music21 library
- **Style system:** Plugin architecture — each genre is a StylePlugin subclass registered in StyleRegistry

## Code Standards

- **Language:** Python 3.10+
- **Type hints:** required on all functions
- **Docstrings:** Google style, in Russian where appropriate
- **Formatting:** black (line-length 100), isort (profile black)
- **Linting:** flake8 (max-line-length 100), mypy, pylint
- **Tests:** pytest + pytest-cov, target coverage >80%

## Development Workflow

- Follow steps in `DEVELOPMENT_PLAN.md` sequentially
- Each step must be discussed before implementation and tested after
- Git commits: Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`)
- Detailed requirements and code examples are in `INSTRUCTIONS.md`
- Stage-by-stage breakdown is in `DEVELOPMENT_STAGES.md`

## OSC Defaults

- Host: `127.0.0.1`
- Send port: `11000`
- Receive port: `11001`
- Default tempo: 140 BPM
- Default key/scale: A harmonic minor
