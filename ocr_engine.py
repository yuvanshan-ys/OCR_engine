import easyocr
import cv2
import numpy as np
from PIL import Image

reader = easyocr.Reader(['en'], gpu=True)

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    _, thresh = cv2.threshold(denoised, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_text(image_path):
    processed_img = preprocess_image(image_path)
    pil_image = Image.fromarray(processed_img)
    result = reader.readtext(np.array(pil_image), detail=0)
    full_text = "\n".join(result)
    return full_text.strip()