

import pandas as pd

df = pd.read_csv("data/daten2.txt", sep=";")
print(df.head())


print("Überblick über den Datensatz:")
print(df.head(), "\n")

ausreisser_temp = df[(df["TT_TER"] < -50) | (df["TT_TER"] > 50)]
print(f"Ausreißer in TT_TER (Temperatur): {len(ausreisser_temp)} Zeilen")
ausreisser_feuchte = df[(df["RF_TER"] < 0) | (df["RF_TER"] > 100)]
print(f"Ausreißer in RF_TER (Relative Feuchte): {len(ausreisser_feuchte)} Zeilen")





