from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
reader = easyocr.Reader(['en'])

for i, page in enumerate(pages):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    # Crop the top portion of the page to read headers
    header_crop = img[100:600, :]
    results = reader.readtext(header_crop)
    print(f"\n--- Page {i+1} Top Headers ---")
    detected_texts = [res[1] for res in results if len(res[1]) > 2]
    print(", ".join(detected_texts[:20]))
