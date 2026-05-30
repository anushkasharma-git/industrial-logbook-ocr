import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop Row 2 Cell 0 (Column 0, bottom part, where 'Bd' was detected)
# Coordinates for Row 2 Cell 0 are x=[128, 318], y=[669, 762]
cell = img[669:762, 128:318]

cv2.imwrite("original_cell.png", cell)

reader = easyocr.Reader(['en'])

# Run different preprocessing techniques and test EasyOCR on each
print("--- PREPROCESSING TESTS ON ROW 2 CELL 0 ---")

# 1. Original
results = reader.readtext(cell)
print("\n1. Original cropped cell:")
for res in results:
    print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")

# 2. Resize x2
cell_resized = cv2.resize(cell, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
results = reader.readtext(cell_resized)
print("\n2. Resized 2x cell:")
for res in results:
    print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")

# 3. Grayscale + Resize x2 + Threshold
gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
thresh_resized = cv2.resize(thresh, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
results = reader.readtext(thresh_resized)
print("\n3. Binarized + Resized 2x cell:")
for res in results:
    print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")

# 4. Grayscale + Resize x2 + Otsu
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
otsu_resized = cv2.resize(otsu, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
results = reader.readtext(otsu_resized)
print("\n4. Otsu Binarized + Resized 2x cell:")
for res in results:
    print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")
