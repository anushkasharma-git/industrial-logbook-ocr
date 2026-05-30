import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

reader = easyocr.Reader(['en'])

# Crop the first column (x from 120 to 320) from y = 500 to 1000
# This covers Row 1, Row 2, Row 3, Row 4 in column 0!
crop = img[500:1100, 120:320]
cv2.imwrite("first_col_crop.png", crop)

results = reader.readtext(crop)
print("EasyOCR results on first column top rows (y=500 to 1100, x=120 to 320):")
for res in results:
    box, text, conf = res
    # Adjust coordinates to page absolute
    abs_y1 = 500 + box[0][1]
    abs_y2 = 500 + box[2][1]
    print(f"  Text: '{text}' conf={conf:.3f} abs_y=[{abs_y1}, {abs_y2}]")
