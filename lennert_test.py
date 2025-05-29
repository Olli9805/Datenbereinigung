import pandas as pd

def bereinigen(df: pd.DataFrame, spalte: str, save_path: str = None) -> pd.DataFrame:
    
    df[spalte] = pd.to_numeric(df[spalte], errors='coerce')

    if spalte=="TT_TER" :
        q1 = df[spalte].quantile(0.25)
        q3 = df[spalte].quantile(0.75)
        iqr = q3 - q1
        untergrenze = q1 - 1.5 * iqr
        obergrenze = q3 + 1.5 * iqr
    elif spalte=="RF_TER":
        untergrenze = 0
        obergrenze = 100

    print(f"Untergrenze: {untergrenze}")
    print(f"Obergrenze: {obergrenze}")
    
    df['mit_nan'] = df[spalte].where(
        (df[spalte] >= untergrenze) & (df[spalte] <= obergrenze),
        pd.NA
    )
    
    mittelwert = df['mit_nan'].mean().__round__(3)
    median = df['mit_nan'].median()
    linear = df['mit_nan'].interpolate(method='linear').round(3)
    ffill = df['mit_nan'].fillna(method='ffill')
    bfill = df['mit_nan'].fillna(method='bfill')

    df['Mittelwert'] = ""
    df['Median'] = ""
    df['Inter_Linear'] = ""
    df['ffill'] = ""
    df['bfill'] = ""
    
    mask = df['mit_nan'].isna()
    df.loc[mask, 'Mittelwert'] = mittelwert
    df.loc[mask, 'Median'] = median
    df.loc[mask, 'Inter_Linear'] = linear[mask]
    df.loc[mask, 'ffill'] = ffill[mask]
    df.loc[mask, 'bfill'] = bfill[mask]

    vergleich = df[['MESS_DATUM', spalte, 'Mittelwert',
                    'Median', 'Inter_Linear', 'ffill', 'bfill']]

    rückgabe_df = pd.DataFrame({
        'MESS_DATUM': df['MESS_DATUM'],
        spalte: df[spalte],
        'mit_nan': df['mit_nan'],
        'Inter_Linear': linear,
        'Mittelwert': df['Mittelwert'],
        'Median': df['Median'],
        'ffill': df['ffill'],
        'bfill': df['bfill']
    })

    if save_path:
        vergleich.to_csv(save_path, index=False, sep=';')
    return rückgabe_df


df = pd.read_csv("Datenbereinigung/data/daten2.txt", sep=";")
df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'].astype(str), format="%Y%m%d%H")

temp_df = bereinigen(df, 'TT_TER', save_path="temp.csv")
hum_df = bereinigen(df, 'RF_TER', save_path="hum.csv")

df['TT_TER_bereinigt'] = temp_df['Inter_Linear'].combine_first(temp_df['mit_nan'])
df['RF_TER_bereinigt'] = hum_df['Inter_Linear'].combine_first(hum_df['mit_nan'])

export_df = df[['STATIONS_ID', 'MESS_DATUM', 'QN_4', 'TT_TER_bereinigt', 'RF_TER_bereinigt', 'eor']]
export_df.columns = ['STATIONS_ID', 'MESS_DATUM', 'QN_4', 'TT_TER', 'RF_TER', 'eor']
export_df.to_csv("bereinigte_werte.csv", index=False, sep=';')
