import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop Row 2 Col 0
cell = img[669:762, 128:318]

# Split channels
b, g, r = cv2.split(cell)

# Compute difference to isolate blue ink
# Blue ink has high B, low R. Grey grid and white background have B ≈ R.
diff = cv2.subtract(b, r)

# Invert diff so handwriting is dark on white
diff_inv = cv2.bitwise_not(diff)

# Binarize using Otsu to get pure black handwriting on pure white background
_, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh_inv = cv2.bitwise_not(thresh)

# Save images to verify grid line removal
cv2.imwrite("diff_isolated.png", diff_inv)
cv2.imwrite("diff_thresh.png", thresh_inv)

reader = easyocr.Reader(['en'])

print("--- TESTING BLUE INK ISOLATION ---")
for name, test_img in [("BGR Original", cell), 
                       ("Diff (isolated)", diff_inv), 
                       ("Diff Thresh (pure black/white)", thresh_inv)]:
    # Resize 2x
    resized = cv2.resize(test_img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    results = reader.readtext(resized)
    print(f"\nImage: {name}")
    if not results:
        print("  (No text detected)")
    for res in results:
        print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")
