import streamlit as st

st.set_page_config(page_title="Allgemeine Statistik",
                page_icon=":bar_chart:",
                layout="wide"
)

# Título de la página con iconos
st.title("🏃‍♂️ 11. Darmstädter Merck-Firmenlauf 2024 📊")

# Introducción con iconos y texto estructurado
st.markdown("""
### 📋 Einführung
Die folgende Seite zeigt einige grundlegende Statistiken zum 11. Darmstädter Merck-Firmenlauf 2024. Die Datenquelle ist die herunterladbare PDF-Tabelle von der Website [my.raceresult.com](https://my.raceresult.com/269925/results#0_438464).

Es wird versucht, die Ergebnisse nicht zu analysieren. Das kann jeder nach eigenem Ermessen tun. Es wird auch nicht empfohlen, die Statistiken zu nutzen, um sich zum Beispiel für eine Strecke anzumelden. Ein Beispiel: Eine Frau könnte anhand der Daten denken, dass die 3,5 km Strecke die geeignetste für sie ist. Andererseits haben wir bei den Frauen in der Altersgruppe W70 über 80% Damen, die die 5 km Strecke gewählt haben. Jeder wählt seine eigenen Referenzen und Interpretationen.

Diese kleine App befindet sich noch in der Entwicklung und enthält noch einige Fehler, die möglicherweise in Zukunft behoben werden (oder wahrscheinlich nicht🙂).
""")

# Instrucciones con iconos
st.markdown("""
### 📝 Anweisungen
Auf der linken Seite der Website befindet sich ein Seitenmenü. Wenn es nicht sichtbar ist, kann es durch Klicken auf einen kleinen Pfeil in der oberen linken Ecke angezeigt werden. In diesem Menü sehen Sie oben die Optionen "Allgemeine Statistik" und "Läufer Statistik". In der ersten Option sehen Sie die grundlegenden Statistiken des Rennens und in "Läufer Statistik" können Sie Ihre m/km mit anderen Läufern vergleichen. Im Moment gibt es nicht mehr.
""")

# Sugerencias y quejas con iconos y link
st.markdown("""
### 💬 Vorschläge und Beschwerden
[Kontakt auf LinkedIn](https://www.linkedin.com/in/roberto-sl-8a0b81b0/)
""")