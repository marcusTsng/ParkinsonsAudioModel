from data_extraction import get_training_data, get_testing_data
from machine_learning import Model

# Data extraction 
X_train, y_train = get_training_data()
X_test, y_test = get_testing_data()

model = Model()
model.train(X_train, y_train)
model.test(X_test, y_test, 0.8)