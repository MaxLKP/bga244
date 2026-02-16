import pandas as pd
from pathlib import Path

# Factory Gas Table: 
# https://www.thinksrs.com/downloads/pdfs/applicationnotes/BGA244%20Gas%20Table.pdf
# Convert this table to Excel with some tool of your choice befor reading it in

gasfile = config_path = Path(__file__).resolve().parent / "gas_config/bga244_gases.xlsx"

df = pd.read_excel(gasfile, dtype = {"Preferred Name": str, "Alternate Name 1": str, "Alternate Name 2": str, "Formula": str, "CAS#": str, "Molecular Weight": str})
df = df[["Formula", "CAS#"]].copy()
df = df.drop([0, 1, 2]) # Get Rid of doubles, but this has to be refined


gas_conv = config_path = Path(__file__).resolve().parent / "gas_config/gases.txt"
with open(gas_conv, "w", encoding = "utf-8") as file:
    for i, row in df.iterrows():
        data = f"{row['Formula']}: {row['CAS#']}".replace("\n", "").replace(" 00:00:00", "")
        file.write(data + "\n")

gas_conv = config_path = Path(__file__).resolve().parent / "gas_config/cas_nr.txt"
with open(gas_conv, "w", encoding = "utf-8") as file:
    for i, row in df.iterrows():
        data = f"{row['CAS#']}: {row['Formula']}".replace("\n", "").replace(" 00:00:00", "")
        file.write(data + "\n")
