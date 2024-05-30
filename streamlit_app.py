import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import plotly.express as px
athlete_events = pd.read_excel('athlete_events.xlsx')


# PLOT 1

selected_sports = ["Athletics", "Badminton", "Boxing", "Cycling", "Gymnastics", "Swimming"]
my_data = athlete_events[(athlete_events['Year'] == 2016) & (athlete_events['Sport'].isin(selected_sports))]

sport_counts = my_data['Sport'].value_counts(normalize=True) * 100

fig = px.pie(values=sport_counts, names=sport_counts.index, title='Distribution of Athletes in Selected Sports (2016)', hole=0.1)
fig.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig)
xanchor="right",
        x=0.99
    ),
    showlegend=True,
    hovermode='x'
)

st.plotly_chart(fig)


# PLOT 8


filtered_dat = athlete_events[(athlete_events['Year'] >= 1990) & (athlete_events['Year'] <= 2016)]

summary_dat = filtered_dat.groupby(['Year', 'Season']).size().reset_index(name='total_athletes')

fig = go.Figure()

for season, color in zip(['Summer', 'Winter'], ['darkorange', 'steelblue']):
    data = summary_dat[summary_dat['Season'] == season]
    fig.add_trace(go.Scatter(
        x=data['Year'],
        y=data['total_athletes'],
        mode='lines+markers',
        name=season,
        line=dict(color=color),
        marker=dict(color=color, size=8),
        text=data['total_athletes'],
        hovertemplate='<b>%{x}</b><br><br>Total Athletes: %{y}',
    ))

fig.update_layout(
    title='Total Athletes in Summer and Winter (1990-2016)',
    xaxis_title='Year',
    yaxis_title='Total Athletes',
    legend_title='Season',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.99
    ),
    showlegend=True,
    hovermode='x'
)

st.plotly_chart(fig)


# plot 9


selected_sports = ["Basketball", "Gymnastics", "Swimming", "Athletics", "Boxing", "Wrestling"]

sport_age = athlete_events[(athlete_events['Year'] >= 1960) & (athlete_events['Year'] <= 2000) & athlete_events['Sport'].isin(selected_sports)]

sport_age['Year'] = pd.to_numeric(sport_age['Year'], errors='coerce')
sport_age['Age'] = pd.to_numeric(sport_age['Age'], errors='coerce')

sport_medians = sport_age.groupby('Sport')['Age'].median().sort_values().index

sport_colors = {
    "Basketball": "#1f77b4",  
    "Gymnastics": "#ff7f0e",  
    "Swimming": "#2ca02c",     
    "Athletics": "#d62728",    
    "Boxing": "#9467bd",       
    "Wrestling": "#8c564b"     
}

fig = go.Figure()

for sport in sport_medians:
    data = sport_age[sport_age['Sport'] == sport]
    fig.add_trace(go.Box(
        x=data['Sport'],
        y=data['Age'],
        name=sport,
        marker_color=sport_colors[sport],  
        boxmean='sd',
        hoverinfo='y+name',
        boxpoints='all'
    ))

fig.update_layout(
    title='Distribution of Age by Sport (1960-2000)',
    xaxis_title='Sport',
    yaxis_title='Age',
    showlegend=True,
    hovermode='closest'
)
st.plotly_chart(fig)



# PLOT 10

world_map = go.Figure(go.Choropleth())

east_asian_countries = [
    "China", "Japan", "South Korea", "North Korea", "Taiwan", "Hong Kong", "Mongolia", "Macau", "Vietnam", 
    "Laos", "Cambodia", "Thailand", "Myanmar", "Malaysia", "Singapore", "Brunei", "Philippines", "Indonesia", 
    "Timor-Leste"]

iso_codes = {
    "China": "CHN", "Japan": "JPN", "South Korea": "KOR", "North Korea": "PRK", "Taiwan": "TWN", 
    "Hong Kong": "HKG", "Mongolia": "MNG", "Macau": "MAC", "Vietnam": "VNM", "Laos": "LAO", 
    "Cambodia": "KHM", "Thailand": "THA", "Myanmar": "MMR", "Malaysia": "MYS", "Singapore": "SGP","Brunei": "BRN", "Philippines": "PHL", "Indonesia": "IDN", "Timor-Leste": "TLS"
}

athlete_counts = athlete_events[
    (athlete_events['Team'].isin(east_asian_countries)) & (athlete_events['Year'].between(1990, 2016))
].groupby('Team')['ID'].nunique().reset_index(name='athlete_count')

athlete_counts['iso_code'] = athlete_counts['Team'].map(iso_codes)

world_map.add_trace(go.Choropleth(
    locations=athlete_counts['iso_code'],
    z=athlete_counts['athlete_count'],
    text=athlete_counts['Team'],
    colorscale='Blues',
    marker_line_color='white',
    colorbar_title='Athlete Count',
))

world_map.update_layout(
    title='Number of Athletes in Southeast Asian and East Asian Countries (1990-2016)',
    geo=dict(
        showcoastlines=True,
        showcountries=True,
        countrycolor='white',
        coastlinecolor='black'
    ),
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Arial"
    )
)

st.plotly_chart(world_map)
