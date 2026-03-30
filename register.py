import cv2
import face_recognition
import pickle
import os

# Create folder
if not os.path.exists("data"):
    os.makedirs("data")

encodings_file = "data/encodings.pkl"

# Load safely
known_encodings = []
known_names = []

if os.path.exists(encodings_file) and os.path.getsize(encodings_file) > 0:
    try:
        with open(encodings_file, "rb") as f:
            known_encodings, known_names = pickle.load(f)
    except:
        print("⚠️ Resetting corrupted file")
        known_encodings = []
        known_names = []

name = input("Enter your name: ").strip()

# 🔥 CHECK DUPLICATE
if name in known_names:
    print(f"❌ User '{name}' already registered!")
    print("👉 Use a different name or delete old data.")
    exit()

video = cv2.VideoCapture(0)

print("\nPress 's' to capture")
print("Press ESC to exit\n")

while True:
    ret, frame = video.read()
    if not ret:
        print("Camera error")
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)

    for (top, right, bottom, left) in faces:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Register", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        if len(faces) == 0:
            print("❌ No face detected")
            continue

        if len(faces) > 1:
            print("❌ Multiple faces detected")
            continue

        try:
            encodings = face_recognition.face_encodings(rgb)

            if len(encodings) == 0:
                print("❌ Encoding failed")
                continue

            encoding = encodings[0]

            known_encodings.append(encoding)
            known_names.append(name)

            with open(encodings_file, "wb") as f:
                pickle.dump((known_encodings, known_names), f)

            print(f"✅ {name} registered successfully!")
            break

        except Exception as e:
            print("❌ Encoding error:", e)
            continue

    elif key == 27:
        break

video.release()
cv2.destroyAllWindows()