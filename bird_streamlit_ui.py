from dataframe import rawdata
import pandas as pd
import plotly.express as px
import streamlit as st
# streamlit run bird_streamlit_ui.py

forest, grassland=rawdata()
# Main title 
st.title(":blue[Bird Species Analysis]")

# Sidebar options
selectors = st.sidebar.radio('Choose an Data:', [':blue[Seasonal Trends]',
                                                 ':blue[Species Distribution]',
                                                   ':blue[Observer Trends]',
                                                     ':blue[Environmental Impact]',
                                                       ':blue[Distance & Behavior]'])


# Sidebar Filters
st.sidebar.header("Filters")
selected_monthf = st.sidebar.multiselect("Select Months for Forest", forest["month"].unique(), default=forest["month"].unique(),)
selected_monthg = st.sidebar.multiselect("Select Months for Grassland", grassland["month"].unique(), default=grassland["month"].unique())
selected_interval = st.sidebar.multiselect("Select the Time Interval", forest["interval_length"].unique(), default=forest["interval_length"].unique())

# For empty filters
if not selected_interval:
    selected_interval= forest["interval_length"].unique()
if not selected_monthf:
    selected_monthf= forest["month"].unique()
if not selected_monthg:
    selected_monthg= grassland["month"].unique()

forest_df = forest[(forest["month"].isin(selected_monthf)) & (forest["interval_length"].isin(selected_interval))]
grassland_df = grassland[(grassland["month"].isin(selected_monthg)) & (grassland["interval_length"].isin(selected_interval))]

# Seasonal Trends
def seasonal_trends():

    # For forest
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Seasonal Trends in Forest</span>', unsafe_allow_html=True)

    forest_count = forest_df.groupby("date")["common_name"].count().reset_index()
    forest_count.columns = ["Date", "Observation Count"]
    
    fig1 = px.line(forest_count, x="Date", y="Observation Count", title="Bird Sightings by Month", markers=True)
    st.plotly_chart(fig1)
    
    max_monthf = forest_count.loc[forest_count["Observation Count"].idxmax()]
    min_monthf = forest_count.loc[forest_count["Observation Count"].idxmin()]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The month with the highest bird observations in forest is {max_monthf['Date']} with {max_monthf['Observation Count']} sightings.</span>', unsafe_allow_html=True)
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The month with the lowest bird observations in forest is {min_monthf['Date']} with {min_monthf['Observation Count']} sightings.</span>', unsafe_allow_html=True)
    
       
    # For Grassland
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write('<span style="font-size:30px; font-weight:bold; color:#FFB233;">\u2022 Seasonal Trends in Grassland</span>', unsafe_allow_html=True)
    
    grassland_count = grassland_df.groupby("date")["common_name"].count().reset_index()
    grassland_count.columns = ["Date", "Observation Count"]
    
    fig2 = px.line(grassland_count, x="Date", y="Observation Count", title="Bird Sightings by Month", markers=True)
    st.plotly_chart(fig2)
    
    max_monthg = grassland_count.loc[grassland_count["Observation Count"].idxmax()]
    min_monthg = grassland_count.loc[grassland_count["Observation Count"].idxmin()]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The month with the highest bird observations in grasslang is {max_monthg['Date']} with {max_monthg['Observation Count']} sightings.</span>', unsafe_allow_html=True)
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The month with the lowest bird observations in grassland is {min_monthg['Date']} with {min_monthg['Observation Count']} sightings.</span>', unsafe_allow_html=True)
    
# Species Distribution
def species_distribution():

    # For Forest |||||||||||||||
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Species Distribution in Forest</span>', unsafe_allow_html=True)

    forest_species = forest_df["common_name"].value_counts().reset_index()
    forest_species.columns = ["Species", "Count"]
    
    fig3 = px.bar(forest_species, x="Species", y="Count", title="Top Observed Bird Species in Forest")
    st.plotly_chart(fig3)

    max_species_f = forest_species.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The most observed bird species in forest is {max_species_f['Species']} with {max_species_f['Count']} sightings.</span>', unsafe_allow_html=True)
    

    # For Grassland |||||||||||||
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Species Distribution in Grassland</span>', unsafe_allow_html=True)

    grassland_species = grassland_df["common_name"].value_counts().reset_index()
    grassland_species.columns = ["Species", "Count"]
    
    fig4 = px.bar(grassland_species, x="Species", y="Count", title="Top Observed Bird Species in Grassland")
    st.plotly_chart(fig4)

    max_species_g = grassland_species.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The most observed bird species in grassland is {max_species_g['Species']} with {max_species_g['Count']} sightings.</span>', unsafe_allow_html=True)
    

# Observer Trends
def observer_trends():
    
    # For Forest |||||||||||||||
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Observer Trends in Forest</span>', unsafe_allow_html=True)

    #st.subheader("Observer Trends in Forest")
    observer_count_f = forest_df["observer"].value_counts().reset_index()
    observer_count_f.columns = ["Observer", "Observation Count"]
    
    fig_5 = px.bar(observer_count_f, x="Observer", y="Observation Count", title="Observer Contributions in Forest")#bar chat
    
    st.plotly_chart(fig_5)

    max_observer_f = observer_count_f.iloc[0]
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> The most active observer in forest is {max_observer_f['Observer']} with {max_observer_f['Observation Count']} observations.</span>', unsafe_allow_html=True)
    
    # For Grassland |||||||||||||
    st.markdown("<br><br>", unsafe_allow_html=True) 
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Observer Trends in Grassland</span>', unsafe_allow_html=True)
    observer_count_g = grassland_df["observer"].value_counts().reset_index()
    observer_count_g.columns = ["Observer", "Observation Count"]
    
    fig_6 = px.bar(observer_count_g, x="Observer", y="Observation Count", title="Observer Contributions in Grassland")
    
    st.plotly_chart(fig_6)
   
    max_observer_g = observer_count_g.iloc[0]
    st.write(f'''<span style="font-size:20px; font-weight:bold; color:#2C1D4C;">The most active observer in grassland is {max_observer_g['Observer']} with {max_observer_g['Observation Count']} observations.</span>''', unsafe_allow_html=True)
    
# Environmental Impact
def environmental_impact():

    # For Forest |||||||||||||
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Environmental Impact in Forest</span>', unsafe_allow_html=True)

    fig1 = px.scatter(forest_df, x="temperature", y="common_name", title="Effect of Temperature on Bird Sightings",size_max=10)
    st.plotly_chart(fig1)

    fig_7 = px.scatter(forest_df, x="humidity", y="common_name", title="Effect of Humidity on Bird Sightings", size_max=10)
    st.plotly_chart(fig_7)
    
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> Temperature and humidity variations affect bird sightings. Lower temperatures and Humidity might correlate with lower sightings in most of the species.</span>', unsafe_allow_html=True)
    
    # For Grassland |||||||||||||
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Environmental Impact in Grassland</span>', unsafe_allow_html=True)

    fig3 = px.scatter(grassland_df, x="temperature", y="common_name", title="Effect of Temperature on Bird Sightings", size_max=10)
    st.plotly_chart(fig3)
    
    fig_8 = px.scatter(grassland_df, x="humidity", y="common_name", title="Effect of Humidity on Bird Sightings", size_max=10)
    st.plotly_chart(fig_8)
    
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> Temperature and humidity variations affect bird sightings. Lower temperatures and Humidity might correlate with lower sightings in most of the species.</span>', unsafe_allow_html=True)

# Distance & Behavior
def distance_behavior():

    # For Forest |||||||||||||
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Distance and Behavior in Forest</span>', unsafe_allow_html=True)

    distance_count_f = forest_df["distance"].value_counts().reset_index()
    distance_count_f.columns = ["Distance", "Count"]
    
    fig_9 = px.bar(distance_count_f, x="Distance", y="Count", title="Bird Sightings by Distance in Forest")
    st.plotly_chart(fig_9)
    
    flyover_f = forest_df["flyover_observed"].value_counts().reset_index()
    flyover_f.columns = ["Flyover Observed", "Count"]
    
    fig_flyover_f = px.pie(flyover_f, names="Flyover Observed", values="Count", title="Flyover Observations in Forest")
    st.plotly_chart(fig_flyover_f)
    
    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> Birds observed within 0 to 100 meters are more frequently recorded. Flyover observations are relatively rare.</span>', unsafe_allow_html=True)

    #For Grassland |||||||||||||
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write('<span style="font-size:30px; font-weight:bold; color:#C8920B;">\u2022 Distance and Behavior in Grassland</span>', unsafe_allow_html=True)

    distance_count_g = grassland_df["distance"].value_counts().reset_index()
    distance_count_g.columns = ["Distance", "Count"]

    fig_10 = px.bar(distance_count_g, x="Distance", y="Count", title="Bird Sightings by Distance in Grassland")
    st.plotly_chart(fig_10)

    flyover_g = grassland_df["flyover_observed"].value_counts().reset_index()
    flyover_g.columns = ["Flyover Observed", "Count"]

    fig_flyover_g = px.pie(flyover_g, names="Flyover Observed", values="Count", title="Flyover Observations in Grassland")
    st.plotly_chart(fig_flyover_g)

    st.write(f'<span style="font-size:20px; font-weight:bold; color:#2C1D4C;"> Birds observed within 0 to 100 meters are more frequently recorded ,provided 0 to 50 is slightly high. Flyover observations are relatively rare.</span>', unsafe_allow_html=True)


# Sidebar options 

if selectors == ':blue[Seasonal Trends]':
   seasonal_trends()
elif selectors==':blue[Species Distribution]':
    species_distribution()
elif selectors==':blue[Observer Trends]':
   observer_trends()
elif selectors==':blue[Environmental Impact]':
   environmental_impact()
else:
   distance_behavior()
   
