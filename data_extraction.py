import pandas as pd
from ucimlrepo import fetch_ucirepo

data = None
train_data = None
test_data = None
train_ratio = 100 

# fetch dataset 
def _fetch_and_split():
    global data, train_data, test_data, train_ratio
    
    print("Fetching dataset...")
    try:
        wine = fetch_ucirepo(id=174)
        X_full = wine.data.features
        y_full = wine.data.targets
        
        data = [X_full, y_full]
        print(f"Dataset loaded: {len(X_full)} rows")
        
        # Now do the split
        _perform_split()
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False
    return True


def _perform_split():
    """Split the full data according to current train_ratio"""
    global train_data, test_data, data, train_ratio
    
    if data is None or len(data) != 2:
        print("No data available to split")
        return
    
    print(f" Splitting data (train ratio = {train_ratio:.2%})...")
    
    X_full, y_full = data
    
    # Combine so we can shuffle together
    df = pd.concat([X_full, y_full], axis=1)
    
    # Shuffle
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Calculate split point
    n_total = len(df_shuffled)
    n_train = int(n_total * train_ratio)
    
    # Split
    train_df = df_shuffled.iloc[:n_train]
    test_df  = df_shuffled.iloc[n_train:]
    
    # Separate features and target again
    train_data = [train_df.iloc[:, :-1], train_df.iloc[:, -1]]
    test_data  = [test_df.iloc[:, :-1],  test_df.iloc[:, -1]]
    
    print(f"→ Training set: {len(train_data[0]):,} rows ({train_ratio:.1%})")
    print(f"→ Test set:     {len(test_data[0]):,} rows")
    print("Split complete")

# def _fetch(): 
#     global data
#     print("Fetching data...")
#     try:
#         d = fetch_ucirepo(id=174) 
#         data_X = d.data.features 
#         data_y = d.data.targets 
#         data = [data_X, data_y]
#         print("Data fetched successfully")
#         _isolate()
#         return data
#     except Exception as e:
#         print(f"Failed to fetch data: {e}")

# def _isolate():
#     print("Isolating data...")
#     global train_ratio

#     # train_data = ?
#     # test_data = ?

#     X, y = data[0], data[1]           # features and targets
    
#     # Optional: shuffle once (recommended for most datasets)
#     df = pd.concat([X, y], axis=1).sample(frac=1, random_state=42).reset_index(drop=True)
    
#     # Split point
#     n_train = int(len(df) * train_ratio)
    
#     # Split
#     train_df = df.iloc[:n_train]
#     test_df  = df.iloc[n_train:]
    
#     # Separate features and targets again
#     train_data = [train_df.iloc[:, :-1], train_df.iloc[:, -1:]]   # last column = target
#     test_data  = [test_df.iloc[:, :-1],  test_df.iloc[:, -1:]]
    
#     print(f"Training set: {len(train_data[0]):,} rows ({train_ratio*100:.1f}%)")
#     print(f"Testing set:  {len(test_data[0]):,} rows")

#     print("Data isolated successfully")
#     pass

def get_training_data(): # UPDATE LATER
    if data == None: _fetch_and_split()
    return train_data
    # return train_data[0], train_data[1]

def get_testing_data(): # UPDATE LATER
    if data == None: _fetch_and_split()
    return test_data#[0], test_data[1]

def set_training_ratio(percentage : float):
    global train_ratio 
    train_ratio = percentage/100


# metadata 
# print(database.metadata) 
  
# # variable information 
# print(database.variables) 