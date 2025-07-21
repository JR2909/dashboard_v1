from dash import Dash, html, dcc
import plotly.express as px
from data.dummy_data import load_data
import geopandas as gpd
import matplotlib.pyplot as plt
import io
import base64
from iso3166 import countries
from parameters import *

country=countries.get(COUNTRY).name
# Pfad zur Shapefile-Datei
path = r"maps/ne_10m_admin_0_countries.shp"
world = gpd.read_file(path)

land = world[world['ADMIN'] == country]

# Plot als Bild speichern
fig, ax = plt.subplots()
land.plot(ax=ax, color="lightblue", edgecolor="black")
ax.axis("off")
img_bytes = io.BytesIO()
plt.savefig(img_bytes, format="png", bbox_inches="tight")
img_bytes.seek(0)
encoded_img = base64.b64encode(img_bytes.read()).decode()

# Dummy-Daten laden
pie_data, bar_data, column_data1, column_data2, bar_data_left = load_data()

# Diagramme erstellen
pie_fig = px.pie(pie_data, names="Kategorie", values="Wert", title="Kreisdiagramm", hole=0.75,height=300, width=400)
bar_fig = px.bar(bar_data, x="Monat", y="Umsatz", title="Balkendiagramm",height=300, width=400)
column_fig1 = px.bar(column_data1, x="Produkt", y="Stückzahl", title="Säulendiagramm 1",height=300, width=400)
column_fig2 = px.bar(column_data2, x="Region", y="Zahl", title="Säulendiagramm 2",height=300, width=400)
bar_fig_left = px.bar(bar_data_left, x="Faktor", y="Score", title="Balkendiagramm unten links",height=300, width=400)



# Dashboard-Aufbau
app = Dash(__name__)
app.layout = html.Div([
    html.Div([
        # Linke Spalte
        html.Div([
            html.Div([
                html.Img(src="data:image/png;base64,{}".format(encoded_img), className="map"),
                ]),
            html.Fieldset([
                html.Div([dcc.Graph(figure=bar_fig_left)], className="kpi"),
                ])
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "padding": "5px"}),

        # Rechte Spalte
        html.Div([
            html.Fieldset([
                html.Div([dcc.Graph(figure=pie_fig)], className="kpi"),
                html.Div([dcc.Graph(figure=bar_fig)], className="kpi")
            ], style={"display": "flex", }),

            html.Fieldset([
                html.Div([dcc.Graph(figure=column_fig1)], className="kpi"),
                html.Div([dcc.Graph(figure=column_fig2)], className="kpi")
            ], style={"display": "flex", "marginTop": "5px"})
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "padding": "5px"})
    ])
])

if __name__ == "__main__":
    app.run(debug=True)