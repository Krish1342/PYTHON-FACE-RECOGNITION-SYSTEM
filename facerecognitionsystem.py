import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

video_capture = cv2.VideoCapture(0)

# Load known faces
krish_images = face_recognition.load_image_file("Faces/krish.jpg")
krish_encoding = face_recognition.face_encodings(krish_images)[0]

rohan_images = face_recognition.load_image_file("Faces/rohan.jpg")
rohan_encoding = face_recognition.face_encodings(rohan_images)[0]

known_face_encodings = [krish_encoding, rohan_encoding]
known_face_names = ["Krish", "Rohan"]
students = known_face_names.copy()

face_locations = []
face_encodings = []

# Get the correct date and time
now = datetime.now()
current_date = datetime.strftime(now, "%Y-%m-%d")

with open(f"{current_date}.csv", "a", newline="") as f:
    lnwriter = csv.writer(f)

    while True:
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Recognize Faces
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distance)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                # Add the text if the person is present
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottom_left_corner_of_text = (10, 100)
                font_scale = 1.5
                font_color = (255, 0, 0)
                thickness = 3
                line_type = 2
                cv2.putText(frame, name + " PRESENT", bottom_left_corner_of_text, font_scale, font, font_color,
                            thickness, line_type)

                if name in students:
                    students.remove(name)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name, current_time])

        cv2.imshow("Attendance", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

video_capture.release()
cv2.destroyAllWindows()
f.close()