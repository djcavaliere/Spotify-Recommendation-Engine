#Import Libraries
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import preprocessing
import spotipy
import config

#Title and User Inputs
st.title('Spotify Recommendation Engine')
st.write('Enter a song to receive recommendations')

#Gather Track and Artist Input from User
user_track = st.text_input('Please Enter the Track Name: ')
user_artist = st.text_input('Please Enter the Artist Name: ')


#Load Pickled Library w/Genre
with open('models/library2.pkl', 'rb') as df2:
    library2 = pickle.load(df2)

#Spotify API
from spotipy.oauth2 import SpotifyClientCredentials
client_credentials_manager = SpotifyClientCredentials(client_id=config.cid, client_secret=config.secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)



#Returns results of spotify api call for user input artist and track
def get_users_track(artist, track):
    
    results = sp.search(q="artist: " + artist + "track: " + track, type="track", limit =1)['tracks']['items'][0]
    artist_id = results['album']['artists'][0]['id']
    track_id = results['id']
    trackName = results['name']
    
    #get artist and track features
    user_artists = artist_features([artist_id])
    user_track = track_features([track_id])
    user_table = pd.concat([user_artists, user_track], axis = 1)
    user_table.drop(columns = ['trackID', 'duration_ms', 'time_signature'], inplace = True)
    user_table.index = [trackName]

    return user_table

#Gets track features from spotify api
def track_features(data):
    danceability = []
    energy = []
    key = []
    loudness = []
    mode = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []
    track_id = []
    duration_ms = []
    time_signature = []
    
    for t in data:
        try:
            results = sp.audio_features(tracks = t)
            danceability.append(results[0]['danceability'])
            energy.append(results[0]['energy'])
            key.append(results[0]['key'])
            loudness.append(results[0]['loudness'])
            mode.append(results[0]['mode'])
            speechiness.append(results[0]['speechiness'])
            acousticness.append(results[0]['acousticness'])
            instrumentalness.append(results[0]['instrumentalness'])
            liveness.append(results[0]['liveness'])
            valence.append(results[0]['valence'])
            tempo.append(results[0]['tempo'])
            track_id.append(results[0]['id'])
            duration_ms.append(results[0]['duration_ms'])
            time_signature.append(results[0]['time_signature'])
        except:
            pass


    track_features = pd.DataFrame(track_id, columns = ['trackID'])
    track_features['danceability'] = danceability
    track_features['energy'] = energy
    track_features['key'] = key
    track_features['loudness'] = loudness 
    track_features['mode'] = mode 
    track_features['speechiness'] = speechiness
    track_features['acousticness'] = acousticness
    track_features['instrumentalness'] = instrumentalness
    track_features['liveness'] = liveness
    track_features['valence'] = valence
    track_features['tempo'] = tempo
    track_features['duration_ms'] = duration_ms
    track_features['time_signature'] = time_signature
    
    return track_features



#Get artists details from spotify
def artist_features(artist):
    results = sp.artists(artist)
    t = results['artists']
    ids = []
    artist_id = [x for x in artist]
    name = []
    genre = []
    popularity = []
    followers = []
    
    
    try:
        for s in t: 
            ids.append(s['id'])
            genre.append(s['genres'])
            popularity.append(s['popularity'])
            followers.append(s['followers']['total'])   
    except:
        ids.append(0)
        
    art_feat = pd.DataFrame(ids, columns = ['artist_id'])
    art_feat['artist_id'] = artist_id
    art_feat['genre'] = genre
    art_feat['popularity'] = popularity
    art_feat['followers'] = followers
    
    return art_feat


def recommender2(library, user_input):    
    #Join Library and User_Input
    user_input['genre'] = str(user_input['genre'][0])
    user_input['song'] = user_input.index
    combined = pd.concat([library, user_input])
    df = combined.drop(columns = ['artist_id'])
    df.reset_index(inplace = True, drop = True)
    
    #normalize features
    df['popularity'] = pd.DataFrame(preprocessing.normalize([df['popularity']]).T)
    df['loudness'] = pd.DataFrame(preprocessing.normalize([df['loudness']]).T)
    df['followers'] = pd.DataFrame(preprocessing.normalize([df['followers']]).T)
    df['tempo'] = pd.DataFrame(preprocessing.normalize([df['tempo']]).T)
    df['key'] = pd.DataFrame(preprocessing.normalize([df['key']]).T)
    
    #Count Vectorize library and input    
    vectorizer = CountVectorizer(max_features = 200)
    genre = vectorizer.fit_transform(df['genre'])

    #Create genre dataframe
    genre_df = pd.DataFrame(genre.toarray(), columns =[vectorizer.get_feature_names_out()])

    #Add genre count to extended df
    combined_genre = pd.concat([df, genre_df], axis = 1)
    combined_genre.index = combined_genre['song']
    #combined_genre.reset_index(inplace = True, drop = True)
    combined_genre.drop(columns = ['genre', 'song'], inplace = True)
    
    #calculate similarity
    similarity = cosine_similarity(combined_genre, combined_genre.iloc[[-1]])
    
    #create a similarity DataFrame
    sim = pd.DataFrame(similarity, index = combined_genre.index, columns = [user_input.index[0]])
    
    #filter out songs where the artist is the same as the input artist
    combined['score'] = sim.iloc[:,0].reset_index(drop= True)
    combined = combined[combined['artist_id'] != combined['artist_id'].iloc[-1]]
    
    #filter to top 5 
    recs = combined.sort_values(by = 'score', ascending = False)[1:6]
    recs.reset_index(inplace = True)
    
    return recs[['song']]



user_input = get_users_track(user_artist, user_track)

st.write(recommender2(library2, user_input))
