import pandas as pd
from collections import defaultdict
import BranjeFilmov as bf
import BranjeOcen as bo
import NakljucniPredikator as np
import PovprecniPredikator as pp

class Recommender:
    def __init__(self, predicator):
        self.predicator = predicator
    
    def fit(self, user_item_data):
        self.user_item_data = user_item_data
        self.predicator.fit(self.user_item_data)

    def recommend(self, userID, n=10, rec_seen=True):
        predicted_grade = self.predicator.predict(userID)
        recommendet_movies = []
        watched_movie_list = list(self.user_item_data.get_watched_movie_list(userID))
        if (rec_seen):
        
            for movieId, grade in predicted_grade.items():
                if movieId in watched_movie_list:
                    if len(recommendet_movies) == n:
                        break
                    recommendet_movies.append((movieId, grade))
        else:
            for movieId, grade in predicted_grade.items():
                if movieId not in watched_movie_list:
                    if len(recommendet_movies) == n:
                        break
                    recommendet_movies.append((movieId, grade))
        return recommendet_movies

md = bf.MovieData('data/movies.dat')
uim = bo.UserItemData('data/user_ratedmovies.dat')
rp = pp.AverahePredictor(0)
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for t in rec_items:
    idmovie, val = t
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))