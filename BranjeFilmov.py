
import pandas as pd
# Branje filmov

class MovieData:
    def __init__(self, path):
        # encoding not working on mac air so thats why encoiding is set
        self.df = pd.read_csv(path, sep='\t', encoding='ISO-8859-1')

    def get_title(self, movieID):
        data = self.df[self.df.id == movieID]['title']
        return data.values[0]

