import easyocr
import cv2
import re
import numpy as np

reader = easyocr.Reader(['en'])

def extract_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return "UNKNOWN"

    h, w, _ = image.shape

    # Crop bottom middle (plate region assumption)
    crop = image[int(h*0.55):h, int(w*0.2):int(w*0.8)]

    # Convert to grayscale
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    # Thresholding to make text clear
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Resize to improve OCR accuracy
    thresh = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    results = reader.readtext(thresh)

    for (bbox, text, prob) in results:
        cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())

        if len(cleaned_text) >= 6:
            return cleaned_text

    return "UNKNOWN"