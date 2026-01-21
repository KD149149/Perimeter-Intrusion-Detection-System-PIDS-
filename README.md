
# 🚨 Perimeter Intrusion Detection System (PIDS)

**AI-Ready | Optical + Thermal Decision Cockpit | Python**

---

## Overview

The **Perimeter Intrusion Detection System (PIDS)** is a Python-based surveillance solution designed to enhance **situational awareness and operator decision-making** for secure perimeters such as borders, military bases, campuses, factories, and critical infrastructure.

The system converts a standard camera feed into a **real-time decision cockpit** by combining:

* Optical live video
* Thermal visualization (simulation, thermal-camera ready)
* Intrusion detection
* Threat prioritization
* Multi-view operator screen

This repository contains a **working MVP** that is scalable and ready for AI upgrades.

---

## Key Features

* Input sources:

  * Laptop / USB camera
  * IP camera (RTSP / HTTP)
  * Recorded video file
* **Multi-view single screen**

  * Large main live feed
  * Side panel with optical + thermal view
* Motion-based intrusion detection
* Color-coded object classification
* Threat level assessment (Low / Medium / High / Critical)
* Virtual fence breach detection
* Auto snapshot on intrusion
* Date-wise video recording
* Excel intrusion report generation
* Keyboard-controlled fusion bias
* Safe exit and clean resource handling

---

## Screen Layout (Operator View)

```
┌───────────────────────────────┬───────────────┐
│                               │ Optical View  │
│   Main Live / Fused Feed       ├───────────────┤
│   (Detection + Overlays)       │ Thermal View  │
│                               │               │
└───────────────────────────────┴───────────────┘
```

---

## Folder Structure

```
PIDS/
│── intrusion_detection.py
│── recordings/
│   └── YYYY-MM-DD/
│       └── intrusion_HH-MM-SS.avi
│── snapshots/
│   └── HHMMSS_IDx.jpg
│── reports/
│   └── intrusion_log.xlsx
│── README.md
│── requirements.txt

```

---

## How to Run

```bash
python intrusion_detection.py
```

## How to Run

```bash
opencv-python
numpy
pandas
openpyxl
```


A popup menu will appear:

1. Laptop Camera
2. IP Camera
3. Video File

Press **q** to quit safely at any time.

---

## Keyboard Controls

| Key | Function              |
| --- | --------------------- |
| 1   | Optical-dominant view |
| 2   | Thermal-dominant view |
| 3   | Balanced fusion       |
| f   | Toggle virtual fence  |
| q   | Quit system           |

---

## AI Upgrade Ready

The current system is structured to easily integrate:

* YOLO / RT-DETR for object detection
* DeepSORT for multi-target tracking
* Real thermal camera streams
* Weapon posture and behavior analysis
* GIS / command-center dashboards

---

## Use Cases

* Border & perimeter security
* Defense and military installations
* Industrial plants and factories
* Campuses and large facilities
* Critical infrastructure protection

---

## Author & Contact

**Code by:** Kajal Dadas
📧 **Contact:** [kajaldadas149@gmail.com](mailto:kajaldadas149@gmail.com)
📌 *For detailed projects, collaborations, and advanced deployments*

---

## Disclaimer

This project is provided as a **technology demonstration and development reference**.
Final deployment should comply with local laws, security policies, and data privacy regulations.

