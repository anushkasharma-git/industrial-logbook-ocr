import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Row 0 (R2) Col 0
y1, y2 = 670, 762
x1, x2 = 128, 318

reader = easyocr.Reader(['en'])

print("--- TESTING FORCE FALLBACK ON ROW 0 COL 0 ---")
# Crop with expanded boundaries
y1_exp = max(0, y1 - 4)
y2_exp = min(img.shape[0], y2 + 6)
cell_img = img[y1_exp:y2_exp, x1:x2]

cell_resized = cv2.resize(cell_img, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
results = reader.readtext(cell_resized)
for res in results:
    print(f"Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")
