import pandas as pd
from collections import defaultdict
import random
class RandomPRedictor:
    def __init__(self, min, max):
        self.min = min;
        self.max = max;
        self.user_item_data;

    def predict(self, user_id):
        user_ratings = dict()

        return random.randint(self.min, self.max)

    def fit(self, user_item_data):
        self.user_item_data = user_item_data


