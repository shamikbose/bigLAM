import pandas as pd

filename = r"C:\Users\Shamik Bose\Downloads\odor-dataset\metadata.csv"
df = pd.read_csv(filename)
skip_cols = ["Image URL", "File Name"]
for col in df.columns:
    if col not in skip_cols:
        new_col_name = col.lower().replace(" ", "_")
        print(f'"{new_col_name}": datasets.Value("string"),')
