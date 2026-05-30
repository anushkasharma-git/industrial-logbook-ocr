import cv2
import numpy as np
from pdf2image import convert_from_path
import os

# =========================
# SETTINGS
# =========================

PDF_PATH = "RDH PROCESS 01042026.pdf"

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(f"{OUTPUT_DIR}/cells", exist_ok=True)

# =========================
# PDF -> IMAGE
# =========================

pages = convert_from_path(PDF_PATH, dpi=300)

# ONLY FIRST PAGE FOR NOW
page = pages[0]

img = np.array(page)

# convert RGB -> BGR
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

original = img.copy()

# =========================
# GRAYSCALE
# =========================

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# =========================
# THRESHOLD
# =========================

thresh = cv2.adaptiveThreshold(
    gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY_INV,
    15,
    8
)

cv2.imwrite(f"{OUTPUT_DIR}/1_threshold.png", thresh)

# =========================
# DETECT HORIZONTAL LINES
# =========================

horizontal_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (40, 1)
)

horizontal = cv2.morphologyEx(
    thresh,
    cv2.MORPH_OPEN,
    horizontal_kernel,
    iterations=2
)

cv2.imwrite(f"{OUTPUT_DIR}/2_horizontal.png", horizontal)

# =========================
# DETECT VERTICAL LINES
# =========================

vertical_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1, 40)
)

vertical = cv2.morphologyEx(
    thresh,
    cv2.MORPH_OPEN,
    vertical_kernel,
    iterations=2
)

cv2.imwrite(f"{OUTPUT_DIR}/3_vertical.png", vertical)

# =========================
# COMBINE TABLE LINES
# =========================

table_mask = cv2.add(horizontal, vertical)

cv2.imwrite(f"{OUTPUT_DIR}/4_table_mask.png", table_mask)

# =========================
# FIND CELL CONTOURS
# =========================

contours, hierarchy = cv2.findContours(
    table_mask,
    cv2.RETR_TREE,
    cv2.CHAIN_APPROX_SIMPLE
)

# draw boxes
debug = original.copy()

cell_count = 0

cells = []

for cnt in contours:

    x, y, w, h = cv2.boundingRect(cnt)

    # FILTER SMALL NOISE
    if w < 40 or h < 20:
        continue

    # FILTER HUGE BOX
    if w > 1000 or h > 1000:
        continue

    cells.append((x, y, w, h))

# SORT TOP TO BOTTOM
cells = sorted(cells, key=lambda b: (b[1], b[0]))

# =========================
# SAVE CELLS
# =========================

for i, (x, y, w, h) in enumerate(cells):

    cv2.rectangle(
        debug,
        (x, y),
        (x + w, y + h),
        (0, 255, 0),
        2
    )

    cell = original[y:y+h, x:x+w]

    cv2.imwrite(
        f"{OUTPUT_DIR}/cells/cell_{i}.png",
        cell
    )

    cell_count += 1

# =========================
# SAVE DEBUG IMAGE
# =========================

cv2.imwrite(f"{OUTPUT_DIR}/5_detected_cells.png", debug)

print("TOTAL CELLS:", cell_count)

print("DONE")
