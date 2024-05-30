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

# PLOT 6


filtered_dat = athlete_events[athlete_events['Year'] >= 1990]
filtered_dat = filtered_dat[['Year', 'Season', 'Sport']].drop_duplicates()

sports_count = filtered_dat.groupby(['Year', 'Season']).size().unstack(fill_value=0)
fig, axs = plt.subplots(2, 1, figsize=(12, 12))

years = sports_count.index
summer_counts = sports_count['Summer']
bar_width = 0.35
x = np.arange(len(years))

axs[0].bar(x, summer_counts, width=bar_width, color='#FFA500', alpha=0.7, label='Summer')
axs[0].set_xlabel('Year')
axs[0].set_ylabel('Number of Sports')
axs[0].set_title('Number of Sports Participated in Summer Season (1990-2022)')
axs[0].set_xticks(x)
axs[0].set_xticklabels(years)
axs[0].legend()
axs[0].grid(True, linestyle='-', alpha=0.2)

for i, summer_count in enumerate(summer_counts):
  axs[0].text(x[i], summer_count, str(summer_count), ha='center', va='bottom', fontsize=12)

winter_counts = sports_count['Winter']

axs[1].bar(x, winter_counts, width=bar_width, color='#4682B4', alpha=0.7, label='Winter')
axs[1].set_xlabel('Year')
axs[1].set_ylabel('Number of Sports')
axs[1].set_title('Number of Sports Participated in Winter Season (1990-2022)')
axs[1].set_xticks(x)
axs[1].set_xticklabels(years)
axs[1].legend()
axs[1].grid(True, linestyle='-', alpha=0.2)

for i, winter_count in enumerate(winter_counts):
  axs[1].text(x[i], winter_count, str(winter_count), ha='center', va='bottom', fontsize=12)

plt.tight_layout()

st.pyplot(fig)
