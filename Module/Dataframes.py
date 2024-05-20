import pandas as pd

# Función para convertir tiempo a segundos
def time_to_seconds(time_str):
    time_parts = list(map(int, time_str.split(':')))
    return time_parts[0] * 3600 + time_parts[1] * 60 + time_parts[2]

def procesar_df(df, distancia):
    df['AK'] = df.apply(lambda row: row['m/w'].upper() if pd.isna(row['AK']) else row['AK'], axis=1)
    df['Zeit-B'] = df.apply(
        lambda row: row['Zeit-N'] if pd.isna(row['Zeit-B']) or row['Zeit-B'] == 'DNS' or row['Zeit-B'] == '' else row[
            'Zeit-B'],
        axis=1
    )
    df['Tiempo en segundos'] = df['Zeit-N'].apply(lambda x: time_to_seconds(str(x)))
    df['Tiempo por km en segundos'] = df['Tiempo en segundos'] / distancia
    df['Zeit pro km in Minuten'] = round (df['Tiempo por km en segundos'] / 60, 2)  # Convertir segundos a minutos como float
    # Asignar el valor de "m/w" en mayúsculas a "AK" si "AK" no existe

    df = df.drop(columns=['Tiempo en segundos', 'Tiempo por km en segundos'])
    conversiones = {
        "Name": "string",
        "Rang": "int",
        "Verein/*Ort": "string",
        # Asegúrate de que el nombre de la columna corresponda exactamente como en tu DataFrame.
        "m/w": "string",
        "m/w Platz": "string",
        "AK": "string",  # Asegúrate de que el nombre de la columna corresponda exactamente como en tu DataFrame.
        "Platz AK": "string",
        "Startnr.": "string",
        "Strecke": "string",
        "Zeit pro km in Minuten": "float"
    }

    # Convertir tipos según el diccionario
    df = df.astype(conversiones)

    return df

# Leer el archivo Excel
file_path = 'F:\\Python_Projects\\angebote_database\\Merck_Lauf\\Merck.xlsx'


# Leer las hojas y procesarlas
df_3_5_km_row = pd.read_excel(file_path, sheet_name="3,5 km")
df_3_5_km = procesar_df(df_3_5_km_row, 3.5)

df_5_km_row = pd.read_excel(file_path, sheet_name="5 km")
df_5_km = procesar_df(df_5_km_row, 5.0)

df_10_km_row = pd.read_excel(file_path, sheet_name="10 km")
df_10_km = procesar_df(df_10_km_row, 10.0)

# Concatenar los DataFrames
df_concatenado = pd.concat([df_3_5_km, df_5_km, df_10_km], ignore_index=True)
