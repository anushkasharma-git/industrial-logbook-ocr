import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

y1, y2 = 669, 762
x1, x2 = 128, 318  # Col 0 (contains 190/200)

reader = easyocr.Reader(['en'])

print("--- PADDING TESTS ON ROW 2 COL 0 (190/200) ---")

for pad_y in [1, 3, 5, 8]:
    for pad_x in [1, 5, 10]:
        crop = img[y1+pad_y:y2-pad_y, x1+pad_x:x2-pad_x]
        crop_resized = cv2.resize(crop, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
        results = reader.readtext(crop_resized)
        texts = [res[1] for res in results]
        print(f"y_pad={pad_y}, x_pad={pad_x}: {texts}")
