import cv2
import os
import sys
import numpy as np

filename = sys.argv[1]
splitted_filename = filename.split(".")[0]

if not os.path.exists(f"dataset/{filename}"):
    print("Файла с таким именем не существует.")
    exit()

os.makedirs(f"output_colors/{splitted_filename}", exist_ok=True)

img = cv2.imread(f"dataset/{filename}")

if img is None:
    print("Изображение не найдено.")
    exit()

b, g, r = cv2.split(img)
cv2.imwrite(f"output_colors/{splitted_filename}/blue.png", b)   
cv2.imwrite(f"output_colors/{splitted_filename}/green.png", g)  
cv2.imwrite(f"output_colors/{splitted_filename}/red.png", r)    

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f"output_colors/{splitted_filename}/grayscale.png", gray)

contrasts = [
    ("Синий", np.std(b)),
    ("Зеленый", np.std(g)), 
    ("Красный", np.std(r)),
    ("Ч/Б", np.std(gray))
]

best = max(contrasts, key=lambda x: x[1])

with open(f"output_colors/{splitted_filename}/analysis.txt", "w") as f:

    diff_rg = abs(np.mean(r) - np.mean(g))
    diff_rb = abs(np.mean(r) - np.mean(b))
    if diff_rb > 30 or diff_rg > 30:
        f.write("Есть цветовой перекос. Рекомендуется использовать отдельные каналы. \n")
        f.write(f"Лучший канал: {best[0]} (контрастность: {best[1]:.1f}).")
    else:
        f.write("Баланс цветов нормальный. Можно использовать Ч/Б.")

print(f"Успешно. Результаты: ./output_colors/{splitted_filename}/.")