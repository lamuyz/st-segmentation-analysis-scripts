import pandas as pd

# Convert transcript count parquet file to GEM format.
# Update input and output paths before running.

# 1. Read raw parquet data
parquet_path = "/path/to/input_counts.parquet"
df = pd.read_parquet(parquet_path)

# 2. Extract required columns and rename them to GEM format
df_gem = pd.DataFrame({
    "geneID": df["gene"],
    "x": df["x"].astype(int),
    "y": df["y"].astype(int),
    "MIDCount": df["counts"],
})

# 3. Save as tab-separated GEM file
out_gem_path = "/path/to/output_counts.gem"
df_gem.to_csv(out_gem_path, sep="\t", index=False)

print(f"GEM file saved to: {out_gem_path}")
