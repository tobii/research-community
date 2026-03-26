# Contributing Guide

Thank you for your interest in contributing to the Tobii Research Tools Catalogue.

This repository is a structured catalogue of tools compatible with Tobii Pro research-grade eye trackers and software. Contributions are welcome, but must follow the schema and workflow to ensure consistency and usability.

---

## How to Contribute

Please follow this process:

1. Add or update the tool in `data/catalogue.csv`
2. Follow the schema defined in `docs/schema.md`
3. Submit a Pull Request

**Important:**

- Do NOT edit the README directly unless explicitly requested
- The README is curated by maintainers
- The CSV is the source of truth

---

## Adding a New Tool

Each new entry MUST include:

- Tool Name
- Category (must match controlled vocabulary)
- Primary Use Case
- Device Type
- Programming Language
- Short Description (one sentence)
- Repository link

Recommended (strongly encouraged):

- Tags (1–5)
- Publication Link
- Publication Status
- Dependencies / Ecosystem
- Notes

---

## Rules

- Each tool MUST have exactly **one Category**
- Each tool MUST have exactly **one Primary Use Case**
- Tags are OPTIONAL but recommended (use **1–5 tags**)
- Tags MUST be **semicolon-separated** (e.g., `event-detection; visualization`)
- Descriptions MUST be **one sentence only**
- Controlled vocabularies MUST be followed exactly where marked as STRICT

---

## Example Entry

```csv
Titta (Python),Experiment Design & Data Collection,experiment-control,experiment-control; psychopy; real-time,Both,Python,Toolbox for running experiments with Tobii eye trackers using PsychoPy,https://github.com/marcus-nystrom/Titta
```

---

## Updating an Existing Tool

You can:

- Fix broken or outdated links
- Improve descriptions
- Add or refine tags
- Add publication information
- Improve notes

Please include a short explanation in your Pull Request.

---

## What Not To Do

- Do NOT create new categories
- Do NOT invent new formats for fields
- Do NOT add multi-sentence descriptions
- Do NOT edit README tables directly

---

## Review Process

Maintainers will:

- Check schema compliance
- Validate links and basic accuracy
- Decide if and how the tool is included in the README

---

## Questions

If something is unclear or you want to propose improvements:

- Open an Issue
- Or start a discussion in your Pull Request

---

Thank you for helping improve this catalogue!

