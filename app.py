#Import Libraries
import pickle
import pandas as pd
import numpy as np
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import spotipy
import config

#Title and User Inputs
st.title('Spotify Recommendation Engine')
st.write('Enter a song to receive recommendations')

#Gather Track and Artist Input from User
user_track = st.text_input('Please Enter the Track Name: ')
user_artist = st.text_input('Please Enter the Artist Name: ')



#Spotify Call
# with open('models/get_users_track.pkl', 'rb') as pickle_in:
# 	call_spotify = pickle.load(pickle_in)

# user_song = call_spotify(user_artist, user_track)

#Recommendation Function
# with open('models/get_recommendation.pkl', 'rb') as rec:
# 	recommender = pickle.load(rec)

# #Run the artist and track through the recommendation engine 
# recommendations = recommender(user_song)

#Return results


#Load Pickled Library w/o Genre
with open('models/library.pkl', 'rb') as df:
	library = pickle.load(df)

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
    user_table.drop(columns = ['trackID','artist_id', 'duration_ms', 'time_signature'], inplace = True)
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


#Calculates Cosine Simularity and Returns Top 5 Recommendations - Genre Not Considered
# def get_recommendations(library, user_input):
#     #calculate similarity
#     similarity = cosine_similarity(library, user_input)
    
#     #create a similarity DataFrame
#     sim = pd.DataFrame(similarity, index = library.index, columns = [user_input.index[0]])
    
#     #filter to top 5 
#     recs = sim.sort_values(by = user_input.index[0], ascending = False)[1:6]
    
#     return recs


def get_recommendations(library2, user_input):
    #Join Library and User_Input
    user_input['genre'] = str(user_input['genre'][0])
    user_input['Song'] = user_input.index
    df = pd.concat([library2, user_input])
    df.drop(columns = ['index'], inplace = True)
    df.reset_index(inplace = True, drop = True)
    
    #Count Vectorize library and input    
    vectorizer = CountVectorizer(max_features = 200)
    genre = vectorizer.fit_transform(df['genre'])

    #Create genre dataframe
    genre_df = pd.DataFrame(genre.toarray(), columns =[vectorizer.get_feature_names_out()])

    #Add genre count to extended df
    combined_genre = pd.concat([df, genre_df], axis = 1)
    combined_genre.index = combined_genre['Song']
    #combined_genre.reset_index(inplace = True, drop = True)
    combined_genre.drop(columns = ['genre', 'Song'], inplace = True)
    
    #calculate similarity
    similarity = cosine_similarity(combined_genre, combined_genre.iloc[[-1]])
    
    #create a similarity DataFrame
    sim = pd.DataFrame(similarity, index = combined_genre.index, columns = [user_input.index[0]])
    
    #filter to top 5 
    recs = sim.sort_values(by = user_input.index[0], ascending = False)[1:6]
    recs.reset_index(inplace = True)
    
    return recs[['Song']]


user_input = get_users_track(user_artist, user_track)


#st.write(user_input)
st.write(get_recommendations(library2, user_input))
#st.write