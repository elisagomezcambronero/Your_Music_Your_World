import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import requests
import datetime

def your_artist_ticketmaster(artistas, token):
    dict_event = {}
    url = "https://app.ticketmaster.com/discovery/v2/events/"
    for artista in artistas:
        params = {"keyword": artista, "apikey": token}   
        res = requests.get(url, params=params)
        if res.status_code == 200:
            try:
                api_events = res.json()["_embedded"]["events"]
                dict_event[artista] = len(api_events)
            except KeyError:
                dict_event[artista] = 0
        else:
            dict_event[artista] = 0

    # filter artist with available events
    dict_event = {k: v for k, v in dict_event.items() if v > 0}
    df = pd.DataFrame({"artist": list(dict_event.keys()), "number_concerts": list(dict_event.values())})
    return df

def tu_request_ticketmaster(artistas, token):
    #info to be added in the dataset
    dict_event = {"event_name": [], "event_location": [], "event_lat": [], "event_long": [], "event_date": [], "event_min_price": [], "event_max_price": [], "artist": [], "url":[]}
    url = "https://app.ticketmaster.com/discovery/v2/events/"
    for artista in artistas:
        params = {"keyword": artista, "apikey": token}   
        res = requests.get(url, params=params)
        #call ticketmaster api
        if res.status_code == 200:
            try:
                api_events = res.json()["_embedded"]["events"]
                # Select elements from api 
                for event in api_events:
                    event_name = event["name"]
                    event_location = event["_embedded"]["venues"][0]["city"]["name"]
                    event_lat = None
                    event_long = None
                    event_date = datetime.datetime.strptime(event["dates"]["start"]["dateTime"], '%Y-%m-%dT%H:%M:%S%z')
                    event_min_price = None
                    event_max_price = None
                    event_url = event["url"]
                    artist = artista
                    venue = event["_embedded"]["venues"][0]["location"]
                    event_lat = venue["latitude"]
                    event_long = venue["longitude"]
                    if "priceRanges" in event: 
                        price_ranges = event["priceRanges"]
                        if len(price_ranges) > 0:
                            price_range = price_ranges[0]
                            event_min_price = price_range.get("min")
                            event_max_price = price_range.get("max")
                    dict_event["event_name"].append(event_name)
                    dict_event["event_location"].append(event_location)
                    dict_event["event_lat"].append(event_lat)
                    dict_event["event_long"].append(event_long)
                    dict_event["event_date"].append(event_date)
                    dict_event["event_min_price"].append(event_min_price)
                    dict_event["event_max_price"].append(event_max_price)
                    dict_event["artist"].append(artist)
                    dict_event["url"].append(event_url)
            except KeyError:
                pass

    df = pd.DataFrame(dict_event)
    return df