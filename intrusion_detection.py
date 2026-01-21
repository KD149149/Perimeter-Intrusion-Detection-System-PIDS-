"""
Perimeter Intrusion Detection System (PIDS)
------------------------------------------
Code by: Kajal Dadas
Contact: kajaldadas149@gmail.com

Description:
AI-ready perimeter surveillance system with optical + thermal
decision cockpit, intrusion detection, and operator support UI.

Note:
This codebase is designed for demo, pilot, and scalable deployment.
"""

import cv2
import numpy as np
import pandas as pd
import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from collections import deque

# =========================
# SYSTEM DIRECTORIES
# =========================
BASE_DIR = os.getcwd()
RECORD_DIR = os.path.join(BASE_DIR, "recordings")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
SNAP_DIR = os.path.join(BASE_DIR, "snapshots")
for d in [RECORD_DIR, REPORT_DIR, SNAP_DIR]:
    os.makedirs(d, exist_ok=True)

log_data = []

# =========================
# BACKGROUND + TRACKING
# =========================
bg = cv2.createBackgroundSubtractorMOG2()
next_id = 1
tracks = {}  # id -> data

VIRTUAL_FENCE_Y = 260
LOITER_TIME = 5  # seconds

# =========================
# CLASSIFICATION (HEURISTIC – AI READY)
# =========================
def classify_object(w, h, speed):
    area = w * h
    if area < 4000:
        return "Animal", (0, 255, 255), 0.65
    if area > 15000:
        return "Vehicle", (0, 165, 255), 0.85
    return "Human", (0, 0, 255), 0.90

def threat_level(dist, speed):
    if dist < 50 and speed > 1.0:
        return "CRITICAL"
    if dist < 100:
        return "HIGH"
    if dist < 200:
        return "MEDIUM"
    return "LOW"

# =========================
# FUSION (THERMAL SIMULATION)
# =========================
def thermal_sim(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.applyColorMap(gray, cv2.COLORMAP_JET)

def fuse(optical, thermal, alpha):
    return cv2.addWeighted(optical, alpha, thermal, 1 - alpha, 0)

# =========================
# MAIN PROCESSOR WITH MULTI-VIEW
# =========================
def process_feed(source):
    global next_id

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        messagebox.showerror("Error", "Source not accessible")
        return

    date_dir = os.path.join(RECORD_DIR, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(date_dir, exist_ok=True)

    out = cv2.VideoWriter(
        os.path.join(date_dir, f"intrusion_{datetime.now().strftime('%H-%M-%S')}.avi"),
        cv2.VideoWriter_fourcc(*"XVID"),
        20,
        (640, 480)
    )

    fusion_alpha = 0.7
    show_fence = True
    start_time = time.time()
    fps_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (640, 480))
        thermal = thermal_sim(frame)
        fused = fuse(frame, thermal, fusion_alpha)

        # ========= DETECTION ON FUSED FEED =========
        mask = bg.apply(frame)
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        now = time.time()
        fps_counter += 1
        fps = fps_counter / max(now - start_time, 1)

        for c in cnts:
            if cv2.contourArea(c) < 1500:
                continue

            x, y, w, h = cv2.boundingRect(c)
            cx, cy = x + w // 2, y + h // 2

            obj_type, color, conf = classify_object(w, h, 0.5)
            dist = abs(VIRTUAL_FENCE_Y - cy)
            threat = threat_level(dist, 0.5)

            obj_id = next_id
            next_id += 1

            tracks[obj_id] = {"trail": deque(maxlen=20), "start": now}
            tracks[obj_id]["trail"].append((cx, cy))

            # DRAWING
            cv2.rectangle(fused, (x, y), (x + w, y + h), color, 2)
            cv2.putText(fused, f"ID-{obj_id} {obj_type} {int(conf*100)}%",
                        (x, y - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
            cv2.putText(fused, f"THREAT: {threat}",
                        (x, y + h + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

            # SNAPSHOT
            snap_path = os.path.join(SNAP_DIR, f"{datetime.now().strftime('%H%M%S')}_ID{obj_id}.jpg")
            cv2.imwrite(snap_path, frame)

            log_data.append({
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Time": datetime.now().strftime("%H:%M:%S"),
                "ID": obj_id,
                "Type": obj_type,
                "Threat": threat,
                "Confidence": conf
            })

        # VIRTUAL FENCE
        if show_fence:
            cv2.line(fused, (0, VIRTUAL_FENCE_Y), (640, VIRTUAL_FENCE_Y), (255, 0, 0), 2)

        # HUD on fused feed
        cv2.putText(fused, f"FPS: {int(fps)}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(fused, "AI RECOMMENDATION: Monitor & alert patrol",
                    (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        # ========= MULTI-VIEW COMPOSITE =========
        thermal_small = cv2.resize(thermal, (320, 240))  # smaller inset
        frame_small = cv2.resize(frame, (320, 240))      # original optical feed inset

        # Combine vertically
        side_panel = np.vstack([frame_small, thermal_small])
        # Combine horizontally: fused feed + side panel
        multi_view = np.hstack([fused, side_panel])

        cv2.imshow("PIDS – Decision Cockpit Multi-View", multi_view)
        out.write(fused)

        # ===== Key Controls =====
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'):
            fusion_alpha = 0.9
        elif key == ord('2'):
            fusion_alpha = 0.2
        elif key == ord('3'):
            fusion_alpha = 0.5
        elif key == ord('f'):
            show_fence = not show_fence

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# =========================
# REPORT
# =========================
def save_report():
    if log_data:
        df = pd.DataFrame(log_data)
        df.to_excel(os.path.join(REPORT_DIR, "intrusion_log.xlsx"), index=False)

# =========================
# MENU
# =========================
def launch_menu():
    root = tk.Tk()
    root.withdraw()

    c = simpledialog.askstring(
        "Mode Select",
        "1 – Laptop Camera\n2 – IP Camera\n3 – Video File"
    )

    if c == "1":
        process_feed(0)
    elif c == "2":
        url = simpledialog.askstring("IP Camera", "Enter IP stream URL")
        process_feed(url)
    elif c == "3":
        file = simpledialog.askstring("Video", "Enter video filename")
        if os.path.exists(file):
            process_feed(file)

    save_report()

# =========================
# ENTRY
# =========================
if __name__ == "__main__":
    launch_menu()
