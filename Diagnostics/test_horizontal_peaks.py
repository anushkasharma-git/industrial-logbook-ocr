import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Grayscale & Adaptive threshold
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
)

# Extract horizontal lines morphology
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 1))
horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

# Sum horizontally along x from 140 to 2600 to find lines Y coordinates
lines_y_proj = np.sum(horizontal[:, 140:2600] > 128, axis=1)

# Find peaks (where horizontal lines are located)
y_lines = []
in_line = False
line_start = 0
for y, val in enumerate(lines_y_proj):
    # If more than 500 pixels in a row are horizontal lines, it is a table horizontal line!
    if not in_line and val > 500:
        line_start = y
        in_line = True
    elif in_line and val <= 500:
        y_lines.append((line_start + y) // 2)
        in_line = False

print("Detected Horizontal Line Y Coordinates:")
print(y_lines)
print(f"Total lines: {len(y_lines)}")
