from pdf2image import convert_from_path
import cv2
import numpy as np
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
SCALE = 400 / 300

print("Rendering page at 400 DPI...")
pages = convert_from_path(PDF_PATH, dpi=400)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Coordinates of Cell r02_c00 (Row 1 column 0, which has y=669, x=129, w=189, h=93 at 300 DPI)
x = int(129 * SCALE)
y = int(669 * SCALE)
w = int(189 * SCALE)
h = int(93 * SCALE)

print(f"Cropping cell at 400 DPI (x={x}, y={y}, w={w}, h={h})...")
cell_img = img[y:y+h, x:x+w]
cv2.imwrite("cell_r02_c00_high_dpi.png", cell_img)

reader = easyocr.Reader(['en'])
results = reader.readtext(cell_img)

print("\nEasyOCR results on 400 DPI cell crop:")
if not results:
    print("  (No text detected)")
for res in results:
    box, text, conf = res
    print(f"  Text: '{text}' conf={conf:.3f} box={box}")
