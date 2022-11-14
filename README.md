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

In total I pulled XXXk tracks from Spotify API to build a library of track and artist features to compare to a users listening history. My extended listening history from Spotify included X songs from Y artists from 2012-2022.

### EDA
Genres

Artists

Tracks

Features


### Modeling
I built two variantions of a recommendations system, one which incorporated the artists' genre and one that did not. Both models utilize the cosine similarity to calculate the similarity between the input song and the track library and identify the most similar songs to surface recommendations. Below are the results:

Model 1
Input:
Recommendations:

Model 2
Input:
Recommendations:

### Conclusion
In conclusion I was able to successfully build a recommendation engine that can take in an artist and track and return reasonable recommendations.

Next Steps/Improvements:
Add more data to the track library
Experiment with different models neural nets, etc
