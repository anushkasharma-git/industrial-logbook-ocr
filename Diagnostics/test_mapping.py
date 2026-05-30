import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table mask and cell detection exactly like structured_extract.py
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

table_mask = cv2.add(horizontal, vertical)

contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cells = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    area = cv2.contourArea(cnt)
    if area < 1000 or w < 40 or h < 20 or w > 1000 or h > 1000:
        continue
    cells.append((x, y, w, h))

cells = list(set(cells))

# Absolute column boundaries from CORRECTED_NOTEBOOK.py
X_LEFT = 140
COLUMN_X = [0, 199, 388, 572, 759, 981, 1215, 1436, 1658, 1863, 1999, 2131, 2319, 2553]
COLUMN_X_abs = [X_LEFT + x for x in COLUMN_X]

print(f"Total cells detected: {len(cells)}")
print("\nMapping first 20 cells to columns:")
for i, cell in enumerate(cells[:20]):
    x, y, w, h = cell
    center_x = x + w // 2
    
    # Find which column it belongs to
    col_idx = None
    for c in range(13):
        if COLUMN_X_abs[c] <= center_x < COLUMN_X_abs[c+1]:
            col_idx = c
            break
            
    print(f"Cell {i}: x={x} w={w} center_x={center_x} -> mapped to col={col_idx}")
