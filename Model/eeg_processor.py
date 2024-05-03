from pythonosc import dispatcher
from pythonosc import osc_server
from sklearn.preprocessing import StandardScaler
import time
from joblib import load
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from collections import Counter
from pymongo import MongoClient

# from db_connection import update_user_data


ip = "192.168.1.208"
port = 5000
start_time = time.time()
# seconds - based on user's need
time_limit = 20


# Example length required by the model
sequence_length = 500  
# Assuming four features (e.g., 'Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8')
feature_count = 4
# Initialize an empty DataFrame with specified columns
buffered_df = pd.DataFrame(columns=['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8'])
# Preallocate the DataFrame for better performance
buffered_df = pd.DataFrame(index=range(sequence_length), columns=['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8'])
buffered_df = buffered_df.fillna(0)


arr = []
buffer_obj = []
def eeg_handler(address: str,*args):
    if round(time.time() - start_time) < time_limit:
        printStr = ''
        global arr
        global buffer_obj
        
        for arg in args:
            printStr += " "+str(arg)        
            # (TP9, AF7, AF8, TP10)
            arr.append(arg)
        
        buffer_obj.append([arr[1], arr[2]])
        arr = []
        
        # print(printStr)
        # print(buffer_obj)
    
    else:
        execute(buffer_obj)
        arr = []    
        # server.shutdown()

        
arr_2 = []
buffer_obj_2 = []
def eeg_handler2(address: str,*args):
    if round(time.time() - start_time) < time_limit:
        printStr = ''
        global arr_2
        global buffer_obj_2
        
        for arg in args:
            printStr += " "+str(arg)        
            # (TP9, AF7, AF8, TP10)
            arr_2.append(arg)
        
        buffer_obj_2.append([arr_2[1], arr_2[2]])
        arr_2 = []
        
        # print(printStr)
        # print(buffer_obj)
    
    else:
        execute2(buffer_obj_2)
        arr_2 = []    
        server.shutdown()


gbl_alpha_af7 = [] 
gbl_alpha_af8 = [] 
gbl_beta_af7 = [] 
gbl_beta_af8 = []

def execute(buffer_obj):
    print("Execute function executed !")
    
    alpha_af7 = []
    alpha_af8 = []

    for value in buffer_obj:
        alpha_af7.append(value[0])
        alpha_af8.append(value[1])
    
    global gbl_alpha_af7
    global gbl_alpha_af8
    gbl_alpha_af7 = alpha_af7
    gbl_alpha_af8 = alpha_af8
    
    print("*********************************")
    print(buffer_obj)
    print("alpha_af7 - *********************************")
    print(alpha_af7)
    print("alpha_af8 - *********************************")
    print(alpha_af8)
    


def execute2(buffer_obj_2):
    print("Execute function executed !")
    
    beta_af7 = []
    beta_af8 = []

    for value in buffer_obj_2:
        beta_af7.append(value[0])
        beta_af8.append(value[1])
    
    global gbl_beta_af7
    global gbl_beta_af8
    gbl_beta_af7 = beta_af7
    gbl_beta_af8 = beta_af8
    
    print("*********************************")
    print(buffer_obj)
    print("beta_af7 - *********************************")
    print(beta_af7)
    print("beta_af8 - *********************************")
    print(beta_af8)
    combine_data()
    
 
def combine_data():
    new_data = {
        'Alpha_AF7': gbl_alpha_af7, 
        'Alpha_AF8': gbl_alpha_af8, 
        'Beta_AF7': gbl_beta_af7, 
        'Beta_AF8': gbl_beta_af7
    }
    print(len(new_data['Alpha_AF7']))
    print(len(new_data['Alpha_AF8']))
    print(len(new_data['Beta_AF7']))
    print(len(new_data['Beta_AF8']))
    
    preprocess_data(new_data)
    

def preprocess_data(df):
    # Example initial buffer DataFrame setup
    new_df = pd.DataFrame(df)
    
    # Step 3: Replace zero values with NaN temporarily to calculate mean without zeros
    new_df.replace(0, np.nan, inplace=True)
    
    # Step 4: Calculate means excluding NaN (which were zeros)
    column_means = new_df.mean()
    
    # Step 5: Fill NaN values with the respective column means
    new_df.fillna(column_means, inplace=True)
    
    # Initialize a scaler based on your training data (assume it's globally defined and fitted)
    scaler = StandardScaler()
    new_df[['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8']] = scaler.fit_transform(new_df[['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8']])
    
    make_predictions(new_df)



def make_predictions(processed_data):
    model = load('E:\Dev\ZenCircle\ZenCircle-Research-Service\Model\model.joblib')
    predictions = model.predict(processed_data)
    print(predictions)

    # Example array of strings
    string_array =predictions

    # Use Counter to count occurrences of each string
    counter = Counter(string_array)

    # Find the most common and second most common string
    most_common_two = counter.most_common(2)  # Returns the two most frequent strings

    # Access the most common and second most common string and their counts
    most_common_string, most_common_count = most_common_two[0][0], most_common_two[0][1]
    second_most_common_string, second_most_common_count = most_common_two[1][0], most_common_two[1][1]

    print("Most common string:", most_common_string, "Frequency:", most_common_count)
    print("Second most common string:", second_most_common_string, "Frequency:", second_most_common_count)
    
    # executing to the mongo db
    # update_user_data
    update_user_data(most_common_string, second_most_common_string)
    
    

# mongo client init
client = MongoClient('mongodb://localhost:27017/')
database = client['zen-circle-test-db']
collection = database['users']


# gets predicted data and stores in the db
def update_user_data(most_common_string, second_most_common_string):
    update_data = {
            "$set": {
            'username': 'vihanpereraux',
            'eeg_predictions': [most_common_string, second_most_common_string]
            }
        }
    collection.update_one({"username": 'vihanpereraux'}, update_data)
    print("Executed !!!")
    return True



if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/elements/alpha_absolute", eeg_handler)
    dispatcher.map("/muse/elements/beta_absolute", eeg_handler2)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    server.serve_forever()
