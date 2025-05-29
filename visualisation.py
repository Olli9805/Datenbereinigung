import csv
import matplotlib.pyplot as plt
import pandas as pd
import os

def lade_rohdaten(pfad):
    daten = []
    with open(pfad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for zeile in reader:
            try:
                temp = float(zeile["TT_TER"])
                hum = float(zeile["RF_TER"])
                daten.append((temp, hum))
            except:
                continue
    return daten

def lade_bereinigte_daten(temp_pfad, hum_pfad):
    temp_df = pd.read_csv(temp_pfad)
    hum_df = pd.read_csv(hum_pfad)
    return list(zip(temp_df.iloc[:, 0], hum_df.iloc[:, 0]))

def zeige_visualisierung():
    roh = lade_rohdaten("data/daten2.txt")
    sauber = lade_bereinigte_daten("temp.csv", "hum.csv")

    # Plot 1: Vor der Bereinigung
    plt.figure()
    plt.title("Vor der Bereinigung")
    for temp, hum in roh:
        if temp < -30 or temp > 50 or hum < 0 or hum > 100:
            plt.scatter(temp, hum, color="red", marker="x", label="Ausreißer")
        else:
            plt.scatter(temp, hum, color="blue", alpha=0.3)
    plt.xlabel("Temperatur (°C)")
    plt.ylabel("Luftfeuchtigkeit (%)")
    plt.grid(True)

    # Plot 2: Nach der Bereinigung
    plt.figure()
    plt.title("Nach der Bereinigung")
    plt.scatter([t for t, _ in sauber], [h for _, h in sauber], color="green", alpha=0.5)
    plt.xlabel("Temperatur (°C)")
    plt.ylabel("Luftfeuchtigkeit (%)")
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    zeige_visualisierung()
