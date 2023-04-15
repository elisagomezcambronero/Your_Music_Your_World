import streamlit as st
#import src.api as sa
import api as sa
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

    st.write("🎵❄️ Winter Recommendations: Acoustic songs with lower 'Energy' and speechiness are perfect for the quiet winter season. the tranquil feeling of winter.")

    st.write("🎵☀️ Summer Recommendations: Songs should be songs with high 'Energy' and 'Danceability', as well as high 'Happiness' and 'Positivity'. Pop, hip-hop, and electronic music are perfect for the summer.")



elif button_clicked == "Liked Songs Clusters":
    df=pd.read_csv("../data/songs_you_like_clusterfeatures.csv", index_col=0)
    features = ['Danceability', 'Energy','Loudness', 'Speechiness', 'Acousticness', 'Valence']
    st.markdown("<h1 style='text-align: center;'> Connect to your Spotify 🤍 Songs </h1>", unsafe_allow_html=True)
    if st.button("Correlations between features"):
        corr_fig = cl.heatmap_correlation_features(df, features)
        st.sidebar.pyplot(corr_fig)
        
    cluster_stats= pd.read_csv("../data/cluster_stats.csv", index_col = 0 )
    fig=cl.radar_plot(cluster_stats)
    st.pyplot(fig)

elif button_clicked == "Ticketmaster":
    st.image("../images/ticketmaster.png")
    st.markdown("## Find your perfect Ticketmaster Event ")
    st.sidebar.markdown("#  Choose your perfect Ticketmaster Event ")
    st.write("Use the sidebar to fill your selection")

    data=pd.read_csv("../data/df_events.csv", index_col=0)
    # Crear mapa centrado en la ubicación promedio de los eventos
    center_lat = (39.8283 + 51.5074) / 2
    center_long = (-98.5795 + 13.4050) / 2
    m = folium.Map(location=[center_lat, center_long], zoom_start=3)
    # Iterar sobre los datos y agregar marcadores
    for index, row in data.iterrows():
    # Obtener información del evento
        event_name = row['event_name']
        event_location = row['event_location']
        event_lat = row['event_lat']
        event_long = row['event_long']
        artist = row['artist']
        url = row['url']

    # Crear marcador y agregarlo al mapa
        popup_html = f'<strong>{event_name}</strong><br>{artist}<br><a href="{url}" target="_blank">{url}</a>'
        popup = folium.Popup(popup_html, max_width=250)
        folium.Marker(location=[event_lat, event_long], popup=popup, tooltip=event_location).add_to(m)

    # Mostrar el mapa en Streamlit
    folium_static(m)
    
    st.sidebar.markdown("# 🎵 Find your perfect Ticketmaster Event 🎵")
    st.sidebar.image("image/music_icon.png")


