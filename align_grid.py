import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Convert to grayscale and invert
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                cv2.THRESH_BINARY_INV, 51, 15)

# Horizontal projection profile to find horizontal lines
horizontal_sum = np.sum(thresh, axis=1)

# Find peaks corresponding to horizontal table lines
# Let's search in the y-range of 500 to 2500
peaks = []
for y in range(500, 2500):
    if horizontal_sum[y] > 200000:  # Strong horizontal line peak
        # Non-maximum suppression to find local maxima
        is_max = True
        for dy in range(-10, 11):
            if horizontal_sum[y + dy] > horizontal_sum[y]:
                is_max = False
                break
        if is_max and y not in peaks:
            peaks.append(y)

print("--- DETECTED HORIZONTAL GRID LINE Y-COORDINATES ---")
print("Peaks found:", sorted(peaks))
