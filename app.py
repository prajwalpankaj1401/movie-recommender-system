import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for idx in movies_list:
        movie_id = movies.iloc[idx[0]].movie_id
        recommended_movie_names.append(movies.iloc[idx[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names,recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.header('Movie Recommender System')
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movies, recommended_posters = recommend(selected_movie)
    columns = st.columns(5)
    for i, col in enumerate(columns):
        with col:
            st.text(recommended_movies[i])
            st.image(recommended_posters[i])