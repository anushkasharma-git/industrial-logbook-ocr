from pdf2image import convert_from_path
import numpy as np
import cv2
import easyocr

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

reader = easyocr.Reader(['en'])

# Let's crop row 1 (which corresponds to r=0 in the code, because Y_START is the top of data rows)
# Wait, let's crop the first 3 rows
for r in range(3):
    y1 = int(670 + r * 91.6)
    y2 = int(y1 + 91.6)
    
    # We will crop the entire row width from COLUMN_BOUNDS[0] (128) to COLUMN_BOUNDS[13] (2613)
    row_img = img[y1:y2, 128:2613]
    cv2.imwrite(f"row_{r+1}_crop.png", row_img)
    print(f"Saved row_{r+1}_crop.png")
    
    # Now let's crop and print the OCR of each cell in these first few columns
    row_texts = []
    for col in range(13):
        x1 = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613][col]
        x2 = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613][col+1]
        
        cell_img = img[y1:y2, x1:x2]
        res = reader.readtext(cell_img)
        txt = " | ".join([r[1] for r in res]) if res else "EMPTY"
        row_texts.append(f"Col {col}: {txt}")
        
    print(f"\n--- Row {r+1} Cells OCR ---")
    print("\n".join(row_texts))
