import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Run identical row grouping as structured_extract.py
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

# Print first 5 rows coordinate details
print(f"Total main table rows: {len(filtered_rows)}")
for r_idx in range(min(5, len(filtered_rows))):
    row = filtered_rows[r_idx]
    row = sorted(row, key=lambda b: b[0])
    print(f"\nRow {r_idx}:")
    for c_idx, cell in enumerate(row[:3]):
        x, y, w, h = cell
        print(f"  Cell {c_idx}: x={x}, y={y}, w={w}, h={h}")
