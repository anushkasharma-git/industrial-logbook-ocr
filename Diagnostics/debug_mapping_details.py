import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Precise physical column boundaries from our vertical line test!
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

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

row_bands = []
ROW_THRESHOLD = 25
for cell in cells:
    x, y, w, h = cell
    center_y = y + h // 2
    assigned = False
    for band in row_bands:
        if abs(center_y - band["y"]) < ROW_THRESHOLD:
            band["cells"].append(cell)
            ys = [c[1] + c[3] // 2 for c in band["cells"]]
            band["y"] = int(np.mean(ys))
            assigned = True
            break
    if not assigned:
        row_bands.append({"y": center_y, "cells": [cell]})

row_bands = sorted(row_bands, key=lambda b: b["y"])
filtered_rows = []
for band in row_bands:
    row_cells = band["cells"]
    if 10 <= len(row_cells) <= 14:
        filtered_rows.append(row_cells)

reader = easyocr.Reader(['en'])

# Let's inspect rows 1, 2, 3 in detail
for r_idx in range(1, 4):
    row = filtered_rows[r_idx]
    row = sorted(row, key=lambda b: b[0])
    print(f"\n--- Row {r_idx} (y range: {min(c[1] for c in row)} to {max(c[1]+c[3] for c in row)}) ---")
    for cell in row:
        x, y, w, h = cell
        center_x = x + w // 2
        
        # Find which column it belongs to using our perfect COLUMN_BOUNDS
        col_idx = None
        for c in range(13):
            if COLUMN_BOUNDS[c] <= center_x < COLUMN_BOUNDS[c+1]:
                col_idx = c
                break
                
        # Crop the cell and resize 2x
        cropped = img[y:y+h, x:x+w]
        cropped_resized = cv2.resize(cropped, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        
        results = reader.readtext(cropped_resized)
        texts = [res[1] for res in results]
        
        print(f"  Cell: x={x}, w={w}, center_x={center_x} -> MAPPED TO COL {col_idx}: '{', '.join(texts)}'")
