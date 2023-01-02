import pandas as pd
import BranjeOcen
import BranjeFilmov as bf
from collections import defaultdict
import random

class RandomPredictor:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def predict(self, user_id):
        user_ratings = dict()
        #min_movieID = self.user_item_data.df["movieID"].min()
        #max_movieID = self.user_item_data.df["movieID"].max()
        list_of_movieIDs = list(set(self.user_item_data.get_all_movies_id()))
        list_of_movieIDs.sort()
        #print('list of ids ', list_of_movieIDs)
        for movieID in list_of_movieIDs:
            user_ratings[movieID] = random.randint(self.min, self.max)
        return user_ratings

    def fit(self, user_item_data):
        self.user_item_data = user_item_data




md = bf.MovieData("data/movies.dat")
print(md.get_title(1))
uid = BranjeOcen.UserItemData("data/user_ratedmovies.dat")
rp = RandomPredictor(1, 5)
rp.fit(uid)
pred = rp.predict(78)
items = [1, 3, 20, 50, 100]
for item in items:
    print("Film: {}, ocena: {}".format(md.get_title(item), pred[item]))
