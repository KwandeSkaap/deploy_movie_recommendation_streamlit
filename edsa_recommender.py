"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
movies_df = pd.read_csv('../unsupervised_data/unsupervised_movie_data/movies.csv')
train_df = pd.read_csv('../unsupervised_data/unsupervised_movie_data/train.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Trending","Solution Overview", "EDA"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    #----- Code for trending page-----
    # Merge train and movies tables
    merged_df = pd.merge(movies_df, train_df, on='movieId')
    # Get average rating for each movie
    average_rating = pd.DataFrame(merged_df.groupby('title')['rating'].mean().reset_index())
    # Get number of votes for each movie
    vote_counts = pd.DataFrame(merged_df['title'].value_counts().reset_index())
    vote_counts.rename(columns={'title' : 'vote_count',
                           'index' : 'title'}, inplace=True)
    # Create dataframe with movies, vote counts, average ratings
    movies_with_scores = movies_df.copy()
    movies_with_scores = pd.merge(movies_with_scores, vote_counts, on='title')
    movies_with_scores = pd.merge(movies_with_scores, average_rating, on='title')

    # Calculate weighted score
    C = movies_with_scores['rating'].mean()
    # Minimum votes required to be listed in the chart - 90th percentile
    m = movies_with_scores['vote_count'].quantile(0.9)
    qual_movies = movies_with_scores.copy().loc[movies_with_scores['vote_count'] >= m]

    def weighted_rating(x, m=m, C=C):
        v = x['vote_count']
        R = x['rating']
        # Calculation based on IMDB formula
        return (v/(v+m) * R) + (m/(m+v) * C)

    # Create a new feature containing the weighted score
    qual_movies['score'] = qual_movies.apply(weighted_rating, axis=1)
    # Sort movies based on score
    qual_movies = qual_movies.sort_values('score', ascending=False)

    # Split pipe-separated genres
    split_genres = pd.DataFrame(qual_movies.genres.str.split('|').tolist(), index=qual_movies.movieId).stack()
    split_genres = split_genres.reset_index([0, 'movieId'])
    split_genres.columns = ['movieId', 'genres']
    # Merge on movie ID
    split_genres_merge = pd.merge(split_genres, qual_movies, on='movieId')
    split_genres_merge = split_genres_merge[['title', 'genres_x', 'score']]
    # List of genres for dropdown
    genres_list = split_genres_merge['genres_x'].unique().tolist()

    if page_selection == "Trending":
        st.title("Trending")
        st.write("The highest-rated movies in the dataset.")        
        st.write("## All genres")
        st.write(qual_movies[['title', 'score']])
        st.write("## Highest rated movies per genre")
        trending_genre = st.selectbox("Select genre", genres_list)
        st.write(split_genres_merge[split_genres_merge['genres_x'] == trending_genre][['title', 'score']].sort_values('score', ascending=False).head(10))
        
        


if __name__ == '__main__':
    main()
