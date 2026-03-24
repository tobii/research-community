# DRAFT

This README is a draft and subject to change.

# products-solutions-community
Tobii Products &amp; Solutions Developer Community

This repo does not contain any code or examples but consists of this README listing a collection of projects, scripts and tools made by separate entities for use with Tobii software and organized by the following categories:

1. Experiments & Data Collection - "I want to set up and run a study"
2. Analysis & Pipelines ⭐ (core) - "I have data - now what?"
3. Gaze Mapping & AOIs - "Where are people looking"
4. Metrics & Event Detection - "turn gaze into meaningful signals"
5. Pupillometry & Cognitive metrics - “Understand cognitive load / pupil response”
6. Visualization - Make sense of results
7. Data Quality - “Is my data trustworthy?”

## Contribution
We are always looking for more contributions! If you want to contribute clone the repo and create a Pull Request with a link to your project and a short description in this README.

## Tobii Pro SDK Documentation
For integrations with the Tobii Pro SDK please see the official documentation for further help [Tobii Pro SDK Documentation](https://developer.tobiipro.com/index.html)

## Experiments & Data Collection
* [TittaLSL](https://github.com/dcnieho/TittaLSL) - Toolbox for creating networked multi-participant eye-tracking experiments using Tobii eye trackers via LSL (Lab Streaming Layer). Achieves ~3 ms end-to-end latency.
* [glassesTools](https://github.com/dcnieho/glassesTools) - Dependency for several dcnieho tools; not standalone
* [PyGaze](https://github.com/esdalmaijer/PyGaze) - Open-source toolbox for eye tracking in Python
* [TobiiGlassesPySuite](https://github.com/ddetommaso/TobiiGlassesPySuite) - Platform-independent suite for controlling Tobii Pro Glasses 2 and managing recordings beyond what the manufacturer's software offers.
* [Titta](MATLAB/PsychToolbox) - MATLAB counterpart to the Python Titta. Full Tobii Pro SDK integration via PsychToolbox for experiment control and data collection.

## Analysis & Pipelines ⭐ (core)
* [GlassesViewer](https://github.com/dcnieho/GlassesViewer) - MATLAB utility for viewing and analyzing data from Tobii Pro Glasses 2 and 3 directly from SD card. Integrates with GazeCode for manual gaze mapping.
* [scanpath](https://github.com/tmalsburg/scanpath) - R package for computing scanpath similarity between participants using the MultiMatch algorithm.
* [TP3Py](https://github.com/smilies-lab/TP3Py) - Modular streaming pipeline for collection and real-time analysis of eye/head tracking data using Tobii Pro Glasses 3.
## Gaze Mapping & AOIs
* [EyeLiveMetrics](https://github.com/Leibniz-HBI/EyeLiveMetrics) - Browser plugin for real-time mapping of gaze to webpage text. Computes fixation, saccade, and reading metrics live without post-hoc AOI annotation.
## Metrics & Event Detection
## Pupillometry & Cognitive metrics
## Visualization
## Data Quality
* [GlassesValidator](https://github.com/dcnieho/glassesValidator) - Automated tool for determining accuracy and precision (data quality) of wearable eye tracker recordings using a validation poster.
