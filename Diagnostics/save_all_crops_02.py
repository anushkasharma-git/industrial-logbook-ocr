import cv2
import numpy as np
from pdf2image import convert_from_path

PDF_PATH = "RDH PROCESS 02042026.pdf"
print("Converting second PDF to images...")
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# Crop R2 to R6
crop_r2_r6 = img[660:1140, 50:2700]
cv2.imwrite("crop_r2_r6_02.png", crop_r2_r6)

# Crop R7 to R13
crop_r7_r13 = img[1100:1800, 50:2700]
cv2.imwrite("crop_r7_r13_02.png", crop_r7_r13)

# Crop R14 to R19
crop_r14_r19 = img[1750:2400, 50:2700]
cv2.imwrite("crop_r14_r19_02.png", crop_r14_r19)

print("Saved second PDF crop files successfully.")
