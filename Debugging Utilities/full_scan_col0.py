import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop the entire Column 0 from y = 578 to 2400
col0_crop = img[578:2400, 128:318]

# Resize 2x
col0_resized = cv2.resize(col0_crop, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

reader = easyocr.Reader(['en'])
results = reader.readtext(col0_resized)

print("--- ALL DETECTED TEXT IN COLUMN 0 ---")
for res in results:
    box, text, conf = res
    # Map back to cropped coordinates (divide by 2)
    y_center = 578 + (box[0][1] + box[2][1]) / 4
    x_center = 128 + (box[0][0] + box[2][0]) / 4
    print(f"y_center={y_center:.1f}, text='{text}', conf={conf:.3f}, box={box}")
