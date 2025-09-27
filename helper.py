import pandas as pd
import json
from thefuzz import process

# Load CSV
csv_url = "https://raw.githubusercontent.com/ltan0120/Final-3179/main/data.csv"
df = pd.read_csv(csv_url)

# Load TopoJSON and extract LGA names
topojson_url = "https://raw.githubusercontent.com/ltan0120/Final-3179/main/mapshaperoutput2.json"
with open("mapshaperoutput2.json") as f:  # or download first
    topo = json.load(f)

topo_lgas = [feat['properties']['LGA_NAME'] for feat in topo['objects']['LGA_POLYGON']['geometries']]

# Function to match CSV LGA names to TopoJSON LGA names
def match_lga(name, choices, threshold=80):
    match, score = process.extractOne(name, choices)
    if score >= threshold:
        return match
    return None

# Apply fuzzy matching
df['Matched_LGA'] = df['Local Government Area'].apply(lambda x: match_lga(x, topo_lgas))

# Keep only matched rows
df_clean = df.dropna(subset=['Matched_LGA']).copy()

# Replace original names with matched names
df_clean['Local Government Area'] = df_clean['Matched_LGA']
df_clean = df_clean.drop(columns=['Matched_LGA'])

# Save cleaned CSV
df_clean.to_csv("data_clean.csv", index=False)

print("Cleaned CSV saved! Number of LGAs:", len(df_clean))
