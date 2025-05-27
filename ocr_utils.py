import pytesseract
import cv2
import easyocr

def read_plate_text(plate_img, method="Tesseract (default)"):
    if method == "EasyOCR":
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(plate_img)
        return result[0][1] if result else "Tidak Terbaca"
    else:
        gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config='--psm 7')
        return text.strip();
    fgvv
