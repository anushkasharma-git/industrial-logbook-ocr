import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table mask like structured_extract.py
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(
    gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
)
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)

# Row bands (we know the Y coords from debug_row_heights.py)
rows_y = [
    (578, 670), # Row 1
    (669, 762), # Row 2
    (761, 854), # Row 3
    (853, 946)  # Row 4
]

for i, (y1, y2) in enumerate(rows_y):
    row_vert = vertical[y1:y2, :]
    # Sum column-wise
    col_proj = np.sum(row_vert > 128, axis=0)
    
    # Find peaks (vertical lines) where projection is high
    peaks = []
    in_peak = False
    peak_start = 0
    for x, val in enumerate(col_proj):
        if not in_peak and val > 5:
            peak_start = x
            in_peak = True
        elif in_peak and val <= 5:
            peaks.append((peak_start + x) // 2)
            in_peak = False
            
    print(f"\nRow {i+1} (y={y1} to {y2}) detected vertical line X coords:")
    print(peaks)
