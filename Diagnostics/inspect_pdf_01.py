from pdf2image import convert_from_path
import easyocr
import numpy as np
import cv2

PDF_PATH = "RDH PROCESS 01042026.pdf"
print(f"Converting pages for {PDF_PATH}...")
pages = convert_from_path(PDF_PATH, dpi=300)
print(f"Total pages in {PDF_PATH}: {len(pages)}")

reader = easyocr.Reader(['en'])

for i, page in enumerate(pages):
    img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
    print(f"Page {i+1} shape: {img.shape}")
    
    # Read the top portion to find out what page this is
    header_crop = img[100:600, :]
    results = reader.readtext(header_crop)
    print(f"\n--- Page {i+1} Top Headers ---")
    detected_texts = [res[1] for res in results if len(res[1]) > 2]
    print(", ".join(detected_texts[:20]))
