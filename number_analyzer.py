import cv2
import os
import sys
import easyocr
import re
import numpy as np

filename = sys.argv[1]
splitted_filename = filename.split(".")[0]

color = sys.argv[2]

if not os.path.exists(f"dataset/{filename}"):
    print("Данных по этому изображению не существует.")
    exit()

def analyze_number(working_image: str, working_color: str) -> str|None:
    image = cv2.imread(working_image)
    b, g, r = cv2.split(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if working_color == "gray":
        blur = cv2.medianBlur(gray, 3)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif working_color == "blue":
        blur = cv2.medianBlur(b, 3)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif working_color == "red":
        blur = cv2.medianBlur(r, 3)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    elif working_color == "green":
        blur = cv2.medianBlur(g, 3)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        print("Неверное название цвета.")
        return

    cv2.imwrite(f"output_colors/{splitted_filename}/blur.png", blur)
    cv2.imwrite(f"output_colors/{splitted_filename}/binary.png", binary)

    reader = easyocr.Reader(['en'], gpu=False)
    results = reader.readtext(binary, allowlist='0123456789')

    found_number = None
    for bbox, text, conf in results:
        text = text.replace(" ", "")
        print(f"Найдено: '{text}' (уверенность: {conf:.2f})")
        
        if re.fullmatch(r"\d{6}", text):
            found_number = text
            return found_number
        

print(analyze_number(f"dataset/{filename}", color))
