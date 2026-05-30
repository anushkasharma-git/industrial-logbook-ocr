import pandas as pd
try:
    df = pd.read_excel("ocr_output_clean.xlsx")
    print("--- CONTENT OF ocr_output_clean.xlsx ---")
    print(df.to_string())
except Exception as e:
    print(f"Error reading ocr_output_clean.xlsx: {e}")
