import pandas as pd
from collections import defaultdict


class AverahePredictor:
    def __init__(self, b):
        self.b = b

    def fit(self, user_item_data):
        self.user_item_data = user_item_data
        self.g_avg = self.user_item_data.get_sum_rating_all_movies() / self.user_item_data.nratings()
        print('avg: ', self.g_avg)

    def calculate(self, movie_id):
        vs = self.user_item_data.get_sum_rating_movie(movie_id)
        n = self.user_item_data.get_number_rating_movie(movie_id)
        return (vs + self.b * self.g_avg) / (n + self.b)


    def predict(self, user_id):
        user_ratings = dict()
        list_of_movieIDs = list(set(self.user_item_data.get_all_movies_id()))
        list_of_movieIDs.sort()
        for movieID in list_of_movieIDs:
            user_ratings[movieID] = self.calculate(movieID)
        return user_ratings
    

        



