import pandas as pd
import BranjeFilmov as br
import datetime
from collections import defaultdict

# Branje ocen
class UserItemData:

    #data from table
    #konstruktor

    def __init__(self, path, from_date=None, to_date=None, min_ratings=0):
        self.df = pd.read_csv(path, "\t", encoding='ISO-8859-1')

        #split from date to day, month, year
        if (from_date != None):
            from_date_a = from_date.split('.')
            to_date_a = to_date.split('.')
            # format of date is like that year-month-day
            from_date_datef = str(f'{from_date_a[2]}-{from_date_a[1]}-{from_date_a[0]}')
            to_date_datef = str(f'{to_date_a[2]}-{to_date_a[1]}-{to_date_a[0]}')
            #make new column dates
            self.df['dates'] = self.df["date_year"].astype(str).str.cat(self.df[['date_month', 'date_day']].astype(str), sep='-')
            self.df['dates'] = pd.to_datetime(self.df['dates'])
            self.df = self.df[self.df['dates'].between(from_date_datef, to_date_datef, inclusive=True)]

        self.df = self.df.groupby("movieID").filter(lambda ratings: len(ratings) >= min_ratings)

    def nratings(self):
        return len(self.df['rating'])

    def get_watched_movie_list(self, userId):
        return self.df[self.df["userID"] == userId]['movieID'].values
    
    def get_all_movies_id(self):
        return self.df['movieID'].values

    #vs - vsota vseh ocen za film movieId
    def get_sum_rating_movie(self, movieId):
        return sum(self.df[self.df['movieID'] == movieId]['rating'])
   

    def get_sum_rating_all_movies(self):
        return sum(self.df['rating'])
    
    # n - stevilo ocen ki jih je dobil film
    def get_number_rating_movie(self, movieId):
        return len(self.df[self.df['movieID'] == movieId])

# movie id 53355 sonnenallee
uid = UserItemData("data/user_ratedmovies.dat")
#n = uid.get_number_rating_movie(53355)
#vs = uid.get_sum_rating_movie(53355)
#b = 0
#g_avg = (uid.get_sum_rating_all_movies() / uid.nratings())
#avg = (vs + b * g_avg) / (n + b)
#print(avg)

