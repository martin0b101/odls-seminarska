import pandas as pd
import math


class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold

    def fit(self, user_item_data):
        self.user_item_data = user_item_data

    def predict(self, user_id):
        pass

    def similarity(self, p1, p2):
        #check if number of users that graded two movies are enough
        if (self.user_item_data.get_number_users_rated_movies(p1, p2) < self.min_values):
            return 0.0
        # get all users and calculates avg rating
        user_avg = dict()
        for user in self.user_item_data.get_all_users():
            user_rating = self.user_item_data.df[self.user_item_data.df['userID'] == user]['rating']
            user_avg[user] = sum(user_rating) / len(user_rating)

        frist_line_in_fromula = 0
        movie1_sqrt = 0
        movie2_sqrt = 0
        for user, avg in user_avg.items():
            ratings_movie1 = list(self.user_item_data.df[(self.user_item_data.df['movieID'] == p1) & (self.user_item_data.df['userID'] == user)]['rating'].values)
            ratings_movie2 = list(self.user_item_data.df[(self.user_item_data.df['movieID'] == p2) & (self.user_item_data.df['userID'] == user)]['rating'].values)
            if ratings_movie1 and ratings_movie2 != []:
                avg_from_user = user_avg[user]
                frist_line_in_fromula += ((ratings_movie1[0] - avg_from_user) * (ratings_movie2[0] - avg_from_user))
                movie1_sqrt += ((ratings_movie1[0] - avg_from_user) ** 2)
                movie2_sqrt += ((ratings_movie2[0] - avg_from_user) ** 2)
        self.similarity_result = frist_line_in_fromula / (math.sqrt(movie1_sqrt)*math.sqrt(movie2_sqrt))
        if self.similarity_result < self.threshold:
            return 0.0
        return self.similarity_result

import BranjeFilmov as bf
import BranjeOcen as bo
import Priporocanje as p

md = bf.MovieData('data/movies.dat')
uim = bo.UserItemData('data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = p.Recommender(rp)
rec.fit(uim)
#print(uim.movies)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))