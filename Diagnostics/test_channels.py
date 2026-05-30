import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop the first column first data row cell (Row 2 COL 0)
cell = img[669:762, 128:318]

# Extract channels
b, g, r = cv2.split(cell)
gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)

reader = easyocr.Reader(['en'])

# Test EasyOCR on each channel
channels = {
    "BGR Original": cell,
    "Grayscale": gray,
    "Blue Channel": b,
    "Green Channel": g,
    "Red Channel (absorbs blue ink)": r
}

print("--- CHANNEL TEST FOR HANDWRITING CONTRAST ---")
for name, img_ch in channels.items():
    # Resize 2x
    img_resized = cv2.resize(img_ch, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    # Run EasyOCR
    results = reader.readtext(img_resized)
    print(f"\nChannel: {name}")
    if not results:
        print("  (No text detected)")
    for res in results:
        print(f"  Text: '{res[1]}' conf={res[2]:.3f}")
