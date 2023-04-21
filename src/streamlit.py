import streamlit as st
import cluster as cl
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
load_dotenv()
import folium
from streamlit_folium import folium_static


Client_id=os.getenv("client_id")
Client_secret=os.getenv("client_secret")
Redirect_uri=os.getenv("redirect_uri")


st.set_page_config(page_title="Your Music Your World")
st.markdown("<h1 style='text-align: center; color: #1DB954;'> Your Music Your World</h1>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.markdown("<h1 style='text-align: center; color: #1DB954;'>Index</h1>", unsafe_allow_html=True)
nav_buttons = ["Introduction", "Songs features","Liked Songs Clusters", "Ticketmaster"]
button_clicked = st.sidebar.radio("", nav_buttons)

st.sidebar.markdown("---")
if button_clicked == "Introduction":
    st.markdown("<h4 style='text-align: center;'><i> Music is a powerful form of expression and a window into our souls </i></h4>", unsafe_allow_html=True)
    st.image("../images/Portada.jpg")
    st.markdown("This project focuses on analyzing your music preferences by extracting information from your liked songs on Spotify and creating playlists based on clusters of features songs. The application recommends seasonal playlists, such as winter, summer, autumn, and spring, based on the features of the songs you like.")
    st.markdown("In addition to recommending playlists, the application also uses the Ticketmaster API to suggest concerts in your area that feature your favorite artists. This feature allows you to attend concerts that match your musical preferences.")
    st.markdown("This project provides a personalized experience that caters to your musical tastes and interests, allowing you to discover new playlists and attend concerts that you are sure to enjoy.")


elif button_clicked == "Songs features":
    st.markdown("<h4 style='text-align: center;'> Spotify Songs Features </h4>", unsafe_allow_html=True)
    st.markdown("First lets understand songs features:")
    features = {
    "DANCEABILITY💃": "Describes how suitable a track is for dancing based on musical elements like tempo, rhythm stability, beat strength, and overall regularity.",
    "ENERGY🔥": "Measures the intensity and activity of a track. Energetic tracks are usually fast, loud, and noisy.",
    "LOUDNESS🔊": "Refers to the overall volume of a track.",
    "SPEECHINESS🗣️": "Measures the presence of spoken words in a track. Tracks with high speechiness are typically spoken word or rap.",
    "ACOUSTINESS🎸": "Measures the degree to which a track is acoustic (versus electronic). High acousticness means the track is mostly acoustic.",
    "VALENCE😊": "Describes the musical positivity of a track. Tracks with high valence sound more positive (happy, cheerful, etc.)"
}

# Create an expander for each feature
    for feature, definition in features.items():
        expander = st.expander(feature)
        with expander:
            st.write(definition)
    st.markdown("<h4 style='text-align: center;'> Does popular taste change over the year? </h4>", unsafe_allow_html=True)            
    st.markdown("In my ETL proyect [Project Top_Songs_Artists](https://github.com/elisagomezcambronero/Project-Top_Spotify_Songs_and_Artists) we discovered that Human taste over music can change. Using top charted songs 2020&2021 spotify list we saw that popularity characteristics values can change depending on the season.")
    st.image("../images/features_seasons.png")

    st.write("🎵❄️ Winter Recommendations: Acoustic songs with lower 'Energy' and speechiness are perfect for the quiet winter season. ")

    st.write("🎵☀️ Summer Recommendations: Songs should be songs with high 'Energy' and 'Danceability', as well as high 'Happiness' and 'Positivity'.")



elif button_clicked == "Liked Songs Clusters":
    df=pd.read_csv("../data/songs_you_like_clusterfeatures.csv", index_col=0)
    features = ['Danceability', 'Energy','Loudness', 'Speechiness', 'Acousticness', 'Valence']
    st.markdown("<h1 style='text-align: center;'> Connect to your Spotify 🤍 Songs </h1>", unsafe_allow_html=True)
    
        
    cluster_stats= pd.read_csv("../data/cluster_stats.csv", index_col = 0 )
    fig=cl.radar_plot(cluster_stats)
    st.pyplot(fig)
    
    if st.button("Create playlist"):
        st.image("images/Sunshine_State_of_Mind.png", caption="Sunshine State of Mind")
        st.image("images/Echoes_of_solitude.png", caption="Echoes of Solitude")

elif button_clicked == "Ticketmaster":
    st.image("../images/ticketmaster.png")
    st.sidebar.markdown("#  Choose your perfect Ticketmaster Event ")
    st.write("Use the sidebar to fill your selection")

    df_events=pd.read_csv("../data/df_events.csv", index_col=0)
    
    #select your event 
    st.markdown("## Find your perfect Ticketmaster Event ")
    #select country
    selected_country = st.sidebar.selectbox("Select a Country", df_events["event_country"].unique())
    filtered_df = df_events[df_events["event_country"] == selected_country]
    #select year date
    selected_year = st.sidebar.selectbox("Select a Year", df_events[df_events["event_country"] == selected_country]["year"].unique())
    selected_month = st.sidebar.selectbox("Select a Month", df_events[df_events["event_country"] == selected_country][df_events["year"] == selected_year]["month"].unique())

    filtered_df = filtered_df[filtered_df["year"] == selected_year]
    filtered_df = filtered_df[filtered_df["month"] == selected_month]

    #center the map
    center_lat = filtered_df["event_lat"].mean()
    center_long = filtered_df["event_long"].mean()
    m = folium.Map(location=[center_lat, center_long], zoom_start=3)
    for index, row in filtered_df.iterrows():
        event_name = row['event_name']
        event_city = row['event_city']
        event_lat = row['event_lat']
        event_long = row['event_long']
        artist = row['artist']
        url = row['url']
    
        # label shown
        popup_html = f'<strong>{event_name}</strong><br>{artist}<br><a href="{url}" target="_blank">{url}</a>'
        popup = folium.Popup(popup_html, max_width=250)
        folium.Marker(location=[event_lat, event_long], popup=popup, tooltip=event_city).add_to(m)

    # Mostrar el mapa
    folium_static(m)







