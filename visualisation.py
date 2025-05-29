import csv
import matplotlib.pyplot as plt


def lade_rohdaten(pfad):
    daten = []
    with open(pfad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for i, zeile in enumerate(reader):
            if i >= 1000:
                break
            try:
                temp = float(zeile["TT_TER"])
                hum = float(zeile["RF_TER"])
                daten.append((temp, hum))
            except:
                continue
    return daten


def lade_bereinigte_daten(pfad):
    daten = []
    with open(pfad, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for i, zeile in enumerate(reader):
            if i >= 1000:
                break
            try:
                temp = float(zeile["TT_TER"])
                hum = float(zeile["RF_TER"])
                daten.append((temp, hum))
            except:
                continue
    return daten


def zeige_visualisierung():
    roh = lade_rohdaten("data/daten2.txt")
    sauber = lade_bereinigte_daten("bereinigte_werte.csv")

    print(f"Rohdaten: {len(roh)} Werte")
    print(f"Bereinigte Daten: {len(sauber)} Werte")

    # Bereich der bereinigten Daten für feste Skala
    temps = [t for t, _ in sauber]
    hums = [h for _, h in sauber]
    temp_min, temp_max = min(temps), max(temps)
    hum_min, hum_max = min(hums), max(hums)

    # Vorher
    plt.figure()
    plt.title("Vor der Bereinigung")
    label_ausreisser = True
    label_gueltig = True
    for temp, hum in roh:
        if temp < -30 or temp > 50 or hum < 0 or hum > 100:
            plt.scatter(temp, hum, color="red", marker="x",
                        label="Ausreißer" if label_ausreisser else "")
            label_ausreisser = False
        else:
            plt.scatter(temp, hum, color="blue", alpha=0.3,
                        label="Gültige Werte" if label_gueltig else "")
            label_gueltig = False
    plt.xlabel("Temperatur (\u00b0C)")
    plt.ylabel("Luftfeuchtigkeit (%)")
    plt.grid(True)
    plt.legend()

    # Nachher
    plt.figure()
    plt.title("Nach der Bereinigung")
    plt.scatter(temps, hums, color="green", alpha=0.5, label="Bereinigte Werte")
    plt.xlabel("Temperatur (\u00b0C)")
    plt.ylabel("Luftfeuchtigkeit (%)")
    plt.grid(True)
    plt.legend()

    # Zusatz: Vorher mit fester Skala
    plt.figure()
    plt.title("Rohdaten (feste Skala wie bereinigt)")
    label_ausreisser = True
    label_gueltig = True
    for temp, hum in roh:
        if temp < -30 or temp > 50 or hum < 0 or hum > 100:
            plt.scatter(temp, hum, color="red", marker="x",
                        label="Ausreißer" if label_ausreisser else "")
            label_ausreisser = False
        else:
            plt.scatter(temp, hum, color="blue", alpha=0.3,
                        label="Gültige Werte" if label_gueltig else "")
            label_gueltig = False
    plt.xlabel("Temperatur (\u00b0C)")
    plt.ylabel("Luftfeuchtigkeit (%)")
    plt.xlim(temp_min, temp_max)
    plt.ylim(hum_min, hum_max)
    plt.grid(True)
    plt.legend()

    print(f"Erzeuge Plot mit {len(roh)} Rohpunkten und {len(sauber)} bereinigten Punkten")

    plt.show()


if __name__ == "__main__":
    zeige_visualisierung()
