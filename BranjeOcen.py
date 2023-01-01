
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
        print(len(self.df['userID']))

    def get_all_items_of_user(self, user_id):
        return self.df



