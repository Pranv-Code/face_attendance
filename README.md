# 🎯 Face Recognition Attendance System

A real-time face recognition-based attendance system built using Python, OpenCV, and face_recognition.
This system captures faces via webcam, verifies identity, prevents spoofing, and logs attendance efficiently.

---

## 🚀 Features

* ✅ Face Registration System
* 🎥 Real-time Face Recognition
* 🧠 Multi-frame Verification (reduces false positives)
* 🔐 Anti-Spoofing (Head Movement + Stability Check)
* ⏱️ Cooldown System (prevents repeated marking)
* 📁 CSV-based Attendance Logging
* ⚡ Optimized for smooth performance

---

## 🧠 How It Works

1. User registers their face using webcam.
2. System encodes and stores facial features.
3. During attendance:

   * Detects face in real-time
   * Matches with stored encodings
   * Verifies using multi-frame confirmation
   * Checks for head movement (anti-spoof)
   * Marks attendance if all conditions pass

---

## 📁 Project Structure

```
face_attendance/
│
├── register.py          # Register new users
├── attendance.py        # Run attendance system
├── data/
│   └── encodings.pkl    # Stored face encodings
│
└── attendance.csv       # Attendance records
```

---

## ⚙️ Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install opencv-python face_recognition dlib numpy
```

---

## ▶️ Usage

### 1. Register User

```bash
python register.py
```

* Enter name
* Press **S** to capture face

---

### 2. Start Attendance

```bash
python attendance.py
```

* Look at camera
* Move head slightly
* Hold still
* Attendance will be marked

---

## 📊 Attendance Format

```
Name, Time
Rahul, 10:23:11
Aman, 10:25:03
```

---

## 🔐 Anti-Spoofing Mechanism

The system prevents fake attendance using:

* Head movement detection
* Stability verification
* Multi-frame confirmation

This ensures:

* ❌ Photos won’t work easily
* ❌ Static images are rejected
* ✅ Real users are verified

---

## ⚡ Performance Optimizations

* Frame skipping (process every N frames)
* Reduced image size for faster detection
* HOG-based face detection (lightweight)

---

## 🛠️ Tech Stack

* Python
* OpenCV
* face_recognition
* dlib
* NumPy

---

## 🚀 Future Improvements

* 🌐 Web App using Flask
* 🖥️ GUI (Tkinter / PyQt)
* 🧠 Blink Detection (advanced anti-spoof)
* ☁️ Database integration (SQLite / Firebase)
* 📊 Dashboard & Analytics

---

## 📌 Notes

* Works best in good lighting conditions
* One face per frame recommended during registration
* Accuracy depends on image quality

---

## 👨‍💻 Author

Developed as a smart attendance system project using face recognition.

---

## ⭐ Acknowledgment

Inspired by real-world biometric attendance systems and computer vision applications.

---
