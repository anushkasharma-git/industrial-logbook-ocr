import cv2
import numpy as np
from pdf2image import convert_from_path

for pdf_name in ["RDH PROCESS 01042026.pdf", "RDH PROCESS 02042026.pdf"]:
    print(f"\n======================================")
    print(f"ANALYZING: {pdf_name}")
    print(f"======================================")
    
    pages = convert_from_path(pdf_name, dpi=300)
    img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Run adaptive threshold to detect gridlines
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
    )
    
    # Horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    
    # Vertical lines
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
    
    # Group into row bands
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
    
    # Filter rows that look like our main table rows (typically 11 to 13 columns)
    filtered_rows = []
    for band in row_bands:
        row_cells = band["cells"]
        if 10 <= len(row_cells) <= 14:
            filtered_rows.append(row_cells)
            
    print(f"Total main table rows found: {len(filtered_rows)}")
    
    # Let's print row Y coordinates
    for idx, row in enumerate(filtered_rows):
        row = sorted(row, key=lambda b: b[0])
        first_cell = row[0]
        last_cell = row[-1]
        mean_y = int(np.mean([c[1] for c in row]))
        mean_h = int(np.mean([c[3] for c in row]))
        print(f"  Row {idx:02d}: mean_y={mean_y}, mean_h={mean_h}, cells_count={len(row)}, x_start={first_cell[0]}, x_end={last_cell[0] + last_cell[2]}")
