import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Row R2 (first data row, y=[670, 762])
y1, y2 = 670, 762
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

reader = easyocr.Reader(['en'])

print("--- RAW DETECTIONS IN ROW R2 (COL 0 & COL 1) ---")

# Pass 1: crop the region
crop_full = img[500:900, 120:600]
results_full = reader.readtext(crop_full)
print("\nPass 1 (cropped table region):")
for res in results_full:
    box, text, conf = res
    abs_x = 120 + (box[0][0] + box[2][0]) / 2
    abs_y = 500 + (box[0][1] + box[2][1]) / 2
    print(f"  abs_x={abs_x:.1f}, abs_y={abs_y:.1f}, text='{text}', conf={conf:.3f}")

# Pass 2: crop cells directly
print("\nPass 2 (cropped cells directly at 3.0x):")
for col in [0, 1]:
    x1, x2 = COLUMN_BOUNDS[col], COLUMN_BOUNDS[col+1]
    cell = img[y1:y2, x1:x2]
    cell_resized = cv2.resize(cell, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
    results_crop = reader.readtext(cell_resized)
    print(f"  Col {col}:")
    for res in results_crop:
        print(f"    text='{res[1]}', conf={res[2]:.3f}, box={res[0]}")
