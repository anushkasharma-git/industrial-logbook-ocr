import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]
Y_START = 670
ROW_HEIGHT = 91.6

reader = easyocr.Reader(['en'])

# Pass 1: Global Context (table crop)
table_crop = img[500:3200, 120:2650]
results_full = reader.readtext(table_crop)

print("--- PASS 1 DETECTIONS FOR COLUMN 0 & COLUMN 1 ---")
for res in results_full:
    box, text, conf = res
    abs_x = 120 + (box[0][0] + box[2][0]) / 2
    abs_y = 500 + (box[0][1] + box[2][1]) / 2
    
    row_idx = int((abs_y - Y_START) / ROW_HEIGHT)
    if 0 <= row_idx < 18:
        col_idx = None
        for c in range(13):
            if COLUMN_BOUNDS[c] <= abs_x < COLUMN_BOUNDS[c+1]:
                col_idx = c
                break
        if col_idx in [0, 1]:
            print(f"Row {row_idx+2} (y_center={abs_y:.1f}) Col {col_idx}: '{text}' (conf={conf:.3f})")
