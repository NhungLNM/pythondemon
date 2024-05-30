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

st.balloons()
st.markdown("# IT2 Group 7")

st.write("We are so glad to see you here. ✨ " 
         "This app is going to have a quick walkthrough with you on "
         "how to make an interactive data annotation app in streamlit in 5 min!")
# PLOT 1

selected_sports = ["Athletics", "Badminton", "Boxing", "Cycling", "Gymnastics", "Swimming"]
my_data = athlete_events[(athlete_events['Year'] == 2016) & (athlete_events['Sport'].isin(selected_sports))]

sport_counts = my_data['Sport'].value_counts(normalize=True) * 100

fig = px.pie(values=sport_counts, names=sport_counts.index, title='Distribution of Athletes in Selected Sports (2016)', hole=0.1)
fig.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig)
# PLOT 2

Year2014 = athlete_events[athlete_events['Year'] == 2014]
Teams = ["United States", "Russia", "Norway", "Germany", "Canada"]
m_data = Year2014[Year2014['Team'].isin(Teams)]

m_data_unique = m_data.drop_duplicates(subset='Name', keep='first')

team_counts = m_data_unique['Team'].value_counts().reset_index()
team_counts.columns = ['Team', 'Count']
team_counts = team_counts.sort_values(by='Count', ascending=False)

unique_colors = ["#FF5733", "#FFBD33", "#33FF57", "#33FFBD", "#5733FF"]

fig = px.bar(
    team_counts,
    x='Count',
    y='Team',
    orientation='h',
    color='Team',
    color_discrete_sequence=unique_colors,
    title="The number of athletes participating from five countries in the 2014 Winter Olympics",
    labels={'Count': 'Athletes', 'Team': 'Countries'}
)

fig.update_layout(
    yaxis=dict(categoryorder='total ascending'),
    showlegend=False
)

st.plotly_chart(fig)
# PLOT 4


b_data = athlete_events[athlete_events['Sport'].isin(["Boxing", "Football", "Judo", "Swimming", "Taekwondo"])]

athlete_counts = b_data['Sport'].value_counts().reset_index()
athlete_counts.columns = ['Sport', 'Count']

color_sequence = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

fig = px.pie(
    athlete_counts,
    values='Count',
    names='Sport',
    title='The number of athletes participating in the Olympic during 120 Years',
    hole=0.7,  # To create a donut chart
    color_discrete_sequence=color_sequence
)

st.plotly_chart(fig)
# PLOT 10

world_map = Figure(go.Choropleth())

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
