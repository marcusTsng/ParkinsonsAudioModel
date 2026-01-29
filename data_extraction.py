from ucimlrepo import fetch_ucirepo

data = None

# fetch dataset 
def _fetch(): 
    global data
    print("Fetching data...")
    try:
        d = fetch_ucirepo(id=174) 
        data_X = d.data.features 
        data_y = d.data.targets 
        data = [data_X, data_y]
        print("Data fetched successfully")
        _isolate()
        return data
    except Exception as e:
        print(f"Failed to fetch data: {e}")

def _isolate():
    print("Isolating data...")
    print("Data isolated successfully")
    pass

def get_training_data(): # UPDATE LATER
    if data == None: _fetch()
    return data[0], data[1]

def get_testing_data(): # UPDATE LATER
    if data == None: _fetch()
    return data[0], data[1]
  
# metadata 
# print(database.metadata) 
  
# # variable information 
# print(database.variables) 