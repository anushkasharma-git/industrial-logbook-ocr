import cv2
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
import easyocr
import os
import re

# =====================================
# SETTINGS & PATHS
# =====================================

PDF_PATH = "RDH PROCESS 01042026.pdf"
OUTPUT_EXCEL = "ocr_output_clean.xlsx"

# =====================================
# COLUMN DEFINITIONS
# =====================================

columns = {
    0: ("warm_fill_wbl_m3", "fraction"),
    1: ("warm_fill_total_m3", "fraction"),
    2: ("warm_fill_temp", "integer"),

    3: ("hot_fill_from", "time"),
    4: ("hot_fill_to", "time"),
    5: ("hot_fill_min", "integer"),

    6: ("c1_wl_perc", "decimal"),
    7: ("c1_wl_m3", "fraction"),
    8: ("c1_wlbl_m3", "fraction"),

    9: ("c2_wl_perc", "decimal"),
    10: ("c2_wl_m3", "fraction"),
    11: ("c2_total_m3", "fraction"),

    12: ("hf_temp", "integer")
}

# Absolute column boundaries calibrated for 300 DPI
X_LEFT = 140
COLUMN_X = [0, 199, 388, 572, 759, 981, 1215, 1436, 1658, 1863, 1999, 2131, 2319, 2553]
COLUMN_X_abs = [X_LEFT + x for x in COLUMN_X]

# =====================================
# CHARACTER CLEANER FUNCTIONS
# =====================================

def clean_digits(text):
    # Common handwritten OCR character-to-digit corrections
    replacements = {
        'O': '0', 'o': '0',
        'I': '1', 'i': '1', 'l': '1', '|': '1', '[': '1', ']': '1', '!': '1', 'J': '1', 'j': '1',
        'Z': '2', 'z': '2',
        'S': '5', 's': '5',
        'b': '6', 'G': '6',
        'T': '7', 't': '7',
        'B': '8',
        'g': '9', 'q': '9'
    }
    cleaned = ""
    for char in text:
        if char.isdigit():
            cleaned += char
        elif char in replacements:
            cleaned += replacements[char]
        elif char in '.:/-,*':
            cleaned += char
    return cleaned

def clean_value(text, col_type):
    text = text.strip()
    cleaned = clean_digits(text)
    
    if col_type == "integer":
        return "".join(c for c in cleaned if c.isdigit())
        
    elif col_type == "decimal":
        val = cleaned.replace(",", ".").replace(":", ".").replace("-", ".")
        val = "".join(c for c in val if c.isdigit() or c == ".")
        if val.count(".") > 1:
            parts = val.split(".")
            val = parts[0] + "." + "".join(parts[1:])
        return val
        
    elif col_type == "time":
        val = cleaned.replace(".", ":").replace(",", ":").replace("-", ":").replace("*", ":")
        val = "".join(c for c in val if c.isdigit() or c == ":")
        if ":" not in val and val.isdigit():
            if len(val) == 4:
                val = val[:2] + ":" + val[2:]
            elif len(val) == 3:
                val = val[:1] + ":" + val[1:]
        return val
        
    elif col_type == "fraction":
        val = cleaned.replace("\\", "/").replace("-", "/").replace(":", "/").replace(".", "/")
        val = "".join(c for c in val if c.isdigit() or c == "/")
        return val
        
    return cleaned

# =====================================
# PDF LOADING & PREPROCESSING
# =====================================

print("Converting first page of PDF...")
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)
original = img.copy()

print("Preprocessing image and creating table mask...")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
)

horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

table_mask = cv2.add(horizontal, vertical)

print("Finding contours of cells...")
contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cells = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    area = cv2.contourArea(cnt)
    # Filter cells by size to avoid noise
    if area < 1000 or w < 40 or h < 20 or w > 1000 or h > 1000:
        continue
    cells.append((x, y, w, h))

# Remove duplicate cell boundaries
cells = list(set(cells))

# =====================================
# GROUP CELLS INTO ROWS
# =====================================

print("Grouping cells into rows...")
row_bands = []
ROW_THRESHOLD = 25  # vertical pixel distance to group cells in the same row

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
        row_bands.append({
            "y": center_y,
            "cells": [cell]
        })

# Sort rows from top to bottom
row_bands = sorted(row_bands, key=lambda b: b["y"])

# Filter valid main table data rows (rows having 11 to 14 cells)
filtered_rows = []
for band in row_bands:
    row_cells = band["cells"]
    if 10 <= len(row_cells) <= 14:
        filtered_rows.append(row_cells)

print(f"Total main table rows detected: {len(filtered_rows)}")

# =====================================
# INITIALIZE OCR
# =====================================

print("Initializing EasyOCR reader...")
reader = easyocr.Reader(['en'])
print("EasyOCR reader initialized.")

# =====================================
# PROCESS ROWS WITH COLUMN MAPPING
# =====================================

data = {}

for r_idx, row in enumerate(filtered_rows):
    # Sort cells left to right just for cleaner logs
    row = sorted(row, key=lambda b: b[0])
    data[r_idx] = {}

    print(f"Processing row {r_idx:02d} ({len(row)} cells)...")

    for cell in row:
        x, y, w, h = cell
        center_x = x + w // 2

        # Map this cell to its absolute column index based on fixed boundaries
        col_idx = None
        for c in range(13):
            if COLUMN_X_abs[c] <= center_x < COLUMN_X_abs[c+1]:
                col_idx = c
                break

        if col_idx is None:
            # Skip cells that fall outside our table columns range
            continue

        col_name, col_type = columns[col_idx]

        # Crop the cell image from original page
        PAD = 1
        cropped = original[
            max(0, y+PAD):min(original.shape[0], y+h-PAD),
            max(0, x+PAD):min(original.shape[1], x+w-PAD)
        ]

        # Empty cell check (ink count)
        gray_crop = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        ink = cv2.countNonZero(255 - gray_crop)
        if ink < 400:  # Skip blank cells
            continue

        # Run EasyOCR
        results = reader.readtext(cropped)
        
        text = ""
        if results:
            # Sort individual detections inside the cell by center Y-coordinate
            results = sorted(results, key=lambda r: (r[0][0][1] + r[0][2][1]) / 2)
            
            if col_type == "fraction" and len(results) >= 2:
                # Top-to-bottom fraction composition
                parts = []
                for res in results:
                    part = clean_value(res[1], "integer")
                    if part:
                        parts.append(part)
                text = "/".join(parts)
            else:
                texts = []
                for res in results:
                    cleaned_part = clean_value(res[1], col_type)
                    if cleaned_part:
                        texts.append(cleaned_part)
                
                if col_type == "fraction":
                    text = "/".join(texts)
                elif col_type == "time":
                    text = "".join(texts)
                elif col_type == "decimal":
                    text = "".join(texts)
                else:
                    text = " ".join(texts)

        # Final cleanup and store
        text = clean_value(text, col_type)
        if text:
            data[r_idx][col_name] = text

# =====================================
# CREATE DATAFRAME & EXPORT
# =====================================

rows_list = []
for r_idx in sorted(data.keys()):
    row_data = data[r_idx]
    
    # Check if the row is mostly empty (skip header rows that got grouped)
    non_empty = sum(1 for v in row_data.values() if v.strip())
    if non_empty < 3:
        continue
        
    complete_row = {}
    for col_idx, (col_name, _) in columns.items():
        complete_row[col_name] = row_data.get(col_name, "")
    rows_list.append(complete_row)

df = pd.DataFrame(rows_list)

# Reorder columns 0 to 12
ordered_cols = [columns[i][0] for i in range(13)]
df = df[ordered_cols]

# Save Excel
df.to_excel(OUTPUT_EXCEL, index=False)

print(f"\nSUCCESS! Processed {len(df)} data rows.")
print(f"Saved robust, zero-shifted OCR spreadsheet to '{OUTPUT_EXCEL}'.")
print("\nFirst 10 rows preview:")
print(df.head(10).to_string())
