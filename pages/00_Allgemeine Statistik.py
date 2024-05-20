import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Añadir el directorio 'Module' al sys.path
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Module'))
sys.path.append(module_path)

# Importar desde Dataframes.py
from Dataframes import df_concatenado

st.set_page_config(page_title="11. Darmstädter Merck-Firmenlauf 2024 - Allgemeine Statistik",
                   page_icon=":bar_chart:",
                   layout="wide")

# Cargar el dataframe (asegúrate de cargar tus datos correctamente)
df = df_concatenado

# Agrupamos por 'm/w' y 'Strecke' y contamos las ocurrencias
grouped = df_concatenado.groupby(['m/w', 'Strecke']).size().reset_index(name='count')

# Calculamos el total por género
total_by_gender = grouped.groupby('m/w')['count'].transform('sum')

# Calculamos el porcentaje
grouped['percentage'] = round((grouped['count'] / total_by_gender) * 100, 2)

# Reorganizamos el DataFrame para mejor visualización
pivot_table = grouped.pivot(index='Strecke', columns='m/w', values='percentage')

# Reemplazar valores nulos con una cadena vacía o un valor apropiado
df = df.fillna('')
category_orders = {"Strecke": ["3,5 km Lauf", "5 km Lauf", "10 km Lauf"]}


def add_divider():
    st.markdown("<hr style='border:1px solid #ccc' />", unsafe_allow_html=True)


# Calcular el total de corredores y por carrera
total_corredores = len(df)
corredores_por_carrera = df['Strecke'].value_counts()

# Text in Deutsch mit den Gesamtdaten und Daten pro Rennen
texto_total = f"Gesamtzahl der Läufer: {total_corredores}"
texto_por_carrera = " || ".join([f"{k}: {v}" for k, v in corredores_por_carrera.items()])

# Layout inicial con título y descripción general
st.title("11. Darmstädter Merck-Firmenlauf 2024 - Allgemeine Statistik")

add_divider()



col1, col2 = st.columns(2)

# Berechnete Texte in Streamlit anzeigen
# Diagramm der prozentualen Teilnahme nach Geschlecht in jedem Rennen
col1.subheader("Prozentsatz der Teilnahme nach Geschlecht in jeder Strecke")
col1.write(
    f"Die Gesamtanzahl der Teilnehmer betrug: {total_corredores}.<br>Teilnehmer pro Strecke: {texto_por_carrera}",
    unsafe_allow_html=True)

with col1:
    df_sex_distribution = df.groupby(['Strecke', 'm/w']).size().reset_index(name='Anzahl')

    fig7 = px.pie(df_sex_distribution, values='Anzahl', names='m/w',
                  title="Verteilung nach Geschlecht im ausgewählten Rennen",
                  color_discrete_sequence=px.colors.sequential.Rainbow, facet_col='Strecke',
                  category_orders=category_orders, hole=0.4, custom_data=['m/w'])

    fig7.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig7)

with col2:
    st.subheader("Statistische Daten zur Teilnahme nach Geschlecht")

    mostrar_porcentaje = st.checkbox("Daten in Prozent anzeigen")

    df_stats_sex = df_sex_distribution.pivot(index='m/w', columns='Strecke', values='Anzahl').reset_index()
    df_stats_sex = df_stats_sex[['m/w'] + category_orders['Strecke']]

    if mostrar_porcentaje:
        df_stats_sex.iloc[:, 1:] = df_stats_sex.iloc[:, 1:].div(df_stats_sex.iloc[:, 1:].sum(axis=0), axis=1) * 100
        df_stats_sex = df_stats_sex.round(2)  # Prozentsätze auf 2 Dezimalstellen runden

    st.write(df_stats_sex)
    st.write(
        "Beobachtend die Daten im Allgemeinen sehen wir, dass Frauen eine Präferenz für die 3,5 km Strecke haben, während Männer die 10 km Strecke bevorzugen. Bei der 5 km Strecke gibt es praktisch eine Parität in der Anzahl von Männern und Frauen. Im Geschlecht Divers finden sich zwei Personen, eine in der 5 km und die andere in der 10 km Strecke.")
    st.write("Prozentsätze der Präferenz nach Geschlecht und Strecke:", pivot_table)

add_divider()

# Geschlechtsauswahl
st.subheader("Streckenpräferenzen nach AK und Geschlecht")
st.write("Der folgende Plot zeigt die Präferenz für die Auswahl der Strecke in Abhängigkeit von der Altersklasse (AK) und dem Geschlecht des Teilnehmers. Mit der Option 'Daten normalisieren' werden diese als Prozentsätze dargestellt. Ohne diese Option werden die Fälle mit den absoluten Daten angezeigt.")
sexo_seleccionado = st.selectbox("Geschlecht", ["Weiblich", "Männlich", "Divers"])

# Filtern des Dataframes nach gewähltem Geschlecht
if sexo_seleccionado == "Weiblich":
    df_filtrado_sexo = df[df['m/w'].str.lower().str.startswith('w')]
elif sexo_seleccionado == "Männlich":
    df_filtrado_sexo = df[df['m/w'].str.lower().str.startswith('m')]
else:
    df_filtrado_sexo = df[df['m/w'].str.lower().str.startswith('d')]

# Checkbox zur Daten-Normalisierung
normalizar = st.checkbox("Daten normalisieren / In Prozent pro AK anzeigen")

col1, col2 = st.columns(2)

# Datenanpassung basierend auf der Checkbox-Auswahl
if normalizar:
    df_count = df_filtrado_sexo.groupby(['AK', 'Strecke']).size().reset_index(name='Anzahl')
    df_filtrado_sexo_normalizado = df_count.groupby('AK').apply(
        lambda x: x.assign(Anzahl=100 * x['Anzahl'] / x['Anzahl'].sum())).reset_index(drop=True)
    df_filtrado_sexo_normalizado['Anzahl'] = df_filtrado_sexo_normalizado['Anzahl'].round(2)
    y_axis_label = "Prozent"
else:
    df_filtrado_sexo_normalizado = df_filtrado_sexo.groupby(['AK', 'Strecke']).size().reset_index(name='Anzahl')
    y_axis_label = "Anzahl"

with col1:
    st.subheader("Streckenpräferenzen nach Alterskategorie")
    fig8 = px.histogram(df_filtrado_sexo_normalizado, x='AK', y='Anzahl', color='Strecke', barmode='group',
                        title="Streckenpräferenzen nach Alterskategorie", category_orders=category_orders,
                        labels={'Anzahl': y_axis_label})
    st.plotly_chart(fig8)

with col2:
    st.subheader("Tabelle")
    df_stats_preferencias = df_filtrado_sexo_normalizado.pivot(index='AK', columns='Strecke', values='Anzahl').reset_index()

    # Añadir columnas faltantes si no están presentes en el DataFrame
    columnas_necesarias = ['AK'] + category_orders['Strecke']
    columnas_faltantes = [col for col in columnas_necesarias if col not in df_stats_preferencias.columns]
    for col in columnas_faltantes:
        df_stats_preferencias[col] = np.nan

    # Reordenar las columnas para asegurarte de que están en el orden deseado
    df_stats_preferencias = df_stats_preferencias[columnas_necesarias]

    st.write(df_stats_preferencias)

add_divider()

col1, col2 = st.columns(2)


def sekunden_zu_hms(sekunden):
    return f"{int(sekunden // 3600):02}:{int((sekunden % 3600) // 60):02}:{int(sekunden % 60):02}"


df['Zeit-TD'] = pd.to_timedelta(df['Zeit-N'].astype(str))

with col1:
    st.subheader("Zeit-N und Zeit/km nach Altersklasse")
    st.write("In diesem Block können Sie die von AK benötigte Zeit sehen, um die Strecke zu vervollständigen, und die Zeit, die die Teilnehmer pro AK benötigen, um einen Kilometer zu absolvieren, abhängig von der Strecke. Dafür können die drei unten angegebenen Filter angepasst werden.")
    rennen_seleccionado = st.selectbox("Strecke", df['Strecke'].unique())
    df_filtrado = df[df['Strecke'] == rennen_seleccionado].sort_values(by='Zeit-TD')

    geschlechter = df_filtrado['m/w'].str.strip().unique()
    geschlecht_filter = st.multiselect(
        "Wählen Sie das Geschlecht",
        options=geschlechter,
        default=list(geschlechter)
    )
    df_filtrado = df_filtrado[df['m/w'].isin(geschlecht_filter)]
    kategorien_sortiert = sorted(df_filtrado['AK'].unique())

    # Zeit in Stunden für die Visualisierung konvertieren
    df_filtrado['Zeit-N-Stunden'] = round(df_filtrado['Zeit-TD'].dt.total_seconds() / 3600, 2)

    # Dropdown zur Auswahl des Diagramms
    grafico_seleccionado = st.selectbox(
        "Wählen Sie das Diagramm",
        options=["Zeit-N nach Alterskategorie", "Zeit/Km nach Alterskategorie"]
    )

with col2:
    if grafico_seleccionado == "Zeit-N nach Alterskategorie":
        st.subheader("Zeit-N nach Alterskategorie")
        fig1 = px.box(df_filtrado, x='AK', y='Zeit-N-Stunden', color='AK',
                      category_orders={'AK': kategorien_sortiert},
                      height=400,
                      labels={'Zeit-N-Stunden': 'Zeit-N'},
                      )

        max_seconds = int(df_filtrado['Zeit-N-Stunden'].max() * 3600)
        tickvals = [i / 3600 for i in range(0, max_seconds, 600)]
        ticktext = [sekunden_zu_hms(i) for i in range(0, max_seconds, 600)]

        fig1.update_layout(
            yaxis=dict(
                tickvals=tickvals,
                ticktext=ticktext
            )
        )

        col2.plotly_chart(fig1)

    elif grafico_seleccionado == "Zeit/Km nach Alterskategorie":
        st.subheader("Zeit/Km nach Alterskategorie")
        fig10 = px.box(df_filtrado, x='AK', y='Zeit pro km in Minuten', color='AK',
                       category_orders={'AK': kategorien_sortiert},
                       height=400)
        col2.plotly_chart(fig10)

    # Temporäre Spalten nach der Verwendung löschen
    del df['Zeit-TD']
    del df_filtrado['Zeit-N-Stunden']

add_divider()

col1, col2 = st.columns(2)

with col1:
    # Titel der Anwendung
    st.subheader("Analyse der Geschlechterparität nach Verein")
    st.write("Dieser Abschnitt stellt die Geschlechterparität in den verschiedenen Vereinen dar. Das Geschlecht diverse ist mit weniger als 0,1 % des Gesamtanteils vertreten und wird daher in der folgenden Tabelle nicht berücksichtigt.")

    # Schieberegler für die minimale Gruppengröße
    min_group_size = st.slider('Minimale Gruppengröße', min_value=3, max_value=20, value=5)

    # Gruppieren nach 'Verein/*Ort' und Vorkommen jedes Geschlechts zählen
    grouped = df_concatenado.groupby(['Verein/*Ort', 'm/w']).size().unstack(fill_value=0)

    # Gesamtzahl der Mitglieder pro Gruppe berechnen
    grouped['Total'] = grouped.sum(axis=1)

    # Filtern von Gruppen mit mindestens der ausgewählten minimalen Größe
    filtered_grouped = grouped[grouped['Total'] >= min_group_size]

    # Berechnung des Geschlechterparitätsindex (näher an 1 ist besser)
    filtered_grouped['Parity_Index'] = filtered_grouped.apply(
        lambda x: min(x['m'], x['w']) / max(x['m'], x['w']) if max(x['m'], x['w']) > 0 else 0, axis=1)

    # Nach dem Paritätsindex sortieren und die Top 10 auswählen
    top_10_parity = filtered_grouped.sort_values(by='Parity_Index', ascending=False)

    # Ergebnisse in Streamlit anzeigen
    st.subheader("Tabelle der Geschlechterparität")
    st.dataframe(top_10_parity[['m', 'w', 'Total', 'Parity_Index']])


with col2:
    # Pie chart für die allgemeine Parität
    st.subheader("Allgemeine Geschlechterparität")

    # Gesamtzahl der Männer und Frauen im df_concatenado berechnen
    total_gender = df_concatenado['m/w'].value_counts().reset_index()
    total_gender.columns = ['Geschlecht', 'Anzahl']

    # Pie chart erstellen mit Plotly Express
    fig = px.pie(total_gender, values='Anzahl', names='Geschlecht', hole=0.4,
                 title='Geschlechterparität 11. Darmstädter Merck-Firmenlauf 2024',
                 labels={'Anzahl': 'Anzahl', 'Geschlecht': 'Geschlecht'},
                 hover_data={'Anzahl': ':.3f'})

    fig.update_traces(textposition='inside', textinfo='percent+label', hovertemplate='%{label}: %{value:.4f} (%{percent:.4f})')

    # Pie chart in Streamlit anzeigen
    st.plotly_chart(fig)


add_divider()

col1, col2 = st.columns(2)

with col1:
    df_filtrado_vc = df[df['Verein/*Ort'] != '']

    df_mas_entradas = df_filtrado_vc['Verein/*Ort'].value_counts().head(10)
    st.subheader('Top 10 Vereine/Orte nach Anzahl der Teilnehmer')
    st.write("Die 10 Vereine/Orte, die am meisten Teilnehmer beim Event vertreten haben")
    col1.write(df_mas_entradas)