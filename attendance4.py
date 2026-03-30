import cv2
import face_recognition
import pickle
import numpy as np
from datetime import datetime
import csv
import os
import time

encodings_file = "data/encodings.pkl"

if not os.path.exists(encodings_file):
    print("❌ No users registered. Run register.py first.")
    exit()

with open(encodings_file, "rb") as f:
    known_encodings, known_names = pickle.load(f)

attendance_file = "attendance.csv"

if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Time"])

marked_today = set()
confidence_counter = {}

# 🔥 Cooldown
cooldown_time = 5  # seconds
last_mark_time = {}

# 🔥 Anti-spoof variables
prev_x = None
movement_detected = False
stable_frames = 0
last_position = None

video = cv2.VideoCapture(0)

print("\nSystem Started...")
print("👉 Move your head and then stay still")
print("Press ESC to exit\n")

while True:
    ret, frame = video.read()
    if not ret:
        print("Camera error")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb)

    for encoding, (top, right, bottom, left) in zip(encodings, faces):

        name = "Unknown"

        if len(known_encodings) > 0:
            distances = face_recognition.face_distance(known_encodings, encoding)

            min_dist = np.min(distances)
            index = np.argmin(distances)

            if min_dist < 0.45:
                name = known_names[index]

        # 🔥 MULTI-FRAME
        if name != "Unknown":
            confidence_counter[name] = confidence_counter.get(name, 0) + 1
        else:
            confidence_counter = {}
            movement_detected = False
            stable_frames = 0
            last_position = None

        # 🔥 HEAD MOVEMENT + STABILITY
        face_center_x = (left + right) // 2

        if prev_x is not None:
            if abs(face_center_x - prev_x) > 25:
                movement_detected = True
                stable_frames = 0

        prev_x = face_center_x

        if movement_detected:
            if last_position is not None:
                if abs(face_center_x - last_position) < 10:
                    stable_frames += 1
                else:
                    stable_frames = 0

            last_position = face_center_x

        # Draw
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        status = name

        if not movement_detected:
            status += " | Move Head"
        elif stable_frames < 5:
            status += " | Hold Still"

        cv2.putText(frame, status, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 🔥 COOLDOWN CHECK
        current_time = time.time()
        can_mark = True

        if name in last_mark_time:
            if current_time - last_mark_time[name] < cooldown_time:
                can_mark = False

        # 🔥 FINAL CONDITION
        if (
            name != "Unknown"
            and confidence_counter.get(name, 0) >= 5
            and movement_detected
            and stable_frames >= 5
            and can_mark
        ):
            if name not in marked_today:
                marked_today.add(name)

                with open(attendance_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    time_now = datetime.now().strftime("%d %m %Y %H:%M:%S")
                    writer.writerow([name, time_now])

                print(f"✅ Attendance marked for {name}")

            # 🔥 Update cooldown time
            last_mark_time[name] = current_time

            # Reset
            confidence_counter[name] = 0
            movement_detected = False
            stable_frames = 0
            last_position = None

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()