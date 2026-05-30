import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Row 2 (y=[669, 762])
y1 = 669
y2 = 762
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

reader = easyocr.Reader(['en'])

print("--- TESTING SCALE 3.0x ON ROW 2 ---")
for col in range(13):
    x1 = COLUMN_BOUNDS[col]
    x2 = COLUMN_BOUNDS[col+1]
    
    cell = img[y1:y2, x1:x2]
    # Resize 3x
    cell_resized = cv2.resize(cell, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
    
    results = reader.readtext(cell_resized)
    texts = [res[1] for res in results]
    print(f"Col {col} (3.0x): {texts}")
