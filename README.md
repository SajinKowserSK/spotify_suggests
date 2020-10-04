# Spotify Suggests 
Content-based recomendation system for suggesting songs to users, based on samples of current songs. Built with Flask, Pandas, NumPy, React and Spotify API. 

# Motivation 

The idea behind this project is to suggest songs without past user data. Users would be prompted by 3-5 songs, rate each song, have a user profile constructed and finally be recommended the best song on Spotify according to their profile feature values. This project broke down to 3 main parts: (1) Generating the data (2) Constructing a user profile (3) Making a user-friendly front-end platform. 

# Process
To begin, we first needed to create a pipeline to generate a table of Spotify songs from a specific genre. This static database would be used to sample the user’s song features and also to identify the ideal song on Spotify based on the data. To do this,  we used the Spotify API, with Python’s request library to get all Spotify playlists within a specific genre and cleaned it with Pandas & Regex (regular expression) libraries. Now that we have the static database of songs within a genre, we randomly prompt the user 3 songs from the database to rate and use the audio features of those songs (done with another type of Spotify API request) to construct a user profile. 

Next we multiplied the audio feature matrix with the user rating matrix for the 3 songs. This created a weighted-feature set for the song which represents the interest of the user for each feature based on the songs rated. A consideration we ran into here is the fact that some people may rate "good" as a 2 while others rate "good" as a 4. To account for this, we aggregated the weighted features and normalized them to construct the user profile. Now that we have the user profile, we look at the remaining songs on the static database, each as a "candidate" song. We multiply the user profile with the audio feature matrix for each song (Pandas & NumPy) to create the Weighted Songs Matrix. The Weighted Songs Matrix shows the respect of each audio feature with respect to the user profile. To calculate the best song, we simply take the song with the highest weighted average.

After completing this experiment using Python within a  Jupyter Notebook. We had to make the platform deployable and user friendly. To do this, we used Flask as a microframework and React for the frontend. 

