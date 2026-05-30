import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop Row 2 Col 2 (x=[508, 696], y=[669, 762])
cell = img[669:762, 508:696]
cv2.imwrite("col2_debug.png", cell)

reader = easyocr.Reader(['en'])

print("--- TESTING COL 2 R2 ---")
# 1. Test different scales
for scale in [1.0, 1.5, 2.0, 3.0, 4.0]:
    resized = cv2.resize(cell, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    results = reader.readtext(resized)
    print(f"Scale {scale}x BGR: {[res[1] for res in results]}")

# 2. Test different paddings
for pad_y in [0, 2, 4, 6]:
    for pad_x in [0, 4, 8]:
        crop = img[669+pad_y:762-pad_y, 508+pad_x:696-pad_x]
        resized = cv2.resize(crop, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        results = reader.readtext(resized)
        print(f"pad_y={pad_y}, pad_x={pad_x}: {[res[1] for res in results]}")
