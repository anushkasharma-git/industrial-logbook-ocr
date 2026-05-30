import cv2
import pytesseract
import numpy as np

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =====================================
# LOAD IMAGE
# =====================================

img = cv2.imread("cell_test1.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# enlarge
gray = cv2.resize(
    gray,
    None,
    fx=5,
    fy=5,
    interpolation=cv2.INTER_CUBIC
)

# threshold
_, thresh = cv2.threshold(
    gray,
    0,
    255,
    cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)

# =====================================
# DETECT FRACTION LINE USING CONTOURS
# =====================================

contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

line_y = None
max_width = 0

for cnt in contours:

    x, y, w, h = cv2.boundingRect(cnt)

    # horizontal line candidate
    if w > 100 and h < 20:

        if w > max_width:
            max_width = w
            line_y = y + h // 2

# fallback
if line_y is None:
    line_y = thresh.shape[0] // 2

# debug
debug = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

cv2.line(
    debug,
    (0, line_y),
    (debug.shape[1], line_y),
    (0,255,0),
    2
)

cv2.imwrite("debug_line1.2.png", debug)

# =====================================
# SPLIT TOP/BOTTOM
# =====================================

top = thresh[:line_y-5, :]
bottom = thresh[line_y+5:, :]

cv2.imwrite("top.png", top)
cv2.imwrite("bottom.png", bottom)

# =====================================
# OCR CONFIG
# =====================================

config = (
    "--psm 7 "
    "-c tessedit_char_whitelist=0123456789."
)

# =====================================
# OCR TOP
# =====================================

top_text = pytesseract.image_to_string(
    top,
    config=config
).strip()

# =====================================
# OCR BOTTOM
# =====================================

bottom_text = pytesseract.image_to_string(
    bottom,
    config=config
).strip()

# =====================================
# FINAL FRACTION
# =====================================

final = f"{top_text}/{bottom_text}"

print("RESULT:")
print(final)