# # import numpy as np
# # import pandas as pd
# # import seaborn as sns
# # import matplotlib.pyplot as plt
# # from sklearn import preprocessing, svm
# # from sklearn.model_selection import train_test_split
# # from sklearn.linear_model import LogisticRegression
# # from sklearn.model_selection import GroupKFold

# # class Model:
# #     def __init__(self):
# #         self.model = LogisticRegression()

# #     def train(self, X_train, y_train): 
# #         pass 
# #         # This trains the model. X_train is the input training data, y_train is the output training data. 
# #         # This should train the model

# #     def test(self, X_test, y_test, benchmark):
# #         score = self.model.score(X_test, y_test)
# #         print(f"Model score: {round(score, 2)}\nPassed benchmark: {score >= benchmark}")
# #         return score

# #     def process_data(self, data):
# #         # LIAM
# #         # run the data (provided by the user input in the website) through the model, and get an output
# #         return "0.67" # return the output as a string, which will be shown on the website
    
# # if __name__ == "__main__":
# #     # TEST CODE - WILL NOT ACTUALLY RUN IN THE WEB PAGE 
# #     # There is a copy of this code in main.py which actually runs, this is just for easier testing
        
# #     from data_extraction import set_training_ratio, get_testing_data, get_training_data
# #     percentage_training_data = 70 # % of the total data used as training data (the rest is used as test data)

# #     # Data extraction 
# #     set_training_ratio(percentage_training_data)
# #     X_train, y_train = get_training_data()
# #     X_test, y_test = get_testing_data()

# #     # Model training
# #     model = Model()
# #     model.train(X_train, y_train)
# #     print("\n\n}---{STATISTICS}---{")
# #     model.test(X_test, y_test, 0.8)

# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from sklearn import preprocessing, svm
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import GroupKFold


# class Model:
#     def __init__(self):
#         # You can tweak these hyperparameters if needed
#         self.model = LogisticRegression(max_iter=1000)  # higher max_iter for convergence
#         self.label_encoder = None   # if labels are strings, we’ll encode them

#     def train(self, X_train, y_train):
#         """
#         Train the logistic regression model on the given training data.
#         X_train: 2D array-like (n_samples, n_features)
#         y_train: 1D array-like (n_samples,)
#         """
#         # If y is not numeric (e.g. ["A","B"]), encode it
#         if not np.issubdtype(np.array(y_train).dtype, np.number):
#             self.label_encoder = preprocessing.LabelEncoder()
#             y_train = self.label_encoder.fit_transform(y_train)

#         self.model.fit(X_train, y_train)

#     def test(self, X_test, y_test, benchmark):
#         """
#         Evaluate the model on test data and print score and benchmark status.
#         """
#         # Apply same label encoding on y_test if we used it during training
#         if self.label_encoder is not None:
#             y_test = self.label_encoder.transform(y_test)

#         score = self.model.score(X_test, y_test)
#         print(f"Model score: {round(score, 2)}\nPassed benchmark: {score >= benchmark}")
#         return score

#     def process_data(self, data):
#         """
#         data: features extracted from ONE audio sample (list/1D array of shape (n_features,))
#               or multiple samples (2D array of shape (n_samples, n_features))

#         Returns: string probability (0–1) of being class 'A' (or class 1 if numeric labels).
#         """
#         # Ensure data is 2D
#         data = np.array(data)
#         if data.ndim == 1:
#             data = data.reshape(1, -1)

#         # Get class probabilities: shape (n_samples, n_classes)
#         proba = self.model.predict_proba(data)  # returns probability for each class[web:1][web:7]

#         # Decide which column corresponds to "object A"
#         # Case 1: original labels were strings like ["A","B"]
#         if self.label_encoder is not None:
#             # Find index of label "A" if it exists; otherwise use the positive class (last column)
#             classes = self.label_encoder.classes_
#             if "A" in classes:
#                 idx_A = np.where(classes == "A")[0][0]
#             else:
#                 idx_A = -1  # fallback: last class
#         else:
#             # Numeric labels: assume class 1 is "object A"
#             # In binary logistic regression, classes_ is typically [0, 1][web:5]
#             classes = self.model.classes_
#             if 1 in classes:
#                 idx_A = np.where(classes == 1)[0][0]
#             else:
#                 idx_A = -1  # fallback: last class

#         # For a single input, take the first sample's probability
#         prob_A = float(proba[0, idx_A])

#         # Return as string, e.g. "0.67"
#         return f"{prob_A:.2f}"

    
# if __name__ == "__main__":
#     # TEST CODE - WILL NOT ACTUALLY RUN IN THE WEB PAGE 
#     # There is a copy of this code in main.py which actually runs, this is just for easier testing
        
#     from data_extraction import set_training_ratio, get_testing_data, get_training_data
#     percentage_training_data = 70  # % of the total data used as training data (the rest is used as test data)

#     # Data extraction 
#     set_training_ratio(percentage_training_data)
#     X_train, y_train = get_training_data()
#     X_test, y_test = get_testing_data()

#     # Model training
#     model = Model()
#     model.train(X_train, y_train)
#     print("\n\n}---{STATISTICS}---{")
#     model.test(X_test, y_test, 0.8)

#     # Example of running one audio sample (feature vector) through the model
#     # fake_sample = X_test[0]  # or some new processed audio
#     # print("Predicted P(object A):", model.process_data(fake_sample))

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing
import random

class Model:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.label_encoder = None

    def train(self, X_train, y_train):
        if not np.issubdtype(np.array(y_train).dtype, np.number):
            self.label_encoder = preprocessing.LabelEncoder()
            y_train = self.label_encoder.fit_transform(y_train)
        self.model.fit(X_train, y_train)

    def test(self, X_test, y_test, benchmark):
        if self.label_encoder is not None:
            y_test = self.label_encoder.transform(y_test)
        score = self.model.score(X_test, y_test)
        print(f"Model score: {round(score, 2)}\nPassed benchmark: {score >= benchmark}")
        return score

    # def process_data(self, data):
    #     data = np.array(data)
    #     if data.ndim == 1:
    #         data = data.reshape(1, -1)
    #     proba = self.model.predict_proba(data)
        
    #     # Probability of Parkinson's (class 1)
    #     idx_parkinsons = np.where(self.model.classes_ == 1)[0][0] if 1 in self.model.classes_ else -1
    #     prob_parkinsons = float(proba[0, idx_parkinsons])
    #     return f"{prob_parkinsons:.2f}"

    def process_data(self, data):
        # fake one for prototype, simply a randomiser
        
        x = random.randint(0, 40)
        return f"{x/100}"