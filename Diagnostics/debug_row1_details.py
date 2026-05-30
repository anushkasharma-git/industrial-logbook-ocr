import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

reader = easyocr.Reader(['en'])

# Let's inspect Row 1 (y=578 to 670) and Row 2 (y=669 to 762)
# We crop the entire width of columns 0 and 1 (x from 120 to 550)
for r_name, y1, y2 in [("Row 1 (Header/Empty?)", 578, 670), ("Row 2 (First Data Row)", 669, 762)]:
    crop = img[y1:y2, 120:550]
    results = reader.readtext(crop)
    print(f"\n--- {r_name} (y={y1} to {y2}) ---")
    for res in results:
        box, text, conf = res
        abs_x1 = 120 + box[0][0]
        abs_x2 = 120 + box[2][0]
        abs_y1 = y1 + box[0][1]
        abs_y2 = y1 + box[2][1]
        print(f"  Detected Text: '{text}' conf={conf:.3f}")
        print(f"    abs_x: [{abs_x1}, {abs_x2}], abs_y: [{abs_y1}, {abs_y2}]")
