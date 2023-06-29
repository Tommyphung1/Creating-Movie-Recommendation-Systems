import pandas as pd

def user_top_5(model = None, review_df = None, user_id = None, movies = None):
    """Take in a model and a user Id and output the predicted rating for the movies
    ______________________________
    Input - user_id (int) 
          - model (model 
          - review_df (Dataframe)
    Output - list (list) 
    ______________________________
    If a user isn't in the list of users, ie new, they will be recommended with the best rated movie on average.
    List output is sorted before returning.
    Will not suggest movies already seen. 
    """
    
    ### If the user is new ### 
    if((user_id not in review_df['userId'].unique()) | (user_id == None)):
        average_ratings = review_df[['movieId','rating']].groupby(by= 'movieId').mean()              ## Group by movies with the average rating taken ## 
        print("New User Detected. Average top rated movies are as followed")                         ## Message the user with decision   ##
        rec_movies = id_title(average_ratings.sort_values('rating', ascending= False).index[0:5], movies)    ## Sort the value by rating and return the top 5 movies ##
        display(rec_movies)
        return None
    
    ### Take the seen movies and don't rate them in the list ### 
    seen_movies = review_df['movieId'].loc[review_df['userId'] == user_id].unique()                  ## All the movies seens by the user from the past review. ##
                                                                                                     ## Assume all movies watched are in the list and rated prior ## 
    new_movies = [movie_id for movie_id in movies.movieId.unique() if movie_id not in seen_movies]   ## A list of all the movie ID not seen by the user so far ## 
    predicted_ratings = []                                                                           ## A list of the predicted ratings for the movies. ## 
    
    ### For each movie ID, use the model to predict the rating for the user based off the model type ###
    for movie in new_movies: 
        predicted_ratings.append((movie, model.predict(user_id, movie)[3]))          ## Model takes a user and the movie ID number ##
    list_of_movies = sorted(predicted_ratings, key= lambda x: x[1], reverse= True)   ## Sort the list based off the predicted ratings ## 
    return list_of_movies                                                            ## Return the list of predictions and the movie ID

def id_title(ids, movies_list):
    """ Simple Function that returns the movie title with a list of IDs """
    return movies_list[movies_list['movieId'].isin(ids)]['title']

def create_ranked_df(user_list, item_list, movie_list):
    """ Take the list of movies from two model and create a weight dataframe with the rank for the list. 
    ______________________________
    Input - user_list (list) 
          - item_list (list) 
          - movie_list (Dataframe)
    Output - final_df (Dataframe) 
    ______________________________
    Each movie ID will be given a rank and the lists are sorted by the movie ID
    The three lists are made to a DataFrame and sort by the final rank sum.
    """    
    weighted_items = [(rank, item[0]) for rank, item in enumerate(item_list)]   ## Rank each item in list ## 
    weighted_users = [(rank, item[0]) for rank, item in enumerate(user_list)]   ## Rank each item in list ##
    weighted_users = sorted(weighted_users, key= lambda x: x[1])   ## Sort the list to the same movie ID ## 
    weighted_items = sorted(weighted_items, key= lambda x: x[1])
    
    movie_ids = [ID[1] for ID in weighted_users]   ## Grab the ID for the list 
    weight_1 = [weight[0] for weight in weighted_users]   ## Grab the weight of the first list ## 
    weight_2 = [weight[0] for weight in weighted_items]   ## Grab the weight of the second list ## 
    
    df_weighted_movies = pd.DataFrame(list(zip(movie_ids, weight_1, weight_2)), columns = ['Movie Id', 'User Rank', 'Item Rank'])   ## Create the dataframe with the lists
    df_weighted_movies['Final Rank'] = df_weighted_movies['User Rank'] + df_weighted_movies['Item Rank']                            ## Create a new column with the sum of the two ranks
    df_weighted_movies['Movie Id'].replace(to_replace= movie_list['movieId'].values, value=movie_list['title'].values, inplace= True)   ## Replace all the Movie ID with the titles
    final_df = df_weighted_movies.sort_values('Final Rank')   ## Sort the Dataframe with the new ranks 
    
    return final_df

def new_movie(new_genres, movies_list, ratings_list):
    """
    Function that takes the genres from a new movie and give it a rating based off the genres given. 
    ______________________________
    Input - new_genres (list) 
          - movies_list (list) 
          - ratings_list (Dataframe)
    Output - mean (value) 
    ______________________________
    If the movie genre is not in the movies list, the average rating would be returned instead. 
    
    """
    ## Check if there are similar genres already in the list ## 
    if new_genres not in movies_list.genres.unique():
        print('Genre/s not found in movies list: {}'.format(new_genres))   
        return ratings_list.rating.mean()   ## If not, return the mean rating of all movies ## 
    print('Genre Detected: {}'.format(new_genres))
    genre_list = movies_list.loc[movies_list['genres'] == new_genres]['movieId'].values   ## If found, return the rating for the genres average  
    return ratings_list.loc[ratings_list['movieId'].isin(genre_list)]['rating'].mean()
    
def new_review(user_id, movie_id, rating, genres, title):
    if user_id not in user_list:
        np.append(user_list, user_id)
    if movie_id not in movie_id_list:
        add_movie(title,genres)
    reviews = reviews.append({'userId':user_id, 'movieId': movie_id, 'rating': rating},ignore_index= True)
    return reviews
    

def add_review(new_review, original_df, movies_list):
    user_id_list = original_df.userId.unique()
    movie_id_list = movies_list.movieId.unique()
         
    if (new_review.get('user_id') == None) | (new_review['user_id'] not in user_id_list):
        ID = user_id_list[-1] + 1                     ## Give a new ID number 
        print('New user number assignment: {}'.format(ID))
    else:
        ID = new_review['user_id']   ## Use the ID given if exist
    
    movie_id = new_review['movie_id']
    
    if movie_id not in movie_id_list:   ## If the movie is not in the movie dataframe
        movie_id = movie_id_list[-1] + 1   ## Give a new ID from the movies list
        new_movies_list = movies_list.append({'movieId':movie_id, 'title':new_review['title'], 'genres':new_review['genre']}, ignore_index= True)   ## Add the movies information to the movie dataframe
    else:
        new_movies_list = movies_list
        
    changed_df = original_df.append({'userId':ID, 'movieId': movie_id, 'rating': new_review['rating']},ignore_index= True)   ## Add the new review to the ratings dataframe
    return changed_df, new_movies_list