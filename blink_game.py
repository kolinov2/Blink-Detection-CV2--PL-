# Import Bibliotek
import numpy as np
import cv2

# Pliki haarcascades
face_cascade = cv2.CascadeClassifier('/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

first_read = True

cap = cv2.VideoCapture(0) # Wyznaczenie kamery do rejestrowania (0 = domyslna)
ret,img = cap.read()

while(ret):
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray,5,1,1)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if(len(faces)>0):
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            roi_face = gray[y:y+h,x:x+w]
            roi_face_clr = img[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50))
            if(len(eyes)>=2):
                if(first_read):
                    cv2.putText(img, "Nacisnij s aby zaczac", (100,100), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
                else:
                    print("----------------------")
            else:
                if(first_read):
                    cv2.putText(img, "Nie wykryto oczu", (100,100), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
                else:
                    print("przegrales")
                    first_read=True
    else:
        cv2.putText(img,"Nie widze twojej twarzy!",(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),2)


    cv2.imshow('img',img)
    a = cv2.waitKey(1)
    # Wylacznie skryptu po nacisnieciu "q"
    if(a==ord('q')):
        break
    # Rozpoczecie gry po nacisnieciu "s"
    elif(a==ord('s') and first_read):
        first_read = False


cap.release()
cv2.destroyAllWindows()
