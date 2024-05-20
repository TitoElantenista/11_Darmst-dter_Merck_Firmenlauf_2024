import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def create_histogram_plotly(df, title, selected_entries=None):
    bin_width = 0.25
    max_value = df['Zeit pro km in Minuten'].max()
    bins = np.arange(0, max_value + bin_width, bin_width)

    # Crear el histograma con Plotly y ajustar la opacidad de las barras
    fig = px.histogram(df, x='Zeit pro km in Minuten', title=title,
                       labels={'Zeit pro km in Minuten': 'Tiempo por km (minutos)'},
                       nbins=len(bins) - 1,
                       color_discrete_sequence=["blue"],
                       opacity=0.35)  # Ajustar opacidad de las barras directamente aquí

    if selected_entries:
        for entry in selected_entries:
            entry_time = df[df['Startnr.'] == entry]['Zeit pro km in Minuten'].values[0]
            # Obtener la frecuencia y la altura de la barra correspondiente
            bin_index = np.digitize(entry_time, bins) - 1
            bin_start = bins[bin_index]
            bin_end = bins[bin_index + 1]
            bin_center = (bin_start + bin_end) / 2
            bin_height = df[(df['Zeit pro km in Minuten'] >= bin_start) & (df['Zeit pro km in Minuten'] < bin_end)].shape[0]

            # Añadir un punto en la posición correspondiente dentro de la barra
            fig.add_trace(
                go.Scatter(
                    x=[entry_time],
                    y=[bin_height * 0.5],
                    mode='markers+text',
                    marker=dict(color='red', size=10, opacity=1.0),  # Establecer opacidad del punto a 1.0
                    textposition="top center",
                    showlegend=False
                )
            )

            # Añadir anotación con texto negro y tamaño más grande
            fig.add_annotation(x=entry_time, y=bin_height * 0.5,
                               text="{}".format(df[df['Startnr.'] == entry]['Name'].values[0]),
                               showarrow=True, arrowhead=2, ax=0, ay=-40,
                               font=dict(color="black", size=14),
                               xanchor="center", bgcolor="white", borderpad=2)

    # Ajustar el layout
    fig.update_layout(
        xaxis_title='Zeit pro km in Minuten',
        yaxis_title='Frequenz',
        bargap=0.02,
        template='plotly_dark',
        height=800
    )

    return fig
