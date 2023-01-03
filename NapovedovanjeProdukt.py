import pandas as pd


class ItemBasedPredictor:
    def __init__(self, min_values=0, threshold=0):
        self.min_values = min_values
        self.threshold = threshold

    def fit(self, user_item_data):
        self.user_item_data = user_item_data

    def predict(self, user_id):
        pass

    def similarity(self, p1, p2):
        self.product_similarity = p1 * p2
        return self.product_similarity

