import cv2
import pytesseract
import pandas as pd
import numpy as np
import os
import re
import time

# =====================================
# TESSERACT PATH
# =====================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# =====================================
# INPUT CELL DIRECTORY
# =====================================

CELL_DIR = "structured_output/cells"

# =====================================
# DEBUG DIRECTORY
# =====================================

DEBUG_DIR = "ocr_debug"

os.makedirs(DEBUG_DIR, exist_ok=True)

# =====================================
# COLUMN DEFINITIONS
# =====================================

columns = {

    0: ("warm_fill_wbl_m3", "fraction"),
    1: ("warm_fill_total_m3", "fraction"),
    2: ("warm_fill_temp", "integer"),

    3: ("hot_fill_from", "time"),
    4: ("hot_fill_to", "time"),
    5: ("hot_fill_min", "integer"),

    6: ("c1_wl_perc", "decimal"),
    7: ("c1_wl_m3", "fraction"),
    8: ("c1_wlbl_m3", "fraction"),

    9: ("c2_wl_perc", "decimal"),
    10: ("c2_wl_m3", "fraction"),
    11: ("c2_total_m3", "fraction"),

    12: ("hf_temp", "integer")
}

# =====================================
# PREPROCESS IMAGE
# =====================================

def preprocess(img):

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # enlarge
    gray = cv2.resize(
        gray,
        None,
        fx=6,
        fy=6,
        interpolation=cv2.INTER_CUBIC
    )

    # denoise
    gray = cv2.GaussianBlur(
        gray,
        (3,3),
        0
    )

    # threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        11
    )

    # thicken handwriting
    kernel = np.ones((2,2), np.uint8)

    thresh = cv2.dilate(
        thresh,
        kernel,
        iterations=1
    )

    # invert back for tesseract
    thresh = 255 - thresh

    return thresh

# =====================================
# OCR SIMPLE VALUE
# =====================================

def ocr_simple(img, whitelist):

    config = (
        f'--oem 1 --psm 7 '
        f'-c tessedit_char_whitelist={whitelist}'
    )
    try:

        text = pytesseract.image_to_string(
            img,
            config=config
        )

    
        return text.strip()

    except Exception as e:

        print("OCR ERROR:", e)

        return ""
time.sleep(0.02)

# =====================================
# OCR FRACTION
# =====================================

def ocr_fraction(img):

    try:

        h = img.shape[0]

        # invalid image
        if h < 10:
            return ""

        # split image
        top = img[:h//2, :]
        bottom = img[h//2:, :]

        # empty safety
        if top.size == 0 or bottom.size == 0:
            return ""

        config = (
            '--oem 1 --psm 7 '
            '-c tessedit_char_whitelist=0123456789.'
        )

        top_text = pytesseract.image_to_string(
            top,
            config=config
        ).strip()

        bottom_text = pytesseract.image_to_string(
            bottom,
            config=config
        ).strip()

        # cleanup
        top_text = re.sub(
            r"[^0-9.]",
            "",
            top_text
        )

        bottom_text = re.sub(
            r"[^0-9.]",
            "",
            bottom_text
        )

        if top_text and bottom_text:
            return f"{top_text}/{bottom_text}"

        return top_text or bottom_text

    except Exception as e:

        print("FRACTION OCR ERROR:", e)

        return ""

time.sleep(0.02)   

# =====================================
# CLEAN TIME
# =====================================

def clean_time(text):

    text = text.replace(".", ":")

    text = re.sub(
        r"[^0-9:]",
        "",
        text
    )

    return text
time.sleep(0.02)
# =====================================
# MAIN OCR LOOP
# =====================================

data = {}

files = sorted(os.listdir(CELL_DIR))

for file in files:

    # only png
    if not file.endswith(".png"):
        continue

    # =====================================
    # PARSE ROW/COL
    # =====================================

    match = re.match(
        r"r(\d+)_c(\d+)\.png",
        file
    )

    if not match:
        continue

    row = int(match.group(1))
    col = int(match.group(2))

    # skip unknown columns
    if col not in columns:
        continue

    col_name, col_type = columns[col]

    # =====================================
    # LOAD IMAGE
    # =====================================

    path = os.path.join(
        CELL_DIR,
        file
    )

    img = cv2.imread(path)

    if img is None:
        continue

    # =====================================
    # PREPROCESS
    # =====================================

    processed = preprocess(img)

    # =====================================
    # SAVE DEBUG IMAGE
    # =====================================

    cv2.imwrite(
        os.path.join(DEBUG_DIR, file),
        processed
    )

    # =====================================
    # OCR BY TYPE
    # =====================================

    if col_type == "integer":

        text = ocr_simple(
            processed,
            "0123456789"
        )

    elif col_type == "decimal":

        text = ocr_simple(
            processed,
            "0123456789."
        )

    elif col_type == "time":

        text = ocr_simple(
            processed,
            "0123456789:"
        )

        text = clean_time(text)

    elif col_type == "fraction":

        text = ocr_fraction(processed)

    else:

        text = ""

    # cleanup
    text = text.strip()

    # =====================================
    # STORE DATA
    # =====================================

    if row not in data:
        data[row] = {}

    data[row][col_name] = text

    print(file, "->", text)

# =====================================
# REMOVE MOSTLY EMPTY ROWS
# =====================================

cleaned_rows = []

for row_index in sorted(data.keys()):

    row_data = data[row_index]

    non_empty = 0

    for value in row_data.values():

        if str(value).strip():
            non_empty += 1

    # skip garbage rows
    if non_empty < 4:
        continue

    cleaned_rows.append(row_data)

# =====================================
# CREATE DATAFRAME
# =====================================

df = pd.DataFrame(cleaned_rows)

# =====================================
# SAVE EXCEL
# =====================================

df.to_excel(
    "ocr_output.xlsx",
    index=False
)

print()
print("DONE")
print("Saved as ocr_output1.xlsx")
