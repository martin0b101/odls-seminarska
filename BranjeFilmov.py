
import pandas as pd
# Branje filmov

class MovieData:
    def __init__(self, path):
        self.df = pd.read_csv(path, sep='\t')

    def get_title(self, movieID):
        data = self.df[self.df.id == movieID]['title']
        return data.values[0]

md = MovieData('data/movies.dat')
print(md.get_title(100))