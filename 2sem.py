import pickle
import pandas as pd

# Branje ocen
class UserItemData:

    #data from table
    #konstruktor
    '''
    def __init__(self, path, start_date='1.1.1900', end_date='1.1.2025', min_ratings=1):
        #print("path", path, start_date, end_date, min_ratings)
        dbfile = open(path, 'r') 
        dbfile.seek(0)
        db = pickle.load(dbfile)
        print(db)
        dbfile.close()
        '''
    

    def __init__(self, path, from_date='0.0.0000', to_date='99.99.9999', min_ratings=1):
        self.df = pd.read_table(path)
        #split from date to day, month, year
        from_date_a = from_date.split('.')
        to_date_a = to_date.split('.')
        print("from date ",from_date_a)
        print("to date ", to_date_a)
        # date can be from 12.1.2007 to 16.2.2008, so date should be between
        self.dffilter_year = self.df[(self.df.date_year >= int(from_date_a[2])) & (self.df.date_year <= int(to_date_a[2]))]
        self.dffilter_y_m = self.dffilter_year[(self.df.date_month >= int(from_date_a[1])) & (self.df.date_month <= int(to_date_a[1]))]
        self.dfdone = self.dffilter_y_m[(self.df.date_day >= int(from_date_a[0])) & (self.df.date_day <= int(to_date_a[0]))]


    def nratings(self):
        print(self.dfdone)
        print(len(self.dfdone))
    
#uid = UserItemData("data/user_ratedmovies.dat", from_date='12.1.2007', to_date='16.2.2008')
#uid.nratings()

# Branje filmov

class MovieData:
    def __init__(self, path):
        self.df = pd.read_table(path, encoding='utf-8')

    def get_title(self, movieID):
        print(self.df)

md = MovieData('data/movies.dat')
md.get_title(1)