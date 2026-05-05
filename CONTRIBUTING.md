# Contributing Guide

Thank you for your interest in contributing to the **Tobii Research Tools Catalogue** 🙌

This repository is a structured catalogue of tools compatible with Tobii Pro research-grade eye trackers. To keep it consistent and useful, please follow the guidelines below.

---

## 🚀 Quick Start

**Most contributions follow this path:**

1. Edit `data/catalogue.csv`
2. Follow the schema in `docs/schema.md`
3. Open a Pull Request

> **Do not edit the README directly.** It is curated by maintainers.

---

## Contribution Types

You can contribute in two ways:

### 1) Catalogue entries (default)

Add or update tools in the CSV (source of truth).

* File: `data/catalogue.csv`
* Spec: `docs/schema.md`

### 2) Scripts

Add reusable scripts or small workflows to the repository.

**Folder structure**

```
scripts/
  your-script-name/
    README.md
    script.py (or other code files)
```

**Requirements**

* One folder per script
* Include a `README.md` with:

  * purpose
  * inputs / outputs
  * dependencies
  * how to run

**Optional (recommended)**

* If broadly useful, also add the script to `data/catalogue.csv` for discoverability.

---

## Adding a New Tool (CSV)

Each row MUST include:

* Tool Name
* Category (STRICT)
* Primary Use Case
* Device Type (STRICT)
* Programming Language (STANDARDIZED)
* Short Description (**one sentence**)
* Repository link

Recommended fields:

* Tags (1–5)
* Publication Link
* Publication Status (STRICT)
* Dependencies / Ecosystem
* Notes

**Tags format**

* lowercase, hyphen-separated
* multiple values separated by `;`

Example:

```text
event-detection; visualization; wearable
```

---

## Rules

### Catalogue entries

* Exactly **one Category** per tool
* Exactly **one Primary Use Case**
* Use **1–5 tags** (recommended)
* Tags must be `;`-separated (e.g., `event-detection; visualization`)
* Description must be **one sentence**
* Follow STRICT vocabularies exactly

### Scripts

* Must live under `scripts/`
* One folder per script
* Must include a `README.md`
* Should be reusable and clearly documented
* May be added to the CSV if broadly useful

---

## Example CSV Row

```csv
Titta (Python),Experiment Design & Data Collection,experiment-control,experiment-control; psychopy; real-time,Both,Python,Toolbox for running experiments with Tobii eye trackers using PsychoPy,https://github.com/marcus-nystrom/Titta
```

---

## Updating Existing Entries

You can:

* Fix broken/outdated links
* Improve descriptions
* Add or refine tags
* Add publication info
* Improve notes

Please include a short explanation in your Pull Request.

---

## What Not To Do

* Do **not** create new categories
* Do **not** change the schema structure
* Do **not** add multi-sentence descriptions
* Do **not** invent new formats for fields
* Do **not** edit README tables directly

---

## Review Process

Maintainers will:

* Check schema compliance
* Validate links and formatting
* Decide if/how entries appear in the README

---

## Need Help?

* Open an Issue
* Or ask in your Pull Request

---

Thanks for helping build a reliable research resource 🚀