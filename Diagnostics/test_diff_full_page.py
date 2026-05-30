import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table parameters
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]
Y_START = 578
ROW_HEIGHT = 91.6
NUM_ROWS = 20

# Blue isolation on the entire page
b, g, r = cv2.split(img)
diff = cv2.subtract(b, r)

# Thresh the diff
_, thresh = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)
thresh_inv = cv2.bitwise_not(thresh)

# Convert to BGR to draw colored lines
debug_img = cv2.cvtColor(thresh_inv, cv2.COLOR_GRAY2BGR)

# Draw column boundaries (vertical red lines)
for x in COLUMN_BOUNDS:
    cv2.line(debug_img, (x, int(Y_START - 50)), (x, int(Y_START + NUM_ROWS * ROW_HEIGHT + 50)), (0, 0, 255), 2)

# Draw row boundaries (horizontal green lines)
for r_idx in range(NUM_ROWS + 1):
    y = int(Y_START + r_idx * ROW_HEIGHT)
    cv2.line(debug_img, (COLUMN_BOUNDS[0] - 50, y), (COLUMN_BOUNDS[-1] + 50, y), (0, 255, 0), 2)

# Save a crop of the first 5 rows for detailed inspection
crop = debug_img[500:1150, 50:2700]
cv2.imwrite("grid_debug_diff_crop.png", crop)
print("Saved grid_debug_diff_crop.png successfully.")
