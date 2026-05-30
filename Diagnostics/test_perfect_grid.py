from pdf2image import convert_from_path
import cv2
import numpy as np
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Mathematical grid settings
Y_START = 578
ROW_HEIGHT = 91.6  # average height
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]

reader = easyocr.Reader(['en'])

# Test the first 4 rows in Column 0
for r in range(4):
    y1 = int(Y_START + r * ROW_HEIGHT)
    y2 = int(y1 + ROW_HEIGHT)
    x1 = COLUMN_BOUNDS[0]
    x2 = COLUMN_BOUNDS[1]
    
    cell_img = img[y1:y2, x1:x2]
    # Resize 2x for high quality HTR
    cell_resized = cv2.resize(cell_img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    
    results = reader.readtext(cell_resized)
    texts = [res[1] for res in results]
    print(f"Row {r+1} COL 0 crop (y=[{y1}, {y2}], x=[{x1}, {x2}]):")
    print(f"  Detected text parts: {texts}")
