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

# Run hybrid logic for r=1, col=0
r = 1
col = 0
y1 = int(Y_START + r * ROW_HEIGHT)
y2 = int(y1 + ROW_HEIGHT)
x1 = COLUMN_BOUNDS[col]
x2 = COLUMN_BOUNDS[col+1]

# Pass 1: Global Context (table crop)
table_crop = img[500:3200, 120:2650]
results_full = reader.readtext(table_crop)
pass1_detections = []
for res in results_full:
    box, text, conf = res
    abs_x = 120 + (box[0][0] + box[2][0]) / 2
    abs_y = 500 + (box[0][1] + box[2][1]) / 2
    row_idx = int((abs_y - Y_START) / ROW_HEIGHT)
    if row_idx == r:
        col_idx = None
        for c in range(13):
            if COLUMN_BOUNDS[c] <= abs_x < COLUMN_BOUNDS[c+1]:
                col_idx = c
                break
        if col_idx == col:
            pass1_detections.append((abs_y, text, conf))

# Pass 2: Cell-cropped directly
PAD = 2
cell_img = img[y1+PAD:y2-PAD, x1+PAD:x2-PAD]
cell_resized = cv2.resize(cell_img, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
results_crop = reader.readtext(cell_resized)
pass2_detections = []
for rc in results_crop:
    box_c, text_c, conf_c = rc
    local_y_center = (box_c[0][1] + box_c[2][1]) / 6
    abs_y_c = y1 + PAD + local_y_center
    pass2_detections.append((abs_y_c, text_c, conf_c))

print("Pass 1 detections:", pass1_detections)
print("Pass 2 detections:", pass2_detections)
