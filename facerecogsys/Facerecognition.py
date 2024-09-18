import cv2

def facerecog():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('H:/JARVIS Main/facerecogsys/trainer/trainer.yml')   
    cascadePath = cv2.data.haarcascades +"haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath) 

    font = cv2.FONT_HERSHEY_SIMPLEX 
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640) 
    cam.set(4, 480) 

    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    # flag = True

    while True:

        ret, img =cam.read() 

        converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  

        faces = faceCascade.detectMultiScale( 
            converted_image,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            Imgnumber, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w])
            if (accuracy < 100):
                accuracy = "  {0}%".format(round(100 - accuracy))

            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))
            
            cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
