import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold

class Model:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, X_train, y_train):
        print("Training model...")
        try:
            self.model.fit(X_train, y_train)
            print("Model trained successfully")
        except Exception as e:
            print(f"Model not trained successfully: {e}")

    def test(self, X_test, y_test, benchmark):
        score = self.model.score(X_test, y_test)
        print(f"Model score: {round(score, 2)}\nPassed benchmark: {score >= benchmark}")
        return score