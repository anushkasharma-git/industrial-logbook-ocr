import cv2
import numpy as np
from pdf2image import convert_from_path
import os

# =====================================
# SETTINGS
# =====================================

PDF_PATH = "RDH PROCESS 01042026.pdf"

OUTPUT_DIR = "structured_output"

CELL_DIR = f"{OUTPUT_DIR}/cells"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CELL_DIR, exist_ok=True)

# =====================================
# LOAD PDF
# =====================================

pages = convert_from_path(
    PDF_PATH,
    dpi=300
)

page = pages[0]

img = np.array(page)

img = cv2.cvtColor(
    img,
    cv2.COLOR_RGB2BGR
)

original = img.copy()

debug = img.copy()

# =====================================
# GRAYSCALE
# =====================================

gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)

# =====================================
# THRESHOLD
# =====================================

thresh = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    15,
    8
)

# =====================================
# DETECT HORIZONTAL LINES
# =====================================

horizontal_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (40,1)
)

horizontal = cv2.morphologyEx(
    thresh,
    cv2.MORPH_OPEN,
    horizontal_kernel,
    iterations=2
)

# =====================================
# DETECT VERTICAL LINES
# =====================================

vertical_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1,40)
)

vertical = cv2.morphologyEx(
    thresh,
    cv2.MORPH_OPEN,
    vertical_kernel,
    iterations=2
)

# =====================================
# TABLE MASK
# =====================================

table_mask = cv2.add(
    horizontal,
    vertical
)

# =====================================
# FIND CELL CONTOURS
# =====================================

contours, hierarchy = cv2.findContours(
    table_mask,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE
)

cells = []

for cnt in contours:

    x, y, w, h = cv2.boundingRect(cnt)

    area = cv2.contourArea(cnt)

    # remove tiny noise
    if area < 1000:
        continue

    # remove tiny boxes
    if w < 40 or h < 20:
        continue

    # remove huge page contour
    if w > 1000 or h > 1000:
        continue

    cells.append((x, y, w, h))

# remove duplicates
cells = list(set(cells))

# =====================================
# SORT TOP -> BOTTOM
# =====================================

cells = sorted(
    cells,
    key=lambda b: (b[1], b[0])
)

# =====================================
# CREATE ROW BANDS
# =====================================

row_bands = []

ROW_THRESHOLD = 25

for cell in cells:

    x, y, w, h = cell

    center_y = y + h // 2

    assigned = False

    for band in row_bands:

        if abs(center_y - band["y"]) < ROW_THRESHOLD:

            band["cells"].append(cell)

            # update average row y
            ys = [
                c[1] + c[3]//2
                for c in band["cells"]
            ]

            band["y"] = int(np.mean(ys))

            assigned = True

            break

    if not assigned:

        row_bands.append({
            "y": center_y,
            "cells": [cell]
        })

# =====================================
# SORT ROWS
# =====================================

row_bands = sorted(
    row_bands,
    key=lambda b: b["y"]
)

# =====================================
# FILTER VALID DATA ROWS
# =====================================

filtered_rows = []

for band in row_bands:

    row = band["cells"]

    # sort left -> right
    row = sorted(row, key=lambda b: b[0])

    # keep only main table rows
    if 11 <= len(row) <= 13:

        filtered_rows.append(row)

# =====================================
# PROCESS ROWS
# =====================================

for r, row in enumerate(filtered_rows):

    # sort left -> right
    row = sorted(row, key=lambda b: b[0])

    for c, cell in enumerate(row):

        x, y, w, h = cell

        PAD = 2

        cropped = original[
            max(0, y+PAD):min(original.shape[0], y+h-PAD),
            max(0, x+PAD):min(original.shape[1], x+w-PAD)
        ]

        # =====================================
        # EMPTY CELL DETECTION
        # =====================================

        gray_crop = cv2.cvtColor(
            cropped,
            cv2.COLOR_BGR2GRAY
        )

        ink = cv2.countNonZero(
            255 - gray_crop
        )

        # skip empty cells
        if ink < 500:
            continue

        # =====================================
        # SAVE CELL
        # =====================================

        filename = f"r{r:02d}_c{c:02d}.png"

        cv2.imwrite(
            os.path.join(CELL_DIR, filename),
            cropped
        )

        # =====================================
        # DEBUG DRAW
        # =====================================

        cv2.rectangle(
            debug,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )

        cv2.putText(
            debug,
            f"{r},{c}",
            (x,y-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0,0,255),
            1
        )

# =====================================
# SAVE DEBUG IMAGE
# =====================================

cv2.imwrite(
    f"{OUTPUT_DIR}/debug_rows_cols.png",
    debug
)

print("DONE")