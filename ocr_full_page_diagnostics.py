import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table parameters
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]
Y_START = 578
ROW_HEIGHT = 91.6

reader = easyocr.Reader(['en'])

# Crop the whole table from y = 500 to 3200, x = 120 to 2650
table_crop = img[500:3200, 120:2650]
print("Running EasyOCR on the entire table page...")
results = reader.readtext(table_crop)

print(f"\nDetected {len(results)} text blocks. Mapping them to our mathematical grid:")

row_data = {}
for res in results:
    box, text, conf = res
    # Page absolute coordinates
    abs_x = 120 + (box[0][0] + box[2][0]) / 2
    abs_y = 500 + (box[0][1] + box[2][1]) / 2
    
    # Map to row index
    row_idx = int((abs_y - Y_START) / ROW_HEIGHT)
    if row_idx < 0 or row_idx >= 20:
        continue
        
    # Map to column index
    col_idx = None
    for c in range(13):
        if COLUMN_BOUNDS[c] <= abs_x < COLUMN_BOUNDS[c+1]:
            col_idx = c
            break
            
    if col_idx is None:
        continue
        
    if row_idx not in row_data:
        row_data[row_idx] = {}
    if col_idx not in row_data[row_idx]:
        row_data[row_idx][col_idx] = []
        
    row_data[row_idx][col_idx].append((abs_y, text, conf))

# Print mapped data sorted by row and column
for r in sorted(row_data.keys()):
    print(f"\nRow {r+1} (approx y={int(Y_START + r*ROW_HEIGHT)}):")
    cols = row_data[r]
    for c in sorted(cols.keys()):
        # Sort vertically inside the cell
        sorted_texts = sorted(cols[c], key=lambda x: x[0])
        text_strs = [f"'{t[1]}' ({t[2]:.2f})" for t in sorted_texts]
        print(f"  Col {c}: {', '.join(text_strs)}")
