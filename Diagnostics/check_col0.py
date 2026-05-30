import cv2
import easyocr
import os

reader = easyocr.Reader(['en'])
cell_dir = "structured_output/cells"

for r in range(10):
    filename = f"r{r:02d}_c00.png"
    path = os.path.join(cell_dir, filename)
    if not os.path.exists(path):
        print(f"{filename} does not exist.")
        continue
    
    img = cv2.imread(path)
    h, w, _ = img.shape
    results = reader.readtext(img)
    print(f"\nCell {filename} (shape {w}x{h}):")
    if not results:
        print("  (No text)")
    for res in results:
        print(f"  Text: '{res[1]}' conf={res[2]:.3f} box={res[0]}")
