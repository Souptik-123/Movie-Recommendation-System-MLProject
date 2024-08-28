from http.client import responses

import pandas as pd
import streamlit as st
import pickle
import pandas as pd
import requests


movie_dict=pickle.load(open('movie_dict.pkl','rb'))
similarity=pickle.load(open("similarity.pkl","rb"))
movies=pd.DataFrame(movie_dict)

def fetch_poster(movie_id):
    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ba88dbc4f2721369b4d29741d11293d3&&language=en-US".format(movie_id))
    data=response.json()
    print(data["poster_path"])
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
def recommend(movie):
    movie_ind = movies[movies['title'] == movie].index[0]
    dist = similarity[movie_ind]
    recmovie = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie=[]
    recommended_movie_poster=[]
    for i in recmovie:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movie.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movie,recommended_movie_poster
st.title("Movie Recommender System")
selected_movie_name= st.selectbox(
    "Lets recommend Movies Based on the movie you chose below ",
    movies['title'].values,
    index=None,
    placeholder="Choose a movie"
)

if st.button("Recommend"):
    name,poster=recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])
