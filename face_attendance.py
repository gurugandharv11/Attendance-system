import cv2
import face_recognition
import requests

# Flask API endpoint
API_URL = "http://127.0.0.1:5000/mark_attendance"

# Load known student face
student_image = face_recognition.load_image_file("student1.jpg")
student_encoding = face_recognition.face_encodings(student_image)[0]

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces([student_encoding], face_encoding)
        if True in matches:
            print("Student recognized! Marking attendance...")
            requests.post(API_URL, json={"roll_no": "CS101"})
            cv2.putText(frame, "Attendance Marked", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
