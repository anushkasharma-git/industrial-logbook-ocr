from pdf2image import convert_from_path
import os

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
print(f"Total pages: {len(pages)}")
for i, page in enumerate(pages):
    print(f"Page {i+1} size: {page.size}")
