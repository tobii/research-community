# Tobii Research Tools Catalogue — Schema & Controlled Vocabularies

## 0. Terminology (How to read this document)

To keep the catalogue consistent and usable, different levels of constraints are used:

- **LOCKED** — Fixed structure that must not be changed.

  - Used for: category system and column schema.
  - Meaning: contributors must use exactly what is defined; changes require maintainers to update the standard.

- **STRICT** — Controlled vocabulary with fixed allowed values.

  - Used for: fields like Category, Device Type, Publication Status.
  - Meaning: only the listed values are allowed; no variations or synonyms (e.g., use "Screen-based", not "desktop").

- **GUIDED** — Recommended vocabulary with flexibility.

  - Used for: Primary Use Case and Tags.
  - Meaning: contributors should use existing terms when possible, but may introduce new ones if needed, keeping them short, clear, and functional.

- **STANDARDIZED** — Formatting convention for consistency.

  - Used for: Programming Language.
  - Meaning: use consistent naming (e.g., "Python", not "python" or "Py").

These levels balance consistency (for filtering and structure) with flexibility (for evolving use cases).

## 1. Category System (Locked)

All tools MUST be assigned to one primary category based on their dominant role in the research workflow.

### Categories

1. **Experiment Design & Data Collection**\
   Tools used to design experiments, present stimuli, connect to devices, and collect gaze data.

2. **Data Access, Parsing & Management**\
   Tools for accessing raw data, converting formats, structuring datasets, and managing exports.

3. **Analysis, Visualization & Quality**\
   Tools for analyzing gaze data, detecting events, visualizing results, and assessing data quality.

4. **Integration & Synchronization**\
   Tools for integrating eye tracking with other systems and synchronizing multimodal data streams.

5. **Wearable & Egocentric Workflows**\
   Tools specific to wearable eye tracking, scene video processing, and egocentric analysis.

6. **Utilities, Examples & SDK Resources**\
   Helper scripts, SDK examples, demos, wrappers, and small utilities supporting development and experimentation.

---

## 2. Column Schema (Locked)

Each entry in the catalogue MUST follow this schema.

| Field                    | Required | Description                                             |
|--------------------------|----------|---------------------------------------------------------|
| Tool Name                | Yes      | Official name of the tool/package/repository            |
| Category                 | Yes      | One of the predefined categories                        |
| Primary Use Case         | Yes      | Specific functional purpose (see controlled vocabulary) |
| Tags                     | Optional | Secondary descriptors for filtering and precise classification |
| Device Type              | Yes      | Type of supported eye tracking setup                    |
| Programming Language     | Yes      | Main implementation language(s)                         |
| Short Description        | Yes      | One concise sentence describing the tool                |
| Repository               | Yes      | Link to source code or main project page                |
| Publication Link         | Optional | DOI, paper, or preprint link                            |
| Publication Status       | Optional | Type of publication (see controlled vocabulary)         |
| Dependencies / Ecosystem | Optional | Key SDKs, frameworks, or environments                   |
| Notes                    | Optional | Additional context, limitations, or use cases           |

---

## 3. Controlled Vocabularies

### 3.1 Category (STRICT)

- Experiment Design & Data Collection
- Data Access, Parsing & Management
- Analysis, Visualization & Quality
- Integration & Synchronization
- Wearable & Egocentric Workflows
- Utilities, Examples & SDK Resources

---

### 3.2 Primary Use Case (GUIDED)

Contributors SHOULD use one of the following where possible. New terms are allowed if necessary but must be concise and functional.

- Experiment control
- Stimulus presentation
- Gaze-contingent display
- Data streaming
- Device control
- Recording
- Data parsing
- Format conversion
- Data export
- Fixation detection
- Saccade detection
- AOI analysis
- Visualization
- Quality control
- Drift correction
- Calibration
- Validation
- Synchronization
- Multimodal integration
- Wearable analysis
- Scene video processing
- Annotation
- SDK wrapper
- Example/demo
- Utility

---

### 3.3 Tags (GUIDED)

Tags provide **secondary classification** to complement the primary category. They enable more precise filtering and reflect that tools can serve multiple functions.

#### Purpose

- Capture multiple roles of a tool (e.g., analysis + visualization)
- Enable filtering and future UI/search capabilities
- Avoid overloading categories with edge cases

#### Format Rules

- Use **lowercase**
- Use **hyphen-separated terms** (e.g., `event-detection`, `gaze-mapping`)
- Multiple tags MUST be **semicolon-separated** in CSV:
  - Example: `event-detection; visualization; wearable`
- Avoid duplicates and synonyms where possible

#### Quantity Rules

- Recommended: **1–5 tags per tool**
- Do not exceed 5 unless strongly justified

#### Suggested Tag Vocabulary (non-exhaustive)

**Functional tags**
- experiment-control
- stimulus-presentation
- data-streaming
- device-control
- preprocessing
- data-export
- event-detection
- event-classification
- gaze-mapping
- aoi-analysis
- scanpath-analysis
- visualization
- quality-control
- validation
- drift-correction
- synchronization
- multimodal-integration
- annotation
- feature-extraction
- machine-learning
- pupillometry

**Context tags**
- screen-based
- wearable
- egocentric
- real-time
- offline
- hyperscanning
- pro-lab
- lsl
- glasses-2
- glasses-3

**Ecosystem tags**
- psychopy
- psychtoolbox
- matlab
- python
- r
- javascript
- sdk-wrapper

Contributors SHOULD prefer existing tags when possible, but may introduce new ones if needed, following the formatting rules.

---

### 3.4 Device Type (STRICT)

- Screen-based
- Wearable
- Both

---

### 3.5 Programming Language (STANDARDIZED)

Use consistent naming:

- Python
- MATLAB
- C#
- C++
- R
- JavaScript
- Unity
- Mixed
- Not specified

---

### 3.6 Publication Status (STRICT)

- Journal article
- Preprint
- Other
- No publication

---

## 4. Rules for Contributors

- Each tool MUST have one primary category.
- Each tool MUST have one primary use case.
- Tags are OPTIONAL but strongly encouraged for discoverability.
- Use **1–5 tags**, following the formatting rules.
- Descriptions MUST be limited to one sentence.
- Controlled vocabularies MUST be used where marked as STRICT.
- Optional fields SHOULD be filled whenever information is available.
- Notes SHOULD remain concise and practical (no long paragraphs).

---

## 5. Design Principles

These principles define how the catalogue is structured, maintained, and used. They are intended to remove ambiguity for contributors and keep the project scalable over time.

### 5.1 Source of Truth

- The **CSV (`data/catalogue.csv`) is the canonical source of truth**.
- All tools and metadata MUST be added or updated in the CSV first.
- The README is a curated view derived from the CSV.

### 5.2 Dual Output Model

The catalogue produces two complementary outputs with different purposes:

**1) Full Dataset (CSV)**
- Purpose: **completeness, structure, machine-readability**
- Contains: all tools, all fields, all metadata
- Used for: filtering, analysis, automation, and future web interfaces

**2) Readable Catalogue (README.md)**
- Purpose: **usability, discoverability**
- Contains: a **curated subset** of tools
- Organized by: workflow-based categories
- Uses: simplified columns (Tool, Use Case, Description)

**Rule:** Contributors SHOULD update the CSV first. Maintainers decide if and how entries are surfaced in the README.

### 5.3 Workflow-First Organization

- Categories reflect the **research workflow**, not implementation details.
- The goal is to answer: *“What am I trying to do?”* rather than *“What is this built with?”*
- Each tool MUST have exactly **one primary category**.

### 5.4 Precision via Tags

- Tags provide **secondary classification** for tools that span multiple functions.
- Categories = browsing layer (human-friendly)
- Tags = filtering layer (machine-friendly)
- Tags SHOULD be used to capture nuance without overcomplicating categories.

### 5.5 Clarity over Completeness (in README)

- The README MUST remain **easy to scan and understand**.
- Only the most relevant tools per category should be included.
- Descriptions MUST be **one sentence** and decision-oriented.

### 5.6 Completeness over Simplicity (in CSV)

- The CSV SHOULD aim for **maximum coverage and detail**.
- Optional fields SHOULD be filled when information is available.
- Multiple tags SHOULD be used where appropriate.

### 5.7 Neutrality (No Implicit Judgement)

- The catalogue is **descriptive, not prescriptive**.
- It does not rank, endorse, or discourage tools.
- Fields like “Status” are intentionally excluded to avoid bias.
- Context should be provided via **Notes** instead of labels.

### 5.8 Consistency and Standardization

- STRICT vocabularies MUST be followed exactly.
- STANDARDIZED fields MUST use consistent naming.
- GUIDED fields SHOULD reuse existing terms when possible.

### 5.9 Link Integrity and Reproducibility

- Repository links MUST be valid and point to the primary source.
- Publication links SHOULD use DOIs when available.
- Entries SHOULD be verifiable using public sources.

### 5.10 Maintainability

- The system should minimize manual overhead.
- Avoid fields that require frequent subjective updates.
- Prefer rules based on **observable, stable signals**.

---

These principles ensure the catalogue remains **useful for researchers, consistent for contributors, and scalable over time**.

