import easyocr
import cv2
import os

reader = easyocr.Reader(['en'])

cell_dir = "structured_output/cells"
test_files = [
    "r02_c01.png",
    "r02_c06.png",
    "r02_c10.png",
    "r05_c00.png",
    "r05_c01.png",
    "r11_c03.png",
    "r11_c10.png"
]

print("Starting EasyOCR Test...")
for filename in test_files:
    path = os.path.join(cell_dir, filename)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
    
    # Read original image
    img = cv2.imread(path)
    
    # Run EasyOCR
    results = reader.readtext(img)
    
    print(f"\nFile: {filename}")
    if not results:
        print("  -> (No text detected)")
    for i, res in enumerate(results):
        box, text, conf = res
        print(f"  Result {i}: text='{text}' conf={conf:.3f} box={box}")
