# Tobii Pro Research Tools Catalogue

![Tobii image](https://a.storyblok.com/f/290827487058644/e5c68b989f/tobii-annual-research-report-webinar.jpg)

A curated catalogue of peer-reviewed open-source and third-party tools, scripts, and software packages compatible with Tobii Pro research-grade eye trackers and software.

This repository helps researchers quickly find tools across the eye-tracking workflow — from experiment design and data collection to analysis and multimodal integration.

---

## How to Use This Catalogue

- Browse by **workflow stage** below to quickly find relevant tools.
- Tables in this README are **compact** and show a **curated subset** of tools.
- The **structured dataset** (more complete and continuously expanded) is available in:
  - `data/catalogue.csv`

💡 Tip: Use Ctrl+Click (Windows) or Cmd+Click (Mac) to open links in a new tab.

📐 Schema and contribution rules: `docs/schema.md`

---

## Device Tags

- 🖥️ Screen-based
- 👓 Wearable
- 🔀 Both

---

## Categories

*Tools are listed alphabetically within each category.*

- **Experiment Design & Data Collection**
- **Data Access, Parsing & Management**
- **Analysis, Visualization & Quality**
- **Integration & Synchronization**
- **Wearable & Egocentric Workflows**
- **Utilities, Examples & SDK Resources**


## Experiment Design & Data Collection

*Use this section if you want to design experiments, present stimuli, or collect gaze data from participants.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [iTrace](https://www.i-trace.org/) | 🔀 Experiment control | Community eye-tracking infrastructure built right into development environments for software engineers and education researchers to conduct realistic eye tracking studies. |
| [LabManager](https://github.com/dcnieho/labManager) | 🖥️ Utility | Toolset for managing multi-station behavioral research labs and launching coordinated experiment tasks. |
| [OpenSesame](https://github.com/open-cogsci/OpenSesame) | 🔀 Experiment control | Graphical experiment builder for behavioral sciences with eye-tracking support. |
| [Opticka](https://github.com/iandol/opticka) | 🖥️ Experiment control | MATLAB framework for behavioral experiments and stimulus presentation with Tobii support via Titta. |
| [Presentation (Tobii Pro Extension)](https://www.neurobs.com/) | 🖥️ Device control | Extension enabling direct connection between Tobii Pro eye trackers and Presentation software by Neurobehavioral Systems. |
| [PsychoPy](https://github.com/psychopy/psychopy) | 🔀 Stimulus presentation | Open-source platform for creating and running a wide range of behavioral experiments. |
| [Psychtoolbox](https://github.com/Psychtoolbox-3/Psychtoolbox-3) | 🖥️ Stimulus presentation | Toolbox for vision research and experiment control in MATLAB |
| [PyGaze](https://github.com/esdalmaijer/PyGaze) | 🖥️ Experiment control | Cross-platform Python library for building eye-tracking experiments with stimulus presentation and online gaze interaction. |
| [TalkToProLab (within Titta)](https://github.com/dcnieho/Titta) | 🖥️ Pro Lab integration | Component inside Titta that lets external MATLAB experiments communicate with Tobii Pro Lab recording workflows. |
| [Titta (PsychoPy)](https://github.com/marcus-nystrom/Titta) | 🖥️ Experiment control | Python toolbox for running Tobii screen-based experiments with PsychoPy-based participant setup, calibration, and recording. |
| [Titta (Psychtoolbox)](https://github.com/dcnieho/Titta) | 🖥️ Experiment control | MATLAB toolbox for running Tobii screen-based experiments with Psychtoolbox-based participant setup, calibration, and recording. |
| [Translog-II](https://sites.google.com/site/centretranslationinnovation/translog-ii) | 🖥️ Recording | Program for recording and analyzing writing and translation processes |

---

## Data Access, Parsing & Management

*Use this section if you need to access raw eye-tracking data, convert formats, or prepare datasets for analysis.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [EyePort](https://github.com/akashcraft/EyePort) | 👓 Data export | Software for collecting, reviewing, and exporting data from Tobii Pro Glasses 3 recordings. |
| [glassesTools](https://github.com/dcnieho/glassesTools) | 👓 Data parsing | Python toolkit for importing, structuring, and processing wearable eye-tracking recordings and derived data. |
| [Tobii Pro Glasses 3 SDK](https://github.com/tobiipro/Tobii.Glasses3.SDK) | 👓 Data streaming | Official SDK and examples for accessing Tobii Pro Glasses 3 streams, recordings, and device control. |
| [Tobii Pro SDK](https://developer.tobiipro.com/) | 🖥️ Data streaming | Official SDK for accessing Tobii Pro eye-tracker streams, events, and device control in research applications. |

---

## Analysis, Visualization & Quality

*Use this section if you want to analyze gaze data, detect events (fixations, saccades), or evaluate data quality.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [capturing-triadic-egs](https://github.com/mrhmatar/capturing-triadic-egs/tree/main) | 🔀 Multimodal integration | Open-source workflow for combining eye-tracking and audio data to study gaze and speech synchrony in triadic interactions. |
| [CHAP](http://in.bgu.ac.il/en/Labs/CNL/chap) | 🔀 Pupillometry analysis | MATLAB GUI for processing and analyzing pupillometry data with standardized preprocessing and group analysis workflows. |
| [EyeFeatures](https://github.com/hse-scila/EyeFeatures) | 🔀 Feature extraction | Python package for extracting engineered and optional deep features from eye-tracking data for downstream modeling. |
| [eyetools](https://github.com/tombeesley/eyetools) | 🔀 Data parsing | R package providing tools for processing, analyzing, and visualizing eye-tracking data. |
| [Floating bar graph](https://github.com/richardandersson/TobiiProLabScripts/tree/master/floating%20bar%20graph) | 🖥️ Visualization | Script for plotting floating bar graphs from Tobii Pro Lab exported data. |
| [GazeCode](https://github.com/jsbenjamins/gazecode) | 👓 Annotation | Tool for manual mapping of gaze data to objects of interest. |
| [gazeR](https://github.com/dmirman/gazer) | 🔀 AOI analysis | R package for analysis workflows covering visual-world, preferential-looking, and pupillometry data. |
| [GlassesValidator](https://github.com/dcnieho/glassesValidator) | 👓 Validation | Toolbox for assessing wearable eye-tracking accuracy and precision using standardized validation workflows. |
| [kollaR](https://cran.r-project.org/package=kollaR) | 🔀 AOI analysis | R package for fixation preprocessing, AOI analysis, scanpaths, and visual analytics on eye-tracking data. |
| [NH2010](https://github.com/dcnieho/NystromHolmqvist2010) | 🔀 Event detection | Implementation of the Nyström-Holmqvist adaptive algorithm for classifying fixations and saccades. |
| [PeyeMMV](https://github.com/krasvas/PeyeMMV) | 🔀 Fixation detection | MATLAB toolbox for fixation detection with interactive visualization and review support. |
| [PhysioData Toolbox](https://physiodatatoolbox.leidenuniv.nl/) | 🔀 Visualization | Toolbox for synchronized preprocessing and visualization of physiological and eye-tracking time series. |
| [PupEyes](https://github.com/HanZhang-psych/pupeyes) | 🔀 Pupillometry preprocessing | Interactive Python package for preprocessing, quality control, and visualization of pupillometry data. |
| [Pupillometric measures of cognitive load](https://github.com/Jihaiku/Pupillometric-measures-of-cognitive-load) | 🔀 Feature extraction | Collection of scripts for deriving cognitive-load-related pupil measures from eye-tracking recordings. |
| [PupillometryR](https://github.com/samhforbes/PupillometryR) | 🔀 Pupillometry analysis | R package for cleaning, transforming, and analyzing pupillometry data. |
| [PupilMetrics](https://github.com/JulesGoninRIO/PupilMetrics) | 🔀 Pupillometry preprocessing | Python toolkit for removing blink and non-blink artifacts from pupil diameter time series. |
| [PyMovements](https://github.com/pymovements/pymovements) | 🔀 Analysis pipeline | Unified Python framework for loading, preprocessing, analyzing, and visualizing eye-movement data. |
| [PyTrack](https://github.com/titoghose/PyTrack) | 🔀 Feature extraction | Python toolkit for extracting eye-movement events and engineered features for downstream analysis. |
| [pypillometry](https://github.com/ihrke/pypillometry) | 🔀 Pupillometry analysis | Python package for pupillometry preprocessing, model-based analysis, and visualization. |
| [SaFiDe](https://github.com/smadariagar/SaFiDe/tree/main) | 🔀 Event detection | Threshold-based algorithm for fixation and saccade detection in gaze data. |
| [scanpath (R)](https://github.com/tmalsburg/scanpath) | 🔀 Scanpath analysis | R package for computing scanpath similarity and alignment metrics such as MultiMatch. |
| [tobii-eye-tracking-pipeline](https://github.com/jessewashburn/tobii-eye-tracking-pipeline) | 🔀 Analysis pipeline | Tobii-oriented workflow for preprocessing, clustering, and machine-learning analysis of gaze data. |
| [Transition matrix plot](https://github.com/richardandersson/TobiiProLabScripts/tree/master/transition%20matrix%20plot) | 🖥️ Visualization | Script for generating AOI transition matrix plots from Tobii Pro Lab exported data. |

---

## Integration & Synchronization

*Use this section if you need to synchronize eye-tracking data with other systems such as EEG, motion capture, or VR.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [App-TobiiPro](https://github.com/labstreaminglayer/App-TobiiPro) | 🖥️ Data streaming | LSL application that connects compatible Tobii Pro devices to the Lab Streaming Layer ecosystem. |
| [EYE-EEG](https://github.com/olafdimigen/eye-eeg) | 🔀 Multimodal integration | Toolbox for synchronizing and analyzing combined EEG and eye-tracking data. |
| [Lab Streaming Layer (LSL)](https://github.com/sccn/labstreaminglayer) | 🔀 Synchronization | Standard backbone for time-synchronized multimodal data acquisition across research devices. |
| [LSL for Tobii Pro Glasses 3](https://github.com/tobiipro/Tobii.Glasses3.SDK#lsl-connector-for-glasses-3) | 👓 Data streaming | LSL connector resources for streaming Tobii Pro Glasses 3 data into multimodal recording setups. |
| [Titta LSL Streamer](https://github.com/dcnieho/Titta/tree/master/LSL_streamer) | 🖥️ Synchronization | Titta component for streaming Tobii data into Lab Streaming Layer for synchronized experiments. |
| [tobiilsl](https://github.com/baekgaard/tobiilsl) | 🖥️ Data streaming | Lightweight Python bridge for publishing Tobii Pro SDK gaze streams into Lab Streaming Layer. |

---

## Wearable & Egocentric Workflows

*Use this section if you are working with wearable eye trackers and need tools for scene video processing or egocentric analysis.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [GazeMapper](https://github.com/dcnieho/gazeMapper) | 👓 Scene video processing | Workflow for mapping wearable gaze onto known real-world targets in egocentric recordings. |
| [GlassesViewer](https://github.com/dcnieho/GlassesViewer) | 👓 Visualization | MATLAB-based viewer for wearable recordings with synchronized scene video, gaze overlays, and inspection tools. |
| [Mobile Gaze Mapping](https://github.com/jeffmacinnes/mobileGazeMapping) | 👓 Scene video processing | Toolbox for mapping mobile eye-tracking gaze onto fixed stimuli using computer-vision homography methods. |
| [TobiiGlassesPyController](https://github.com/ddetommaso/TobiiGlassesPyController) | 👓 Device control | Python controller for operating Tobii Pro Glasses devices and managing recordings from code. |
| [TobiiGlassesPySuite](https://github.com/ddetommaso/TobiiGlassesPySuite) | 👓 Device control | Python suite for controlling Tobii Pro Glasses 2 devices and working with recordings. |
| [TP3Py](https://github.com/SUNYOpt/TP3Py) | 👓 Data streaming | Real-time pipeline for streaming and processing Tobii Pro Glasses 3 gaze and head-motion data. |

---

## Utilities, Examples & SDK Resources

*Use this section if you are looking for example code, SDK wrappers, or small utilities to support development and prototyping.*

| Tool | Use Case | Description |
| ---- | -------- | ----------- |
| [EyeLiveMetrics](https://git.gesis.org/iir/eyelivemetrics) | 🖥️ Real-time analysis | Browser-based open-source plugin for real-time reading and eye movement metrics from streamed gaze data on web pages. |

---

## Contributing

Contributions are welcome.

👉 Please **update `data/catalogue.csv` first** following the schema before proposing changes to the README.

See `CONTRIBUTING.md` for full guidelines.

---

## Disclaimer

This is a community-maintained catalogue. Inclusion does not imply endorsement. Users should verify compatibility with their specific Tobii Pro device, SDK version, and experimental setup.

