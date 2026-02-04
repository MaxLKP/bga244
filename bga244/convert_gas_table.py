import pandas as pd
import yaml

gasfile = r"bga244\gas_conifg\bga244_gases.xlsx" # Cobvert this to Excel with some tool: https://www.thinksrs.com/downloads/pdfs/applicationnotes/BGA244%20Gas%20Table.pdf

df = pd.read_excel(gasfile, dtype = {"Preferred Name": str, "Alternate Name 1": str, "Alternate Name 2": str, "Formula": str, "CAS#": str, "Molecular Weight": str})
df = df[["Formula", "CAS#"]].copy()
df = df.drop([0, 1, 2]) # Get Rid of doubles, but this has to be refined

with open(r"bga244\gas_conifg\gases.txt", "w", encoding = "utf-8") as file:
    for i, row in df.iterrows():
        data = f"{row['Formula']}: {row['CAS#']}".replace("\n", "").replace(" 00:00:00", "")
        file.write(data + "\n")

with open(r"bga244\gas_conifg\cas_nr.txt", "w", encoding = "utf-8") as file:
    for i, row in df.iterrows():
        data = f"{row['CAS#']}: {row['Formula']}".replace("\n", "").replace(" 00:00:00", "")
        file.write(data + "\n")
