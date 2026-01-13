# 🔐 Live Video Jigsaw CAPTCHA

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/Computer_Vision-OpenCV-green?style=for-the-badge&logo=opencv)
![Pygame](https://img.shields.io/badge/GUI-Pygame-red?style=for-the-badge&logo=pygame)
![Status](https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge)

> **An innovative "Liveness Detection" security mechanism that turns your real-time video feed into an interactive puzzle.**

---

## 📜 Overview

Traditional CAPTCHAs (text or static image selection) are becoming increasingly easy for AI bots to solve. **Live Video Jigsaw CAPTCHA** introduces a new layer of security by requiring **real-time human interaction** with a live video stream.

The system captures the user's webcam feed, slices it into a $4 \times 4$ scrambled grid in real-time, and requires the user to reconstruct their own live video stream. This proves:
1.  **Liveness:** The video feed is active (not a static photo).
2.  **Humanity:** The ability to recognize context and continuity in a moving image.

---

## 📸 Demo Preview

*(Recommended: Add a screenshot or GIF of your game here later)*

---

## ✨ Key Features

* **Real-Time Video Slicing:** Uses `OpenCV` and `NumPy` to slice live video buffers into 16 discrete textures at 60 FPS.
* **Interactive Drag-and-Drop:** Seamlessly swap video tiles while the video continues to play inside them.
* **Cyberpunk UI:** Custom-built interface with a futuristic security aesthetic, status indicators, and countdown timers.
* **State Machine Logic:** Robust game loop handling states for `MENU`, `SCANNING`, `VERIFIED`, and `ACCESS DENIED`.
* **Dynamic Difficulty:** Code structure allows for easy expansion to $3 \times 3$ or $5 \times 5$ grids.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Computer Vision:** OpenCV (`cv2`) - Handles video capture, mirroring, and frame processing.
* **Game Engine:** Pygame - Manages the rendering loop, event handling, and UI drawing.
* **Math/Matrix:** NumPy - Used for efficient array manipulation (rotating and slicing video frames).

---

## 🚀 Installation & Setup

### Prerequisites
Ensure you have Python installed on your system.

### 1. Clone the Repository
```bash
git clone [https://github.com/tanishq-ch/CaptchaGames.git](https://github.com/tanishq-ch/CaptchaGames.git)
cd CaptchaGames


