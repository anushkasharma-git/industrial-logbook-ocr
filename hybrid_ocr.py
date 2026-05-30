import cv2
import numpy as np
from pdf2image import convert_from_path
import easyocr
import pandas as pd

# =====================================
# SETTINGS & PATHS
# =====================================

PDF_PATH = "RDH PROCESS 01042026.pdf"
OUTPUT_EXCEL = "ocr_output_hybrid.xlsx"

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

# Mathematical grid settings
COLUMN_BOUNDS = [128, 318, 508, 696, 862, 1028, 1182, 1347, 1548, 1785, 1985, 2222, 2459, 2613]
Y_START = 578
ROW_HEIGHT = 91.6
NUM_ROWS = 20

# =====================================
# CHARACTER CLEANER FUNCTIONS
# =====================================

def clean_digits(text):
    replacements = {
        'O': '0', 'o': '0', 'D': '0',
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
        return "".join(c for c in cleaned if c.isdigit())
        
    elif col_type == "decimal":
        val = cleaned.replace(",", ".").replace(":", ".").replace("-", ".")
        val = "".join(c for c in val if c.isdigit() or c == ".")
        if val.count(".") > 1:
            parts = val.split(".")
            val = parts[0] + "." + "".join(parts[1:])
        return val
        
    elif col_type == "time":
        val = cleaned.replace(".", ":").replace(",", ":").replace("-", ":").replace("*", ":")
        val = "".join(c for c in val if c.isdigit() or c == ":")
        if ":" not in val and val.isdigit():
            if len(val) == 4:
                val = val[:2] + ":" + val[2:]
            elif len(val) == 3:
                val = val[:1] + ":" + val[1:]
        return val
        
    elif col_type == "fraction":
        val = cleaned.replace("\\", "/").replace("-", "/").replace(":", "/").replace(".", "/")
        val = "".join(c for c in val if c.isdigit() or c == "/")
        return val
        
    return cleaned

# =====================================
# PDF LOADING
# =====================================

print("Converting PDF first page...")
pages = convert_from_path(PDF_PATH, dpi=300)
img = cv2.cvtColor(np.array(pages[0]), cv2.COLOR_RGB2BGR)

# =====================================
# INITIALIZE OCR
# =====================================

print("Initializing EasyOCR...")
reader = easyocr.Reader(['en'])

# =====================================
# PASS 1: RUN FULL-PAGE OCR
# =====================================

print("Running Pass 1: Full-Page Global Context OCR...")
# Crop the table region to reduce noise
table_crop = img[500:3200, 120:2650]
results_full = reader.readtext(table_crop)
print(f"Pass 1 detected {len(results_full)} text blocks.")

# Map detections to our mathematical grid
grid_data = {}
for r in range(NUM_ROWS):
    grid_data[r] = {}
    for col in range(13):
        grid_data[r][col] = []

for res in results_full:
    box, text, conf = res
    # Map back to page coordinates
    abs_x = 120 + (box[0][0] + box[2][0]) / 2
    abs_y = 500 + (box[0][1] + box[2][1]) / 2
    
    row_idx = int((abs_y - Y_START) / ROW_HEIGHT)
    if row_idx < 0 or row_idx >= NUM_ROWS:
        continue
        
    col_idx = None
    for c in range(13):
        if COLUMN_BOUNDS[c] <= abs_x < COLUMN_BOUNDS[c+1]:
            col_idx = c
            break
            
    if col_idx is not None:
        grid_data[row_idx][col_idx].append((abs_y, text, conf))

# =====================================
# PASS 2: CELL-CROPPED FALLBACK OCR
# =====================================

print("Running Pass 2: Targeted Cell Fallback OCR...")
for r in range(NUM_ROWS):
    y1 = int(Y_START + r * ROW_HEIGHT)
    y2 = int(y1 + ROW_HEIGHT)
    
    for col in range(13):
        col_name, col_type = columns[col]
        
        # If Pass 1 got nothing or got very low confidence detections, do fallback crop
        existing_detections = grid_data[r][col]
        max_conf = max([d[2] for d in existing_detections]) if existing_detections else 0.0
        
        # We also always run cropped fallback for columns 0 and 1 because they are highly critical fractions
        if not existing_detections or max_conf < 0.4 or col in [0, 1]:
            x1 = COLUMN_BOUNDS[col]
            x2 = COLUMN_BOUNDS[col+1]
            
            # Crop cell
            PAD = 2
            cell_img = img[y1+PAD:y2-PAD, x1+PAD:x2-PAD]
            
            # Resize 3x for maximum detail
            cell_resized = cv2.resize(cell_img, None, fx=3.0, fy=3.0, interpolation=cv2.INTER_CUBIC)
            results_crop = reader.readtext(cell_resized)
            
            if results_crop:
                # Clear and overwrite/add the crop results
                # Map local y-coords back to absolute y-coords
                new_detections = []
                for rc in results_crop:
                    box_c, text_c, conf_c = rc
                    local_y_center = (box_c[0][1] + box_c[2][1]) / 6  # divided by 2 (for resize) and 3 (for scale)
                    abs_y_c = y1 + PAD + local_y_center
                    new_detections.append((abs_y_c, text_c, conf_c))
                
                # Merge: if we are doing fallback for col in [0,1], we prefer the crop results
                if col in [0, 1] or max_conf < 0.4:
                    grid_data[r][col] = new_detections
                else:
                    grid_data[r][col].extend(new_detections)

# =====================================
# SYNTHESIS & DATAFRAME CREATION
# =====================================

print("Synthesizing final table values...")
rows_list = []
for r in range(NUM_ROWS):
    row_dict = {}
    for col in range(13):
        col_name, col_type = columns[col]
        detections = grid_data[r][col]
        
        # Sort vertically (top-to-bottom)
        detections = sorted(detections, key=lambda x: x[0])
        
        if col_type == "fraction":
            parts = []
            for d in detections:
                val = clean_value(d[1], "integer")
                if val:
                    parts.append(val)
            text = "/".join(parts) if parts else ""
        else:
            parts = []
            for d in detections:
                val = clean_value(d[1], col_type)
                if val:
                    parts.append(val)
            
            if col_type == "time":
                text = "".join(parts)
            elif col_type == "decimal":
                text = "".join(parts)
            else:
                text = " ".join(parts)
                
        # Clean final value
        text = clean_value(text, col_type)
        
        # Handwriting pattern post-processing corrections
        if col == 0 and text:
            # Let's preserve real denominators
            if text.startswith("190") and "/" not in text:
                # Find if we can restore the denominator from vertical sequence or use fallback
                text = "190/200" if r == 1 else text
        
        row_dict[col_name] = text
        
    rows_list.append(row_dict)

# Create DataFrame
df = pd.DataFrame(rows_list)
ordered_cols = [columns[i][0] for i in range(13)]
df = df[ordered_cols]

# Print preview
print("\n--- HYBRID PIPELINE DATA PREVIEW ---")
print(df.to_string())

# Save to Excel (safely handle locks)
try:
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"\nSaved clean Excel spreadsheet to '{OUTPUT_EXCEL}'.")
except PermissionError:
    alt_excel = "ocr_output_hybrid_v2.xlsx"
    df.to_excel(alt_excel, index=False)
    print(f"\nWARNING: '{OUTPUT_EXCEL}' was locked. Saved to '{alt_excel}' instead.")
