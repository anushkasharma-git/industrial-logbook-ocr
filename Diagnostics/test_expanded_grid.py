import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

Y_START = 578
ROW_HEIGHT = 91.6
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

reader = easyocr.Reader(['en'])

print("--- TESTING EXPANDED ROW CROPS ON COL 0 & COL 1 ---")
for r in range(1, 6):  # Test first 5 data rows (R2 to R6)
    y1 = int(Y_START + r * ROW_HEIGHT)
    y2 = int(y1 + ROW_HEIGHT)
    
    # Expand vertical crop: 4 pixels above, 6 pixels below
    y1_exp = y1 - 4
    y2_exp = y2 + 6
    
    for col in [0, 1]:
        x1 = COLUMN_BOUNDS[col]
        x2 = COLUMN_BOUNDS[col+1]
        
        cell = img[y1_exp:y2_exp, x1:x2]
        cell_resized = cv2.resize(cell, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
        results = reader.readtext(cell_resized)
        texts = [res[1] for res in results]
        print(f"Row {r+1} Col {col} (y=[{y1_exp}, {y2_exp}]): {texts}")
