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

    def process_data(self, data):
        # LIAM
        # run the data (provided by the user input in the website) through the model, and get an output
        return "0.67" # return the output as a string, which will be shown on the website
    
if __name__ == "__main__":
    # TEST CODE - WILL NOT ACTUALLY RUN IN THE WEB PAGE 
    # There is a copy of this code in main.py which actually runs, this is just for easier testing
        
    from data_extraction import set_training_ratio, get_testing_data, get_training_data
    percentage_training_data = 70 # % of the total data used as training data (the rest is used as test data)

    # Data extraction 
    set_training_ratio(percentage_training_data)
    X_train, y_train = get_training_data()
    X_test, y_test = get_testing_data()

    # Model training
    model = Model()
    model.train(X_train, y_train)
    print("\n\n}---{STATISTICS}---{")
    model.test(X_test, y_test, 0.8)