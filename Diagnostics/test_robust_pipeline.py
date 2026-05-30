from pdf2image import convert_from_path
import cv2
import numpy as np
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
page = pages[0]

img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)

# Coordinates for Page 1 of the PDF (which has the 13 columns layout)
Y_TOP = 274
Y_BOTTOM = 3169
X_LEFT = 140
X_RIGHT = 2693
COLUMN_X = [0, 199, 388, 572, 759, 981, 1215, 1436, 1658, 1863, 1999, 2131, 2319, 2553]

# Slicing table
table_img = img[Y_TOP:Y_BOTTOM, X_LEFT:X_RIGHT]
gray = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
gray_inv = 255 - gray
_, thresh = cv2.threshold(gray_inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

dark = (thresh > 128).astype(np.uint8)
projection = np.sum(dark, axis=1)

ROW_MIN_GAP = 20
ROW_MIN_HEIGHT = 25
ROW_MAX_HEIGHT = 150
INK_THRESHOLD = 2

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

merged = []
for band in row_bands:
    if merged and (band[0] - merged[-1][1]) < ROW_MIN_GAP:
        merged[-1] = (merged[-1][0], band[1])
    else:
        merged.append(list(band))
row_bands = merged

print(f"Detected {len(row_bands)} row bands.")

reader = easyocr.Reader(['en'])

# Test first 3 data rows (excluding headers)
# Header is usually row_bands[0] and row_bands[1]
for r_idx in range(2, 5):
    if r_idx >= len(row_bands):
        break
    y1, y2 = row_bands[r_idx]
    row_img = table_img[y1:y2, :]
    
    print(f"\n--- Testing Data Row {r_idx-2} (y={y1} to {y2}) ---")
    for col in range(13):
        x1 = COLUMN_X[col]
        x2 = COLUMN_X[col+1]
        cell_img = row_img[:, x1:x2]
        
        # padding
        PAD = 3
        h_cell, w_cell, _ = cell_img.shape
        if h_cell > 2*PAD and w_cell > 2*PAD:
            cell_img = cell_img[PAD:-PAD, PAD:-PAD]
            
        results = reader.readtext(cell_img)
        texts = [res[1] for res in results]
        print(f"  Col {col}: '{', '.join(texts)}'")
