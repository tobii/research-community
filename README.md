# Tobii Research Tools Catalogue

A curated catalogue of peer-reviewed open-source and third-party tools, scripts, and software packages compatible with Tobii Pro research-grade eye trackers.

This repository helps researchers quickly find tools across the eye-tracking workflow — from experiment design and data collection to analysis and multimodal integration.

---

## How to Use This Catalogue

- Browse by **workflow stage** below to quickly find relevant tools.
- Tables in this README are intentionally **compact for readability**.
- The **full structured dataset** (all fields, notes, and metadata) is available in:
  - `data/catalogue.csv`

---

## Device Tags

- 🖥️ Screen-based
- 👓 Wearable
- 🔀 Both

---

## Categories

- **Experiment Design & Data Collection**
- **Data Access, Parsing & Management**
- **Analysis, Visualization & Quality**
- **Integration & Synchronization**
- **Wearable & Egocentric Workflows**
- **Utilities, Examples & SDK Resources**

---

## Experiment Design & Data Collection

*Use this section if you want to design experiments, present stimuli, or collect gaze data from participants.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [Titta (Python)](https://github.com/marcus-nystrom/Titta) | 🔀 Experiment control | PsychoPy-integrated toolbox for Tobii experiment control and data collection. |
| [Titta (MATLAB)](https://github.com/dcnieho/Titta) | 🔀 Experiment control | PsychToolbox-based MATLAB integration for Tobii experiments. |
| [PyGaze](https://github.com/esdalmaijer/PyGaze) | 🖥️ Experiment control | Cross-platform library for building eye-tracking experiments. |
| [TittaLSL](https://github.com/dcnieho/Titta/tree/master/LSL_streamer) | 🔀 Multimodal experiments | Enables multi-participant experiments via LSL with low latency. |
| [Opticka](https://github.com/iandol/opticka) | 🖥️ Experiment control | MATLAB toolbox for primate experiments using Tobii via Titta. |
| [LabManager](https://github.com/dcnieho/labManager) | 🖥️ Lab orchestration | Manages multiple lab machines and launches experimental tasks. |

---

## Data Access, Parsing & Management

*Use this section if you need to access raw eye-tracking data, convert formats, or prepare datasets for analysis.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [Tobii Pro SDK](https://developer.tobiipro.com/) | 🔀 Data streaming | Official SDK for accessing Tobii Pro data streams and device control. |
| [glassesTools](https://github.com/dcnieho/glassesTools) | 👓 Data processing | Core backend for processing wearable eye-tracking recordings. |
| [Mobile Gaze Mapping](https://github.com/jeffmacinnes/mobileGazeMapping) | 👓 Gaze mapping | Maps wearable gaze onto fixed stimuli using homography. |
| [TobiiGlassesPySuite](https://github.com/ddetommaso/TobiiGlassesPySuite) | 👓 Device control | Controls Tobii Glasses 2 and manages recordings. |
| [TP3Py](https://github.com/smilies-lab/TP3Py) | 👓 Streaming pipeline | Real-time streaming and processing for Glasses 3 data. |

---

## Analysis, Visualization & Quality

*Use this section if you want to analyze gaze data, detect events (fixations, saccades), or evaluate data quality.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [PyMovements](https://github.com/pymovements/pymovements) | 🔀 Full pipeline | End-to-end analysis including preprocessing, detection, and visualization. |
| [PyTrack](https://github.com/titoghose/PyTrack) | 🔀 Feature extraction | Extracts fixations, saccades, and supports statistical analysis. |
| [kollaR](https://cran.r-project.org/package=kollaR) | 🔀 Analysis pipeline | R toolkit for event detection, AOIs, and visualization. |
| [NH2010](https://github.com/dcnieho/NystromHolmqvist2010) | 🔀 Event detection | Adaptive velocity-based fixation/saccade classification. |
| [PeyeMMV](https://github.com/krasvas/PeyeMMV) | 🔀 Event detection | Dispersion-based fixation detection with visualization. |
| [SaFiDe](https://github.com/Neurosistemas-Lab/SaFiDe) | 🔀 Event detection | Deterministic fixation/saccade detection using thresholds. |
| [scanpath (R)](https://github.com/tmalsburg/scanpath) | 🔀 Scanpath analysis | Computes scanpath similarity using MultiMatch. |
| [GlassesValidator](https://github.com/dcnieho/glassesValidator) | 👓 Data quality | Assesses accuracy and precision of wearable recordings. |
| [GazeMapper](https://github.com/dcnieho/gazeMapper) | 👓 AOI analysis | Automates world-based gaze mapping for wearable data. |
| [GlassesViewer](https://github.com/dcnieho/GlassesViewer) | 👓 Visualization | MATLAB tool for viewing and analyzing wearable recordings. |
| [PupEyes](https://github.com/theDebbister/PupEyes) | 🔀 Pupillometry preprocessing | Interactive preprocessing and visualization of pupil data. |
| [PupilMetrics](https://github.com/JulesGoninRIO/PupilMetrics) | 🔀 Pupillometry preprocessing | Removes blink and non-blink artifacts from pupil data. |
| [pypillometry](https://github.com/ihrke/pypillometry) | 🔀 Pupillometry analysis | GLM-based modeling and analysis of pupil dilation. |
| [PupillometryR](https://github.com/samhforbes/PupillometryR) | 🔀 Pupillometry analysis | R pipeline for cleaning, modeling, and visualization. |
| [CHAP](http://in.bgu.ac.il/en/Labs/CNL/chap) | 🔀 Pupillometry analysis | MATLAB GUI for preprocessing and analyzing pupil data. |
| [EyeFeatures](https://github.com/hse-scila/EyeFeatures) | 🔀 ML analysis | Feature engineering and ML pipelines for gaze data. |
| [tobii-eye-tracking-pipeline](https://github.com/jessewashburn/tobii-eye-tracking-pipeline) | 🔀 ML pipeline | End-to-end Tobii-specific pipeline with clustering and ML. |
| [capturing-triadic-egs](https://github.com/mrhmatar/capturing-triadic-egs) | 🔀 Synchrony analysis | Pipeline for analyzing gaze synchrony in interactions. |
| [gazeR](https://github.com/dmirman/gazer) | 🔀 Analysis pipeline | R package for gaze and pupillometry analysis workflows. |

---

## Integration & Synchronization

*Use this section if you need to synchronize eye-tracking data with other systems such as EEG, motion capture, or VR.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [Lab Streaming Layer (LSL)](https://github.com/sccn/labstreaminglayer) | 🔀 Synchronization backbone | Standard framework for time-synchronized multimodal data streams. |
| [TittaLSL](https://github.com/dcnieho/TittaLSL) | 🔀 Multimodal integration | Extends Titta for synchronized multi-device and multi-participant experiments over LSL. |
| [App-TobiiPro](https://github.com/labstreaminglayer/App-TobiiPro) | 🔀 LSL connector | LSL application that connects Tobii Pro devices to LabRecorder using the Tobii Pro C SDK. |
| [tobiilsl](https://github.com/baekgaard/tobiilsl) | 🔀 Python-to-LSL bridge | Lightweight Python interface that pushes Tobii Pro SDK gaze streams into LSL. |
| [TalkToProLab (within Titta)](https://github.com/dcnieho/Titta) | 🖥️ Pro Lab integration | External Presenter bridge for running experiments outside Tobii Pro Lab while keeping Pro Lab recording and analysis workflows. |

---

## Wearable & Egocentric Workflows

*Use this section if you are working with wearable eye trackers and need tools for scene video processing or egocentric analysis.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [EyePort](https://github.com/akashcraft/EyePort) | 👓 Data collection | Collects and exports data from Tobii Pro Glasses 3. |
| [TP3Py](https://github.com/smilies-lab/TP3Py) | 👓 Streaming | Real-time pipeline for wearable gaze and head tracking. |
| [TobiiGlassesPySuite](https://github.com/ddetommaso/TobiiGlassesPySuite) | 👓 Device control | Controls and manages recordings for Glasses 2. |
| [GazeMapper](https://github.com/dcnieho/gazeMapper) | 👓 AOI mapping | Automates mapping gaze onto real-world stimuli. |
| [GlassesValidator](https://github.com/dcnieho/glassesValidator) | 👓 Validation | Evaluates wearable eye-tracking data quality. |
| [GlassesViewer](https://github.com/dcnieho/GlassesViewer) | 👓 Visualization | Visualizes gaze data directly from recordings. |

---

## Utilities, Examples & SDK Resources

*Use this section if you are looking for example code, SDK wrappers, or small utilities to support development and prototyping.*

| Tool | Use Case | Description |
|------|----------|-------------|
| [Tobii Pro SDK Examples](https://github.com/TobiiPro) | 🔀 Example/demo | Official example scripts for using Tobii Pro SDK. |
| [eyetools](https://github.com/tombeesley/eyetools) | 🔀 Utility | Lightweight R package for common eye-tracking processing tasks. |
| [EyeLiveMetrics](https://github.com/Leibniz-HBI/EyeLiveMetrics) | 🖥️ Real-time analysis | Browser-based tool for real-time gaze and reading metrics. |

---

## Contributing

Please see CONTRIBUTING.md for guidelines on how to add or update entries.

---

## Disclaimer

This is a community-maintained catalogue. Inclusion does not imply endorsement. Users should verify compatibility with their specific Tobii Pro device, SDK version, and experimental setup.

