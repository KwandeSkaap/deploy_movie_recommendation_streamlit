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

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview", "EDA"]

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
        st.write('### Enter Your Three Favorite Movies live')
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
    # -------------------------------------------------------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")

    if page_selection == "EDA":
        st.subheader("Visualizations used to explore the data")
        if st.checkbox('Top 15 movies'):
            image = Image.open('top_15_movies.png')
            st.image(image, caption='TOP 15 MOVIES ', use_column_width=True)
        if st.checkbox('Bottom 15 Movies'):
            image = Image.open('bottom_15_movies.png')
            st.image(image, caption='BOTTOM 15 MOVIES', use_column_width=True)
        if st.checkbox('Frequent Genres'):
            image = Image.open('frequent_genres.png')
            st.image(image, caption='FREQUENT GENRES ', use_column_width=True)
        if st.checkbox('Genres according to Ratings'):
            image = Image.open('highest_rated_genres.png')
            st.image(image, caption='HIGHEST RATED GENRES', use_column_width=True)
        if st.checkbox('Director Ratings'):
            image = Image.open('highest_rated_directors.png')
            st.image(image, caption='HIGHEST RATED DIRECTORS', use_column_width=True)
        if st.checkbox('Runtime and score comparison'):
            image = Image.open('runtime_vs_score.png')
            st.image(image, caption='RUNTIME VS SCORE', use_column_width=True)
        if st.checkbox('Keywords Frequency'):
            image = Image.open('frequently_used_keywords.png')
            st.image(image, caption='FREQUENTLY USED KEYWORDS', use_column_width=True)
        if st.checkbox('Keywords Frequency for Highly Rated Movies'):
            image = Image.open('keywords_for_highly_rated_movies.png')
            st.image(image, caption='FREQUENTLY USED KEYWORDS HIGHLY RATED MOVIES', use_column_width=True)
        if st.checkbox('Keywords Frequency for Poorly Rated Movies'):
            image = Image.open('keywords_for_poorly_rated_movies.png')
            st.image(image, caption='FREQUENTLY USED KEYWORDS POORLY RATED MOVIES', use_column_width=True)


    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()
