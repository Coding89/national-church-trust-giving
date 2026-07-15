"""
Title: National Churches Trust (NCT) 360Giving Data Integration Pipeline

This script consolidates historical NCT grant spreadsheets (from 2016 to 2024) into a unified, schema
Parquet dataset for analysis.

"""
import datetime
import sys
from pathlib import Path
import pandas as pd

# Column mapping to handle 360Giving's naming conventions
COLUMN_MAP = {
    "Identifier":"Identifier",
    "Title": "Title",
    "Description": "Description",
    "Amount Awarded": "Amount Awarded",
    "Currency": "Currency",
    "Award Date": "Award Date",
    "Recipient Org:Name": "Recipient Org:Name",
    "Recipient Org:Identifier": "Recipient Org:Identifier",
    "Recipient Org:Charity Number": "Recipient Org:Charity Number",
    "Recipient Org:County": "Recipient Org:County",
    "Recipient Org:Postal Code": "Recipient Org:Postal Code",
    "Recipient Org:Description": "Recipient Org:Description",
    "Listed Status": "Listed Status",
    "Beneficiary Location:Description": "Beneficiary Location:Description",
    "Beneficiary Location:Name": "Beneficiary Location:Name",
    "Grant Programme:Title": "Grant Programme:Title",
    "Funding Org:Name": "Funding Org:Name",
    "Data Source": "Data Source",
    "Last Modified":"Last Modified",
}

# Clean up column names
def clean_col_name(col):
    if not isinstance(col, str):
        col = str(col)
    col = col.strip()
    return " ".join(col.split()).replace("\n", " ").replace("\r", "")

# Reads a single grant spreadsheet
def parse_file(file_path):
    path = Path(file_path)
    
    try:
        if path.stat().st_size == 0:
            print(f"Skipping empty file: {path.name}")
            return None
        
        xl = pd.ExcelFile(path, engine="openpyxl")
        
        # Finds the right data tab
        sheet_name = None
        for s in xl.sheet_names:
            if any(x in s.lower() for x in ["trust", "grant", "data"]):
                sheet_name = s
                break
        if not sheet_name:
            sheet_name = xl.sheet_names[0]
            
        print(f" Reading ➝ {path.name} | sheet: {sheet_name}")
               
        df = pd.read_excel(
            xl, sheet_name=sheet_name, engine="openpyxl", dtype=str
        )
        
        if df.empty or len(df) < 2:
            print(f"Caution! No data in sheet for {path.name}")
            return None
        
        # Normalises column names
        df.columns = [clean_col_name(c) for c in df.columns]
        
        # Verify that we actually have the expected columns
        missing_cols = [c for c in COLUMN_MAP.keys() if c not in df.columns]
        if len(missing_cols) == len(COLUMN_MAP):
            print(
                f"Caution! Critical layout shift: Found none of the expected headers in {path.name}"
            )
            return None
        
        # Keeps only the columns that are recognised
        existing_cols = [c for c in COLUMN_MAP.keys() if c in df.columns]
        df = df[existing_cols].copy()
        df.rename(columns=COLUMN_MAP, inplace=True)
        
        df["source_file"] = path.name
        return df
    
    except Exception as e:
        print(f"Failed to read {path.name}: {e}")
        return None
    
if __name__ == "__main__":
    data_dir = Path("datasets") # changed from ../datasets
        
    if not data_dir.exists():
            print(f"ERROR: Directory '{data_dir} does not exist.")
            sys.exit(1)
     # Takes into account all file years       
    files = sorted(
            data_dir.glob("*_national_churches_trust_360_giving_data.xlsx")
        )
        
    if not files:
            print("Nothing worked. Check the Excel files.")
            sys.exit(1)
        
    print(f"Found {len(files)} files with a matching schema. Merging...\n")
        
    all_data = []
        
    for f in files:
            year = datetime.datetime.now().year
            try:
                year = int(f.stem[:4])
            except ValueError:
                year = datetime.datetime.now().year
            
            print(f"Processing {year} data...")
            result = parse_file(f)
            
            if result is not None and not result.empty:
                result["grant_calendar_year"] = year
                all_data.append(result)
            
    if not all_data:
            print("No data extracted. Check the files.")
            sys.exit(1)
            
    print("\nMerging everything in a single Master set...")
    final = pd.concat(all_data, ignore_index=True)
        
    if "Award Date" in final.columns:
            final["Award Date"] = pd.to_datetime(
                final["Award Date"], errors="coerce"
            )
        
    if "Amount Awarded" in final.columns:
            final["Amount Awarded"] = pd.to_numeric(
                final["Amount Awarded"], errors="coerce"
            )
        # Final cleaning of data
    final.drop_duplicates(inplace=True)
    final = final.loc[:, ~final.columns.duplicated()].copy()
        
        # Save to file and provides a parquet file
    out_parquet = "national_church_grants_2016_2024.parquet"
    try:
            final.to_parquet(
                out_parquet, index=False, engine="pyarrow", compression="snappy"
            )
            print(f"\n Success! {len(final):,} grants saved to {out_parquet}")
    except Exception as e:
            print(f"Parquet compression engine failed ({e}), saving to CSV...")
            final.to_csv("national_churches_grants_fallback.csv", index=False)
        
    print("Pipeline execution complete")
