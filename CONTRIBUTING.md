# Contributing Guide

Thank you for your interest in contributing to the **Tobii Research Tools Catalogue** 🙌

This repository is a structured catalogue of tools compatible with Tobii Pro research-grade eye trackers. To keep it consistent and useful, please follow the guidelines below.

---

## 🚀 Quick Start

There are two contribution paths in this repository:

| Contribution Type | Purpose                                                              | Main Location        |
| ----------------- | -------------------------------------------------------------------- | -------------------- |
| Catalogue entries | Add structured metadata about tools, packages, workflows, or scripts | `data/catalogue.csv` |
| Scripts           | Contribute reusable code, utilities, or workflows                    | `scripts/`           |

> **Do not edit the README directly.** It is curated by maintainers.

---

## 1. Contributing to the Catalogue (`catalogue.csv`)

Use this path to:

* Add a new tool or package
* Add metadata about an existing script
* Improve discoverability and filtering
* Add publication or ecosystem information

### Steps

1. Edit `data/catalogue.csv`
2. Follow the schema in `docs/schema.md`
3. Open a Pull Request

### Required Fields

Each row MUST include:

* Tool Name
* Category (STRICT)
* Primary Use Case
* Device Type (STRICT)
* Programming Language (STANDARDIZED)
* Short Description (**one sentence**)
* Repository link

### Recommended Fields

* Tags (1–5)
* Publication Link
* Publication Status (STRICT)
* Dependencies / Ecosystem
* Notes

### Tags Format

* lowercase, hyphen-separated
* multiple values separated by `;`

Example:

```text
event-detection; visualization; wearable
```

### Rules for Catalogue Entries

* Exactly **one Category** per tool
* Exactly **one Primary Use Case**
* Use **1–5 tags** (recommended)
* Tags must be `;`-separated
* Description must be **one sentence**
* Follow STRICT vocabularies exactly

### Example `catalogue.csv` Row

```csv
Titta (Python),Experiment Design & Data Collection,experiment-control,experiment-control; psychopy; real-time,Both,Python,Toolbox for running experiments with Tobii eye trackers using PsychoPy,https://github.com/marcus-nystrom/Titta
```

---

## 2. Contributing Scripts

Use this path to contribute:

* Standalone scripts
* Small workflows
* Utilities
* Reusable analysis code

### Folder Structure

```
scripts/
  your-script-name/
    README.md
    script.py (or other code files)
```

### Requirements

* One folder per script
* Include a `README.md` with:

  * purpose
  * inputs / outputs
  * dependencies
  * how to run

### Rules for Scripts

* Scripts MUST live under `scripts/`
* Each script MUST have its own folder
* Each script MUST include a `README.md`
* Scripts SHOULD be reusable and clearly documented

### Optional (Recommended)

If a script is broadly useful, ALSO add it to `data/catalogue.csv`.

This improves:

* discoverability
* filtering
* future search and web interfaces

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
