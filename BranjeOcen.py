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
        return list(set(uid.df['userID']))

    def get_number_users_rated_movies(self, movie_id1, movie_id2):
        return len(self.df[(self.df['movieID'] == movie_id1) | (self.df['movieID'] == movie_id2)]['userID'])



# movie id 53355 sonnenallee
uid = UserItemData("data/user_ratedmovies.dat", min_ratings=1000)

#number of users that rated two movies
#print(len((uid.df[(uid.df['movieID'] == 1580) | (uid.df['movieID']==2719)]['userID'])))

'''
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
'''
import math
import numpy as np
from numpy.linalg import norm

list_of_ratings_man_in_black = uid.get_rating_of_movie(1580)
list_of_ratings_ghosbuster = uid.get_rating_of_movie(2716)

p1 = list_of_ratings_man_in_black
p2 = list_of_ratings_ghosbuster

max_len = max(len(p1), len(p2))
p1 += [0] * (max_len - len(p1))
p2 += [0] * (max_len - len(p2))

simi = np.dot(p1, p2) / (norm(p1)* norm(p2))

print(1-simi)

def mean(lst):
  return sum(lst) / len(lst)

def sum_of_squares(lst):
  deviation = [x - mean(lst) for x in lst]
  return sum([x ** 2 for x in deviation])

def adjusted_cosine_similarity(x, y):
  dot_product =[[(x[i] - mean(x)) * (y[i] - mean(y)) for i in range(len(x))]]
  product_of_sums = (sum_of_squares(x) ** 0.5) * (sum_of_squares(y) ** 0.5)
  return dot_product / product_of_sums

simularity = adjusted_cosine_similarity(p1, p2)
print(simularity)


def adjusted_cosine_similarity(p1, p2):
  mean1 = np.mean(p1)
  mean2 = np.mean(p2)
  
  numerator = 0
  den1 = 0
  den2 = 0
  
  for i in range(len(p1)):
    numerator += (p1[i] - mean1) * (p2[i] - mean2)
    den1 += (p1[i] - mean1) ** 2
    den2 += (p2[i] - mean2) ** 2
  
  den1 = np.sqrt(den1)
  den2 = np.sqrt(den2)
  
  if den1 == 0 or den2 == 0:
    return 0
  
  return numerator / (den1 * den2)

print(adjusted_cosine_similarity(p1, p2))

'''