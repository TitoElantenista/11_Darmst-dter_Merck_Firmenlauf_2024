import sys
import os
import streamlit as st
# Añadir el directorio 'Module' al sys.path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Module'))
sys.path.append(module_path)
from plot_module import create_histogram_plotly
from Dataframes import df_3_5_km, df_10_km, df_5_km, df_concatenado

st.set_page_config(layout="wide")
# Streamlit app
st.title("Analyse der Läuferzeiten")

# Selector para elegir el DataFrame
distancia = st.selectbox("Wähle die Distanz", ["3,5 km Lauf", "5 km Lauf", "10 km Lauf", "Allgemein"], index=3)

if distancia == "3,5 km Lauf":
    df_selected = df_3_5_km
elif distancia == "5 km Lauf":
    df_selected = df_5_km

    # Suponiendo que df es tu DataFrame y "Rang" es la columna de interés
    x_min = df_selected['Rang'].min()
    x_max = df_selected['Rang'].max()

    # Crear un conjunto de todos los valores en el rango de x_min a x_max
    expected_values = set(range(x_min, x_max + 1))

    # Crear un conjunto de los valores actuales en la columna "Rang"
    current_values = set(df_selected['Rang'])

    # Encontrar los valores faltantes
    missing_values = expected_values - current_values

    # Imprimir los valores faltantes
    print("Valores faltantes en la columna 'Rang' entre", x_min, "y", x_max, ":", sorted(missing_values))



elif distancia == "10 km Lauf":
    df_selected = df_10_km
else:
    df_selected = df_concatenado







# Multiselect para filtrar por valores únicos de "m/w"
# Limpiar valores únicos
unique_genders = df_selected['m/w'].str.strip().unique()

# Widget multiselect
gender_filter = st.multiselect(
    "Wähle das Geschlecht",
    options=unique_genders,
    default=list(unique_genders)  # Asegurarse de convertir a lista
)

# Filtrar el DataFrame basado en el filtro de género
filtered_df = df_selected[df_selected['m/w'].isin(gender_filter)]

# Obtener opciones únicas de AK después de aplicar el filtro de género
ak_options = filtered_df['AK'].unique()

# Convertir las opciones de AK a lista para asegurar compatibilidad con default
ak_options_list = list(ak_options)

# Widget multiselect para AK con todas las opciones preseleccionadas
ak_filter = st.multiselect(
    "Wähle die Altersklassen (AK)",
    options=ak_options_list,
    default=ak_options_list  # Asegurarse de convertir a lista
)


# Filtrar el DataFrame según los valores seleccionados en los multiselect
df_selected = df_selected[df_selected['m/w'].isin(gender_filter) & df_selected['AK'].isin(ak_filter)]

# Checkbox para excluir outliers
exclude_outliers = st.checkbox("Ausreißer nach rechts ausschließen")

if exclude_outliers:
    # Calcular el límite superior (por ejemplo, percentil 95)
    upper_limit = df_selected['Zeit pro km in Minuten'].quantile(0.99)
    # Filtrar los datos para excluir los outliers hacia la derecha
    df_selected = df_selected[df_selected['Zeit pro km in Minuten'] <= upper_limit]

# Mostrar el DataFrame seleccionado
st.dataframe(df_selected)

# Crear el plot utilizando la función del módulo
fig = create_histogram_plotly(df_selected, title="caca")  # Bin size in minutes

# Actualizar las opciones de 'Startnr.' basadas en el DataFrame filtrado
startnr_options = df_selected['Startnr.'].unique()


st.divider()
col1, col2, col3 = st.columns(3)

# Crear el plot utilizando la función del módulo


selected_labels = []
selected_entries = []
if st.checkbox("Einzelne Läufer wählen", value=True):
    # Multiselect para elegir por club o localidad antes de seleccionar los corredores individuales
    club_options = df_selected['Verein/*Ort'].unique()
    selected_clubs = col1.multiselect("Wähle Verein/*Ort (OPTIONAL)", options=club_options)

    # Filtrar df para agregar automáticamente las entradas del club seleccionado
    if selected_clubs:
        club_entries = df_selected[df_selected['Verein/*Ort'].isin(selected_clubs)]
        for entry in club_entries.iterrows():
            entry_label = f"{entry[1]['Startnr.']} - {entry[1]['Name']}"
            if entry_label not in selected_labels:
                selected_labels.append(entry_label)

    # Crear opciones que incluyan "Startnr." y "Name" para mostrar
    options = df_selected.apply(lambda row: f"{row['Startnr.']} - {row['Name']}", axis=1).unique()
    selected_labels = col1.multiselect("Wähle die 'Startnr.'", options=options, default=selected_labels)

    # Recuperar los valores de 'Startnr.' correspondientes a las etiquetas seleccionadas
    startnr_map = {f"{row['Startnr.']} - {row['Name']}": row['Startnr.'] for index, row in df_selected.iterrows()}
    selected_entries = [startnr_map[label] for label in selected_labels if label in startnr_map]

    if selected_entries:
        # Crear un DataFrame con las entradas seleccionadas
        df_entries = df_selected[df_selected['Startnr.'].isin(selected_entries)]
        col2.dataframe(df_entries[['Name', 'Startnr.', 'Zeit pro km in Minuten', 'AK', 'Strecke','Zeit-N']])
    else:
        col2.write("Wenn Einzelläufer ausgewählt werden, erscheint hier eine Tabelle.")
else:
    col2.write("Wenn Einzelläufer ausgewählt werden, erscheint hier eine Tabelle.")

fig = create_histogram_plotly(df_selected, title="Verteilung der Zeiten pro km", selected_entries=selected_entries)

# Mostrar el plot
st.plotly_chart(fig, use_container_width=True)

