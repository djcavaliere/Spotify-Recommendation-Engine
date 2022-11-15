# Spotify-Recommendation-Engine

### Table of Contents
1) [Introduction & Problem Statement](#introduction-&-problem-statement)
2) [Data Collection & Cleaning](#data-collection-&-cleaning)
3) [EDA](#EDA)
4) [Modeling](#Modeling)
5) [Conclusion](#Conclusion)


### Introduction & Problem Statement 
For this project I put myself in the role of a Data Scientist at Spotify. My job is to provide song recommendations based on a users listening preferences. I will build a recommendation engine that can intake a song and artist and provide 5 recommended songs to the listener.

Approach
1. Request listening history from Spotify and Call the Spotify API to build a library of tracks 
2. Clean & Prepare Data for Modeling
3. Analyze track features & my listening preferences  
4. Build and Evaluate Recommendations
---

### Data Collection & Cleaning
Extended Spotify Listening History- (Include Link to Spotify Data Request)
Kaggle Song List- (Include Link to Kaggle)
Spotify API - Include Link to API Reference

In total I pulled 183k tracks from Spotify API to build a library of track and artist features to compare to a users listening history. My extended listening history from Spotify included 12k songs from 3k artists from January 2012- November 2022.

### EDA
Genres: I've listened to 724 unique genres with the top genres being rock, pop, blues, hip-hop, and soul. While my top genres YoY remain fairly consistent I do have a wide array of genres under my belt.

Artists: I've listened to 2,975 unique artists. It appears I have a tendency to latch on to some artists then cycle through to different artists year over year as you can see most years I have a completely different list of top ten artists.

Tracks: I've listened to 12,323 unique songs. Similar to the artist year over year analysis we can see I also have a tendency to obssess over a set of songs then cycle through them as my top tens year over year have signifcant variation.

Features: Track features remain relatively consistent over the years as the distribution charts hold the same shapes across years. Most songs I listen to are mid-energy, non-instrumental, and relatively loud.


### Modeling
I built two variantions of a recommendations system, one which incorporated the artists' genre and one that did not. Both models utilize the cosine similarity to calculate the similarity between the input song and the track library and identify the most similar songs to surface recommendations. Additionally I filtered out songs from the same artist as the input track. Below are the results:

Recommender 1
The first recommender showed some promise with songs from popular/common genres such as rap, hip-hop, pop, etc. However this model struggled with less common genres such as edm, funk, newwave. If we don't consider genre in our similarity calculation we are more prone to serving unsuccessful recommendations for less popular genres.

Recommender 2
The second recommender exceeded my expectations. It performed exceptionally well for common and some uncommon genres. While many further improvements can be made (see conclusion below), this model is ready to ship.

### Conclusion
In conclusion I was able to successfully build a model and streamlit app that takes in a user input artist and track compares that to the combined track library and serves five recommendations from artists unique from the input artist. While Model 1 struggles with certain genres and styles of music, Model 2 which considers genre appears to perform reasonably well. Given additional time I would like to make the following improvements to the serve better recommendations.

Next Steps:
<br>1.Experiment with KNN Models
<br>2. Pull in more data from spotify api to have a more robust library to choose from
<br>3. Incoporate Audio Data
<br>4. Find a way to capture the relationship between similar genres
<br>5. Deploy and receive user feedback on where the recommendation engine struggles