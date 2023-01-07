import pandas as pd
import BranjeFilmov as br
import datetime
from collections import defaultdict
import numpy as np

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
        return len(self.df['rating'].values)

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

    def get_rating_of_movie(self, movieId):
        return list(self.df[self.df['movieID'] == movieId]['rating'].values)

    def get_all_users(self):
        return list(set(self.df['userID']))

    def get_number_users_rated_movies(self, movie_id1, movie_id2):
        return len(self.df[(self.df['movieID'] == movie_id1) | (self.df['movieID'] == movie_id2)]['userID'])

    def return_numpy_df(self):
        return self.df[['movieID', 'userID', 'rating']].to_numpy()

    def get_rating_movie(self, user_id, movie_id):
        return self.df[(self.df['userID'] == user_id) & (self.df['movieID'] == movie_id)]['rating'].values


# movie id 53355 sonnenallee
uid = UserItemData("data/user_ratedmovies.dat", min_ratings=1000)

#number of users that rated two movies
#print(len((uid.df[(uid.df['movieID'] == 1580) | (uid.df['movieID']==2719)]['userID'])))
# get all from rating from movies

#print(uid.get_rating_movie(50, 78))
'''
users = uid.get_all_users()
#movieID, userID, rating
data_frame_nupmy = uid.df[['movieID', 'userID', 'rating']].to_numpy()
user_avg = dict()
for user in users:
  user_rating = uid.df[uid.df['userID'] == user]['rating']
  user_avg[user] = sum(user_rating)/len(user_rating)

frist_line_in_fromula = 0
movie1_sqrt = 0
movie2_sqrt = 0

p1 = 1580
p2 = 2716
#print(data_frame_nupmy)
data_frame_numpy_filter_movieID1 = data_frame_nupmy[np.where(data_frame_nupmy[:, 0] == p1)]
data_frame_numpy_filter_movieID2 = data_frame_nupmy[np.where(data_frame_nupmy[:, 0] == p2)]
for user in users:
    data_frame_nupmy_filter_userID1 = data_frame_numpy_filter_movieID1[np.where(data_frame_numpy_filter_movieID1[:, 1] == user)]
    data_frame_nupmy_filter_userID2 = data_frame_numpy_filter_movieID2[np.where(data_frame_numpy_filter_movieID2[:, 1] == user)]
    if (data_frame_nupmy_filter_userID1.size > 0 and data_frame_nupmy_filter_userID2.size > 0):
        #print(data_frame_nupmy_filter_userID1[:, -1][0])
        #print(data_frame_nupmy_filter_userID2[:, -1][0])
        avg_from_user = user_avg[user]
        # print('movie1', ratings_movie1[0] - avg_from_user)
        # print('movie2', ratings_movie2[0] - avg_from_user)
        frist_line_in_fromula += ((data_frame_nupmy_filter_userID1[:, -1][0] - avg_from_user) * (data_frame_nupmy_filter_userID2[:, -1][0] - avg_from_user))
        movie1_sqrt += ((data_frame_nupmy_filter_userID1[:, -1][0] - avg_from_user) ** 2)
        movie2_sqrt += ((data_frame_nupmy_filter_userID2[:, -1][0] - avg_from_user) ** 2)

import math
sim = frist_line_in_fromula / (math.sqrt(movie1_sqrt)*math.sqrt(movie2_sqrt))
print("similarity", sim)

#(uid.df[(uid.df['movieID'] == p1) & (uid.df['userID'] == user)]['rating'].values


#get all users id
users = list(set(uid.df['userID']))
#print('users=', users)
#every user calculate avg rating
# go through users and get avg for ratings
user_avg = dict()
for user in users:
  user_rating = uid.df[uid.df['userID'] == user]['rating']
  user_avg[user] = sum(user_rating)/len(user_rating)
  
#print(user_avg)
#print all rating and userId where movieId is 1580
frist_line_in_fromula = 0
movie1_sqrt = 0
movie2_sqrt = 0
for user, avg in user_avg.items(): 
  ratings_movie1 = list(uid.df[(uid.df['movieID']==1580) & (uid.df['userID']== user)]['rating'].values)
  ratings_movie2 = list(uid.df[(uid.df['movieID']==780) & (uid.df['userID']== user)]['rating'].values)
  if ratings_movie1 and ratings_movie2 != []:
    avg_from_user = user_avg[user]
    #print('movie1', ratings_movie1[0] - avg_from_user)
    #print('movie2', ratings_movie2[0] - avg_from_user)
    frist_line_in_fromula += ((ratings_movie1[0] - avg_from_user) * (ratings_movie2[0] - avg_from_user))
    movie1_sqrt += ((ratings_movie1[0]-avg_from_user)**2)
    movie2_sqrt += ((ratings_movie2[0]-avg_from_user)**2)

import math
sim = frist_line_in_fromula / (math.sqrt(movie1_sqrt)*math.sqrt(movie2_sqrt))
print("similarity", sim)
    
#print(uid.df[['movieID','userID', 'rating']])

##n = uid.get_number_rating_movie(50)
#vs = uid.get_sum_rating_movie(50)
#b = 100
#g_avg = (uid.get_sum_rating_all_movies() / uid.nratings())
#avg = (vs + b * g_avg) / (n + b)
#print(avg)
'''

