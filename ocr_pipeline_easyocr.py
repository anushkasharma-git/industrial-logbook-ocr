import easyocr
import cv2
import pandas as pd
import numpy as np
import os
import re

# =====================================
# INPUT CELL DIRECTORY
# =====================================

CELL_DIR = "structured_output/cells"

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
# CHARACTER CLEANER FUNCTIONS
# =====================================

def clean_digits(text):
    # Common handwritten text recognition misread replacements
    replacements = {
        'O': '0', 'o': '0',
        'I': '1', 'i': '1', 'l': '1', '|': '1', '[': '1', ']': '1', '!': '1', 'J': '1', 'j': '1',
        'Z': '2', 'z': '2',
        'S': '5', 's': '5',
        'b': '6', 'G': '6',
        'T': '7', 't': '7',
        'B': '8',
        'g': '9', 'q': '9'
    }
    cleaned = ""
    for char in text:
        if char.isdigit():
            cleaned += char
        elif char in replacements:
            cleaned += replacements[char]
        elif char in '.:/-,*':
            cleaned += char
    return cleaned

def clean_value(text, col_type):
    text = text.strip()
    cleaned = clean_digits(text)
    
    if col_type == "integer":
        # Keep only digits
        return "".join(c for c in cleaned if c.isdigit())
        
    elif col_type == "decimal":
        # Replace common separators with dot
        val = cleaned.replace(",", ".").replace(":", ".").replace("-", ".")
        val = "".join(c for c in val if c.isdigit() or c == ".")
        # Keep only the first dot if multiple exist
        if val.count(".") > 1:
            parts = val.split(".")
            val = parts[0] + "." + "".join(parts[1:])
        return val
        
    elif col_type == "time":
        # Replace separators with colon
        val = cleaned.replace(".", ":").replace(",", ":").replace("-", ":").replace("*", ":")
        val = "".join(c for c in val if c.isdigit() or c == ":")
        
        # If no colon but 3 or 4 digits, insert colon
        if ":" not in val and val.isdigit():
            if len(val) == 4:
                val = val[:2] + ":" + val[2:]
            elif len(val) == 3:
                val = val[:1] + ":" + val[1:]
        return val
        
    elif col_type == "fraction":
        # Standard fraction format
        val = cleaned.replace("\\", "/").replace("-", "/").replace(":", "/").replace(".", "/")
        val = "".join(c for c in val if c.isdigit() or c == "/")
        return val
        
    return cleaned

# =====================================
# MAIN PIPELINE
# =====================================

print("Initializing EasyOCR reader...")
reader = easyocr.Reader(['en'])
print("EasyOCR reader initialized.")

data = {}

files = sorted(os.listdir(CELL_DIR))

print("Processing cells...")
cell_count = 0

for file in files:
    if not file.endswith(".png"):
        continue

    # Parse row/col indices from filename (e.g. r02_c05.png)
    match = re.match(r"r(\d+)_c(\d+)\.png", file)
    if not match:
        continue

    row = int(match.group(1))
    col = int(match.group(2))

    if col not in columns:
        continue

    col_name, col_type = columns[col]
    path = os.path.join(CELL_DIR, file)
    
    img = cv2.imread(path)
    if img is None:
        continue

    # Run EasyOCR
    results = reader.readtext(img)
    
    text = ""
    if results:
        # Sort detections by center y-coordinate (top-to-bottom)
        results = sorted(results, key=lambda r: (r[0][0][1] + r[0][2][1]) / 2)
        
        if col_type == "fraction" and len(results) >= 2:
            # If multiple detections in a fraction cell, join them with a slash
            parts = []
            for res in results:
                part = clean_value(res[1], "integer")  # treat each part as integer
                if part:
                    parts.append(part)
            text = "/".join(parts)
        else:
            # Otherwise, combine detections or use the single one
            texts = []
            for res in results:
                cleaned_part = clean_value(res[1], col_type)
                if cleaned_part:
                    texts.append(cleaned_part)
            
            if col_type == "fraction":
                text = "/".join(texts)
            elif col_type == "time":
                text = "".join(texts)
            elif col_type == "decimal":
                text = "".join(texts)
            else:
                text = " ".join(texts)
                
    # Final cleanup of the resulting text
    text = clean_value(text, col_type)

    if row not in data:
        data[row] = {}

    data[row][col_name] = text
    cell_count += 1
    if cell_count % 50 == 0:
        print(f"Processed {cell_count} cells...")

print("All cells processed. Generating dataframe...")

# =====================================
# CREATE DATAFRAME
# =====================================

rows_list = []
for row_idx in sorted(data.keys()):
    row_data = data[row_idx]
    
    # Fill in missing columns for this row with empty string
    complete_row = {}
    for col_idx, (col_name, _) in columns.items():
        complete_row[col_name] = row_data.get(col_name, "")
        
    rows_list.append(complete_row)

df = pd.DataFrame(rows_list)

# Reorder columns to match the index 0 to 12
ordered_cols = [columns[i][0] for i in range(13)]
df = df[ordered_cols]

# =====================================
# SAVE EXCEL
# =====================================

output_path = "ocr_output_easyocr.xlsx"
df.to_excel(output_path, index=False)

print(f"\nSUCCESS! Processed {cell_count} cells.")
print(f"Saved highly accurate OCR output as '{output_path}'.")
print("\nFirst 10 rows preview:")
print(df.head(10).to_string())
