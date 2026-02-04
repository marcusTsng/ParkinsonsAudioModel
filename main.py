print("Loading...")

from data_extraction import get_training_data, get_testing_data, set_training_ratio
from machine_learning import Model

# INTERFACE
print("\n\n}---{MODEL TRAINING INTERFACE}---{")
percentage_training_data = float(input("Percentage used as training data /% (0-100): "))

print("Loading...")

# Data extraction 
set_training_ratio(percentage_training_data)
X_train, y_train = get_training_data()
X_test, y_test = get_testing_data()

model = Model()
model.train(X_train, y_train)
print("\n\n}---{STATISTICS}---{")
model.test(X_test, y_test, 0.8)