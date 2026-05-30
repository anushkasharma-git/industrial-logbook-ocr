import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table boundaries
Y_TOP = 274
Y_BOTTOM = 3169
X_LEFT = 128
X_RIGHT = 2613

table_img = img[Y_TOP:Y_BOTTOM, X_LEFT:X_RIGHT]
gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)

# Otsu binarization
gray_inv = 255 - gray
_, thresh = cv2.threshold(gray_inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Perfect vertical lines coordinates relative to X_LEFT = 128
# COLUMN_BOUNDS = [128, 318, 508, 696, ... ]
# So relative: [0, 190, 380, 568, 734, 900, 1054, 1219, 1420, 1657, 1857, 2094, 2331, 2485]
v_lines = [0, 190, 380, 568, 734, 900, 1054, 1219, 1420, 1657, 1857, 2094, 2331, 2485]

# Erase vertical lines from binarized image (set to 0)
thresh_no_vlines = thresh.copy()
for vl in v_lines:
    x_min = max(0, vl - 8)
    x_max = min(thresh_no_vlines.shape[1], vl + 8)
    thresh_no_vlines[:, x_min:x_max] = 0

# Project horizontally (count ink pixels per row)
dark = (thresh_no_vlines > 128).astype(np.uint8)
projection = np.sum(dark, axis=1)

# Find contiguous row bands where ink > threshold
# Since vertical lines are gone, the spaces between rows will have almost 0 projection!
INK_THRESHOLD = 5
ROW_MIN_HEIGHT = 40
ROW_MAX_HEIGHT = 150
ROW_MIN_GAP = 15

in_row = False
row_y = 0
row_bands = []

for y, count in enumerate(projection):
    if not in_row and count >= INK_THRESHOLD:
        row_y = y
        in_row = True
    elif in_row and count < INK_THRESHOLD:
        height = y - row_y
        if ROW_MIN_HEIGHT <= height <= ROW_MAX_HEIGHT:
            row_bands.append((row_y, y))
        in_row = False

# Merge close bands
merged = []
for band in row_bands:
    if merged and (band[0] - merged[-1][1]) < ROW_MIN_GAP:
        merged[-1] = (merged[-1][0], band[1])
    else:
        merged.append(list(band))
row_bands = merged

print(f"Detected {len(row_bands)} row bands using the perfect projection method!")
print("\nFirst 10 row bands absolute page Y ranges:")
for i, (y1, y2) in enumerate(row_bands[:10]):
    abs_y1 = Y_TOP + y1
    abs_y2 = Y_TOP + y2
    print(f"  Row {i+1}: Y=[{abs_y1}, {abs_y2}] (height={y2-y1})")
