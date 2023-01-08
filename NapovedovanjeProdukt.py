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
        self.all_sim = self.calcualte_all_sim_with_numpy()
    
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

    def calcualte_all_sim_with_numpy(self):
        movis_sim_np_array = []
        all_movies_np1 = np.unique(self.df_numpy[:, 0])
        all_movies_np2 = np.unique(self.df_numpy[:, 0])
        for movieId1 in all_movies_np1:
            for movieId2 in all_movies_np2:
                if movieId1 != movieId2:
                    similarity = self.similarity(movieId1, movieId2)
                    if similarity > 0:
                        movis_sim_np_array.append([movieId1, movieId2, similarity])
        return np.array(movis_sim_np_array)

    def calcualte_all_sim_with_numpy(self):
        movis_sim_np_array = []
        all_movies_np1 = np.unique(self.df_numpy[:, 0])
        all_movies_np2 = np.unique(self.df_numpy[:, 0])
        for movieId1 in all_movies_np1:
            for movieId2 in all_movies_np2:
                if movieId1 != movieId2:
                    similarity = self.similarity(movieId1, movieId2)
                    if similarity > 0:
                        movis_sim_np_array.append([movieId1, movieId2, similarity])
        return np.array(movis_sim_np_array)


    # for every sim that is >0 get the number of rating that user gave movie
    # formula is sum(sim*rating_user)/sum(sim)
    def predict(self, user_id):
        predict_movie_ratings = dict()
        for movieId in self.all_sim[:, 0]:
            pred_for_user = self.all_sim[np.where(self.all_sim[:, 0] == movieId)]
            formula_first_line = 0
            sum_sim = 0
            i = 0
            for movieid2 in pred_for_user[:, 1]:
                rating = uim.get_rating_movie(user_id, int(movieid2))
                if rating.size > 0:
                    sim = pred_for_user[i, 2]
                    sum_sim += sim
                    formula_first_line += (sim*rating[0])
                i+=1
            pred = formula_first_line/sum_sim

            predict_movie_ratings[movieId] = pred
        return predict_movie_ratings

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

    def return_top20_most_sim(self):
        sorted_sim = self.all_sim[self.all_sim[:, 2].argsort()][::-1]
        return sorted_sim[:20]


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


print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print(rp.return_top20_most_sim)