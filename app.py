import streamlit as st
# Base packages
import pandas as pd
import numpy as np
import datetime
import altair as alt
import matplotlib.pyplot as plt
# Plot interactive maps
import geopandas as gpd
from shapely import wkt
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, ColumnDataSource
import json
from bokeh.models import HoverTool
# Command to launch Ngrok: ./ngrok http 8501


# sidebar
st.sidebar.markdown("*Dernière mise à jour: 10/12/2024*")
st.sidebar.markdown("---")
st.sidebar.header("Ressources utiles")
st.sidebar.markdown("Application réalisé par Mirana Ramanantsoa")

# header
st.header("COVID-19 au Sénégal 🇸🇳")
st.header("Part 1: Data Exploration")
st.write("In this section, we will explore the Altair cars dataset.")
st.markdown("*Further resources [here](https://altair-viz.github.io/gallery/selection_histogram.html)*")


# dataframe 
df =pd.read_csv("https://raw.githubusercontent.com/maelfabien/COVID-19-Senegal/master/COVID_Senegal.csv",sep=";")
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

# II. Summary of the number of cases
st.markdown("---")
evol_cases = df[['Date', 'Positif', 'Negatif', 'Décédé', 'Guéri']].groupby("Date").sum().cumsum()
st.subheader("En bref")
total_positif = evol_cases.tail(1)['Positif'][0]
total_negatif = evol_cases.tail(1)['Negatif'][0]
total_decede = evol_cases.tail(1)['Décédé'][0]
total_gueri = evol_cases.tail(1)['Guéri'][0]



st.markdown("Nombre de malades: <span style='font-size:1.1em;'>%s</span>"%(total_positif - total_gueri), unsafe_allow_html=True)
# nb de décès 
st.markdown("Nombre de décès : <span style='font-size:1.1em;'>%s</span>"%(total_decede), unsafe_allow_html=True)
# nb de guérison 
st.markdown("Nombre de guérion : <span style='font-size:1.1em;'>%s</span>"%(total_gueri), unsafe_allow_html=True)
st.markdown("Pourcentage de guerison: <span style='font-size:1.1em;'>%s</span>"%(np.round(total_gueri / total_positif * 100, 1)), unsafe_allow_html=True)
st.markdown("Taux de croissance journalier lissé sur les 2 derniers jours: <span style='font-size:1.1em;'>%s</span>"%(np.round(pd.DataFrame(np.sqrt(evol_cases['Positif'].pct_change(periods=2)+1)-1).tail(1)['Positif'][0] * 100, 2)), unsafe_allow_html=True)
st.markdown("Nombre total de cas positifs: <span style='font-size:1.1em;'>%s</span>"%(total_positif), unsafe_allow_html=True)
st.markdown("Nombre de tests negatifs: <span style='font-size:1.1em;'>%s</span>"%(total_negatif), unsafe_allow_html=True)
st.markdown("Nombre de tests réalisés: <span style='font-size:1.1em;'>%s</span>"%(total_positif + total_negatif), unsafe_allow_html=True)
st.markdown("Pourcentage de tests positifs: <span style='font-size:1.1em;'>%s</span>"%(np.round(total_positif / (total_positif + total_negatif) * 100, 1)), unsafe_allow_html=True)


st.markdown("---")
st.subheader("Cas positifs")
shapefile = '../02-Interactive-Map/input/ne_110m_admin_0_countries.shp'



positif = alt.Chart(evol_cases.reset_index()).mark_line(size=4, point=True).encode(
    x='Date',
    y='Positif'
).properties(title="Evolution of the number of positive cases", height=400, width = 700)

positif



st.markdown("---")
st.subheader("Graphique sources covid")


ch1 = alt.Chart(df.dropna(subset=['Source/Voyage'])).mark_bar().encode(
    x = 'Source/Voyage:N',
    y=alt.Y('count()', title='Number of patients')
).properties(title="Source", height=300, width=700)
ch1 