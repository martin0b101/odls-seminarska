import pandas as pd
import BranjeFilmov as bf
import BranjeOcen as bo


class ViewsPredicator:
    def __init__(self):
        pass

    def fit(self, user_item_data):
        self.user_item_data = user_item_data

    def predict(self, user_id):
        user_ratings = dict()
        list_of_movieIDs = list(set(self.user_item_data.get_all_movies_id()))
        list_of_movieIDs.sort()
        for movieID in list_of_movieIDs:
            user_ratings[movieID] = self.user_item_data.get_number_rating_movie(movieID)
        return user_ratings
    

'''
md = bf.MovieData('data/movies.dat')
uim = bo.UserItemData('data/user_ratedmovies.dat')
vp = ViewsPredicator()
vp.fit(uim)
pred = vp.predict(78)

items = [4993, 5952, 7153, 50, 100]
for item in items:
    print("Film: {}, ocena: {}".format(md.get_title(item), pred[item]))
'''