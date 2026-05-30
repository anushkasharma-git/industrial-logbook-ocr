import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Blue isolation
b, g, r = cv2.split(img)
diff = cv2.subtract(b, r)
_, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
thresh_inv = cv2.bitwise_not(thresh)

# Mathematical grid settings
Y_START = 578
ROW_HEIGHT = 91.6
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

reader = easyocr.Reader(['en'])

# Test first data row (Row R2, between y = 669 and y = 760)
y1 = 669
y2 = 760

print("--- TESTING ALL COLUMNS IN ROW 2 WITH BLUE ISOLATION ---")
for col in range(13):
    x1 = COLUMN_BOUNDS[col]
    x2 = COLUMN_BOUNDS[col+1]
    
    # Crop the cell
    PAD = 2
    cell = thresh_inv[y1+PAD:y2-PAD, x1+PAD:x2-PAD]
    
    # Resize 2x
    cell_resized = cv2.resize(cell, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # Run EasyOCR
    results = reader.readtext(cell_resized)
    texts = [res[1] for res in results]
    print(f"Col {col} (x=[{x1}, {x2}]): {texts}")
