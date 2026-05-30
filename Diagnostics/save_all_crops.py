import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 01042026.pdf"
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop Row 7 to 13
crop_r7_r13 = img[1100:1800, 50:2700]
cv2.imwrite("crop_r7_r13.png", crop_r7_r13)

# Crop Row 14 to 20
crop_r14_r20 = img[1750:2450, 50:2700]
cv2.imwrite("crop_r14_r20.png", crop_r14_r20)

print("Saved crop_r7_r13.png and crop_r14_r20.png successfully.")
