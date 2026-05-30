import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table parameters
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]
y1 = 669
y2 = 762

reader = easyocr.Reader(['en'])

print("--- INSPECTING ROW 1 (FIRST DATA ROW) ALL COLUMNS ---")
for col in range(13):
    x1 = COLUMN_BOUNDS[col]
    x2 = COLUMN_BOUNDS[col+1]
    
    cell_img = img[y1:y2, x1:x2]
    # Save image for verification if needed
    cv2.imwrite(f"cell_row1_col{col}.png", cell_img)
    
    cell_resized = cv2.resize(cell_img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
    results = reader.readtext(cell_resized)
    texts = [res[1] for res in results]
    print(f"  Col {col} (x=[{x1}, {x2}]): '{', '.join(texts)}'")
