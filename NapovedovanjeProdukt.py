import pandas as pd
import math
import numpy as np

class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold

    def fit(self, user_item_data):
        self.user_item_data = user_item_data
        self.all_users = self.user_item_data.get_all_users()
        self.df_numpy = self.user_item_data.return_numpy_df()
        # get all users and calculates avg rating
        self.user_avg = dict()
        for user in self.all_users:
            user_rating = self.user_item_data.df[self.user_item_data.df['userID'] == user]['rating']
            self.user_avg[user] = sum(user_rating) / len(user_rating)
        #self.all_sim = self.calculate_all_sim()
    
    # calculates all sim for every movie and returns dict 
    # with {(movieId1, movieId2): similarity} 
    def calculate_all_sim(self):
        # all movies and sim
        movie_sim = dict()
        all_movies_np1 = np.unique(self.df_numpy[:, 0])
        all_movies_np2 = np.unique(self.df_numpy[:, 0])
        for movieId1 in all_movies_np1:
            for movieId2 in all_movies_np2:
                if movieId1 != movieId2:
                    movie_sim[(movieId1, movieId2)] = self.similarity(movieId1, movieId2)
        return movie_sim

    # for every sim that is >0 get the number of rating that user gave movie
    # formula is sum(sim*rating_user)/sum(sim)
    def predict(self, user_id):

        pass

    def similarity(self, p1, p2):
        #check if number of users that graded two movies are enough
        if (self.user_item_data.get_number_users_rated_movies(p1, p2) < self.min_values):
            return 0.0

        frist_line_in_fromula = 0
        movie1_sqrt = 0
        movie2_sqrt = 0
        movie1_df_filter = self.df_numpy[np.where(self.df_numpy[:, 0] == p1)]
        movie2_df_filter = self.df_numpy[np.where(self.df_numpy[:, 0] == p2)]
        for user in self.user_avg.keys():
            ratings_movie1 = movie1_df_filter[np.where(movie1_df_filter[:, 1] == user)]
            ratings_movie2 = movie2_df_filter[np.where(movie2_df_filter[:, 1] == user)]
            if ratings_movie1.size > 0 and ratings_movie2.size > 0:
                avg_from_user = self.user_avg[user]
                rating_movie1_cal = ratings_movie1[:, -1][0] - avg_from_user
                rating_movie2_cal = ratings_movie2[:, -1][0] - avg_from_user
                frist_line_in_fromula += ((rating_movie1_cal) * (rating_movie2_cal))
                movie1_sqrt += ((rating_movie1_cal) ** 2)
                movie2_sqrt += ((rating_movie2_cal) ** 2)
        self.similarity_result = frist_line_in_fromula / (math.sqrt(movie1_sqrt)*math.sqrt(movie2_sqrt))
        if self.similarity_result < self.threshold:
            return 0.0
        return self.similarity_result

    # item is movieId
    def similarItems(self, item, n):
        movies_np_array = np.unique(self.df_numpy[:, 0])
        most_similar = list()
        for movieId in movies_np_array:
            if movieId != item:
                most_similar.append((movieId, self.similarity(item, movieId)))
        most_similar.sort(key=lambda x : x[1], reverse=True)
        return most_similar[:n]


import BranjeFilmov as bf
import BranjeOcen as bo
import Priporocanje as p

md = bf.MovieData('data/movies.dat')
uim = bo.UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = p.Recommender(rp)
rec.fit(uim)


#calculcate predict
dict_movies_sim = rp.calculate_all_sim()
user_id = 78
formula_sum_of_sim_and_rating = 0
sum_of_sim = 0

# for every movie i want to predict i have to get sim and then, get the number of 
# of movie that is similar and then get rating of this movie
for movies, sim in dict_movies_sim.items():
    movieid1, movieid2 = movies
    if sim > 0:
        sum_of_sim += sim
        rating_movie1 = uim.get_rating_movie(user_id, movieid1)
        rating_movie2 = uim.get_rating_movie(user_id, movieid2)
        formula_sum_of_sim_and_rating += (sim * rating_movie1)
        formula_sum_of_sim_and_rating += (sim * rating_movie2)




'''
#print(uim.movies)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))
'''
'''
import numpy as np

movies = np.array(list(set(uim.get_all_movies_id())))
N = print(len(movies))
top_20_most_similar_movies = dict()
for movie1 in movies:
    for movie2 in movies:
        if movie1 != movie2:
            top_20_most_similar_movies[(movie1, movie2)] = (md.get_title(movie1), md.get_title(movie2))


top_20_most_similar_movies_sorted = sorted(top_20_most_similar_movies)


print(top_20_most_similar_movies_sorted)
similarty_all_movies = list()
for moveIds in top_20_most_similar_movies_sorted:
    movieId1, movieId2 = moveIds
    name = f"Film1: {md.get_title(movieId1)}, Film2: {md.get_title(movieId2)}, podobnost:"
    podobnost = rp.similarity(movieId1, movieId2)
    similarty_all_movies.append((name, podobnost))

similarty_all_movies.sort(key=lambda x : x[1], reverse=True)

for name_sim in similarty_all_movies[:20]:
    name, sim = name_sim
    print(f'{name} {sim}')
    #print("Film1 ", md.get_title(movieId1), " Film2 ", md.get_title(movieId2), "similarity: ", rp.similarity(movieId1, movieId2))

'''

'''
rec_items = rp.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))
'''

