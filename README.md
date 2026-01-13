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

2. Install Dependencies
### Install the required libraries using pip

Bash

pip install -r requirements.txt
3. Run the Application
Bash

python main.py
🎮 How to Play
Initiate: Click the "INITIATE" button on the right control panel to start the security protocol.

Solve: The live video on the left will scramble. Click and drag the grid blocks to swap them.

Objective: Rearrange the blocks to form the correct image of yourself.

Timer: You have 60 seconds to complete the verification before the session expires.

📂 Project Structure
Plaintext

Live-Jigsaw-Captcha/
│
├── main.py              # Core application logic (CV pipeline + Game Loop)
├── requirements.txt     # Dependency list
├── README.md            # Documentation
└── assets/              # (Optional) Fonts and UI assets
🧠 Technical Highlights (Code Logic)
### This project demonstrates efficient handling of video buffers. Instead of saving static images, the engine

Captures a raw frame from the webcam.

Mirrors the frame for natural UX.

Rotates the matrix (NumPy) to align OpenCV coordinates with Pygame surface coordinates.

Slices the array dynamically based on the current grid permutation.

Renders only the visible slices to the GPU buffer.

🔮 Future Roadmap
[ ] Web Port: Rewriting the engine in p5.js for browser-based integration.

[ ] AI Validation: Implementing a background Face Detection model to ensure a face is actually present during the puzzle.

[ ] Audio Feedback: Adding futuristic sound effects for tile swaps and verification success.

🤝 Contributing
### Contributions are welcome! If you have ideas for better UI or optimization

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request
