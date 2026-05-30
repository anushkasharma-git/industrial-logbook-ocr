import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr

PDF_PATH = "RDH PROCESS 02042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Table crop
table_crop = img[500:3200, 120:2650]
reader = easyocr.Reader(['en'])
results = reader.readtext(table_crop)

print(f"Total detections: {len(results)}")

# Write all detections to a text file for easy inspection
with open("all_detections_02.txt", "w") as f:
    for res in sorted(results, key=lambda x: (x[0][0][1], x[0][0][0])):
        box, text, conf = res
        abs_x = 120 + (box[0][0] + box[2][0]) / 2
        abs_y = 500 + (box[0][1] + box[2][1]) / 2
        f.write(f"abs_x={abs_x:.1f}, abs_y={abs_y:.1f}, text='{text}' (conf={conf:.2f})\n")

print("Saved all detections to all_detections_02.txt")
