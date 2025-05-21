import cv2

def detect_plate(image):
    plate_cascade = cv2.CascadeClassifier("models/haarcascade_russian_plate_number.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in plates:
        plate_img = image[y:y+h, x:x+w]
        return plate_img, (x, y, w, h)
    return None, None
