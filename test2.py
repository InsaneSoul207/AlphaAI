import cv2
import numpy as np
import os

class FaceRecognitionLogin:
    def __init__(self):
        self.known_faces = []
        self.known_face_names = []
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def load_known_faces(self, path):
        # Load known faces from a directory
        for file in os.listdir(path):
            img = cv2.imread(os.path.join(path, file))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) > 0:
                self.known_faces.append(gray)
                self.known_face_names.append(os.path.splitext(file)[0])

    def recognize_face(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Check if a face was detected
        if len(faces) > 0:
            # Extract the face region
            x, y, w, h = faces[0]
            face_region = gray[y:y+h, x:x+w]

            # Compare the face region with known faces
            for i, known_face in enumerate(self.known_faces):
                if self.compare_faces(face_region, known_face):
                    return self.known_face_names[i]

        return "Unknown"

    def compare_faces(self, face1, face2):
        # Simple comparison using histogram comparison
        hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
        return cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL) > 0.5

    def register(self, username, camera_index=0):
        # Initialize the camera
        cap = cv2.VideoCapture(camera_index)

        # Take a few frames to stabilize the camera
        for i in range(10):
            ret, frame = cap.read()

        # Take a photo of the user
        ret, frame = cap.read()
        if not ret:
            return False

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        # Check if a face was detected
        if len(faces) > 0:
            # Extract the face region
            x, y, w, h = faces[0]
            face_region = gray[y:y+h, x:x+w]

            # Add the face region to the known faces
            self.known_faces.append(face_region)
            self.known_face_names.append(username)

            # Save the face region to a file
            cv2.imwrite(f"faces/{username}.jpg", face_region)

            # Release the camera
            cap.release()
            cv2.destroyAllWindows()

            return True

        return False

    def login(self, camera_index=0):
    # Initialize the camera
        cap = cv2.VideoCapture(camera_index)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Recognize the face
            name = self.recognize_face(frame)

            # Display the result
            cv2.imshow('Face Recognition Login', frame)
            cv2.putText(frame, f"Recognized: {name}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # If a face is recognized, exit the loop
            if name != "Unknown":
                print(f"Welcome, {name}!")
                break

            # Check if the user wants to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cap.release()
        cv2.destroyAllWindows()

    def main(self):
        print("Welcome to Face Recognition Login!")
        choice = input("Do you want to login or register? (login/register): ")

        if choice.lower() == "login":
            self.load_known_faces("faces")
            self.login()
        elif choice.lower() == "register":
            username = input("Enter your username: ")
            if self.register(username):
                print("Registration successful!")
            else:
                print("Registration failed. Please try again.")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    frl = FaceRecognitionLogin()
    frl.main()