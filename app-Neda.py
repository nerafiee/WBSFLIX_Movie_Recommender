import streamlit as st
import pandas as pd
 
st.title("Neda's Movie Recommender")
st.write(
    """
    ### Popularity-based movie recommender
    """
)

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

### popularity based recommender
def popularity_based_recommender(dense_matrix: pd.DataFrame, min_n_ratings: int, num: int):
    
    return (
    dense_matrix
        .groupby('movieId')
        .agg(
            mean_rating = ('rating', 'mean'),
            count_rating = ('rating', 'count')
        )
        .reset_index()
        .sort_values('mean_rating', ascending=False)
        .query('count_rating > @min_n_ratings')
        .head(num)
        )

num_recom = (
    st
    .sidebar
    .number_input(label = "How many top-rated movies should we recommend you?", min_value = 0, max_value = 200))

dense_matrix = ratings.copy()
recom_ids = popularity_based_recommender(dense_matrix.copy(), 20, num_recom)
recom_names = pd.merge(recom_ids, movies, on='movieId').filter(['title'])
st.dataframe(recom_names)

st.write(
    """
    ### Item-based movie recommender
    ##### The search results for your favorite movie:
    """
) 
### py function get sparse matrix
def get_sparse_matrix(dense_matrix: pd.DataFrame): 

    return(
    dense_matrix
        .pivot(index='userId', columns='movieId', values='rating')
    )

### item based recommender
def item_based_recommender(dense_matrix: pd.DataFrame, movieId: str, n: int=5): # n=6, minimum number of ratings

    sparse_matrix = get_sparse_matrix(dense_matrix)

    return(
    sparse_matrix
        .corrwith(sparse_matrix[movieId])
        .sort_values(ascending=False)
        .index
        .to_list()[1:n+1]
    )

def recommend_movie_title(movies: pd.DataFrame, ratings:pd.DataFrame, movie_id: str, min_num_rating: int):
    Ids = pd.DataFrame(item_based_recommender(ratings, movie_id, min_num_rating))
    result= (
        Ids
        .rename(columns={0:'movieId'})
        .merge(movies, on='movieId', how='left')
        .filter(['title'])
        )
    return(result)


movie_title = st.sidebar.text_input(label = "To use the item-based movie recommender, you need to enter the name (or even part of the name) of your favorite movie here:")
movies[movies['title'].str.contains(movie_title.title(), na=False)]

movie_id = st.sidebar.number_input("If you found the right name of your favorite movie, please enter its ID here:", min_value=1, max_value=movies.shape[0])
list= recommend_movie_title(movies, ratings, movie_id, min_num_rating=5)
st.write(
    """
    ### Our recommendation for you :)
    """
) 
st.dataframe(list)
