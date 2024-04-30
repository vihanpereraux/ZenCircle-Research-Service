from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server
import threading
dispatcher = dispatcher.Dispatcher()
# dispatcher_2 = dispatcher.Dispatcher()
from sklearn.preprocessing import StandardScaler
import time
from joblib import load
import numpy as np
import pandas as pd



ip = "192.168.1.208"
port = 5000

buffer_obj = []

model = load('model.joblib')

# Start time
start_time = time.time()
# Example length required by the model
sequence_length = 500  
# Assuming four features (e.g., 'Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8')
feature_count = 4
# Initialize an empty DataFrame with specified columns
buffered_df = pd.DataFrame(columns=['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8'])
# Preallocate the DataFrame for better performance
buffered_df = pd.DataFrame(index=range(sequence_length), columns=['Alpha_AF7', 'Alpha_AF8', 'Beta_AF7', 'Beta_AF8'])
buffered_df = buffered_df.fillna(0)


# (TP9, AF7, AF8, TP10)

alpha_af7 = []
alpha_af8 = []
printStr = ''
printStr1 = []
charz = []
def start_gathering():
    dispatcher.map("/muse/elements/alpha_absolute", eeg_handler)
    # dispatcher.map("/muse/elements/beta_absolute", eeg_handler2)
    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()


def eeg_handler(address: str,*args):
    # for arg in args:
    #     charz.append(arg) 

    # # print("Alpha Values - ")
    # print(len(args))
    
    if time.time() - start_time < 5: 
        print("Reaching here because more time is there")
        
        for arg in args:
            printStr1.append(arg)  
            
        print(printStr)
        # alpha - AF7, AF8
        buffer_obj.append([printStr1[1], printStr1[2]])
        
        for value in buffer_obj:
            alpha_af7.append(value[0])
        # print(alpha_af7)    
        
        for value in buffer_obj:
            alpha_af8.append(value[1])
        # print(alpha_af8)
        
        new_data = {
            'Alpha_AF7': alpha_af7, 'Alpha_AF8': alpha_af7 
        }
        dummy_display(new_data)
        return
           
        # print("Not Reaching here because more there's no time")
        
        # add_data_to_buffer(new_data)
        
        
def dummy_display(new_data):
    print(new_data)
# new_data2 = {}
# def eeg_handler2(address: str,*args):
#     global new_data2
#     printStr = ''
#     printStr1 = []
    
#     beta_af7 = []
#     beta_af8 = []
    
#     # for arg in args:
#     #     printStr += " "+str(arg)
#     #     printStr1.append(arg) 

#     # print("Beta Values - ")
#     # print(printStr)
    
#     if len(buffer_obj) < 50:
#         for arg in args:
#             printStr += " "+str(arg)
#             printStr1.append(arg)  
            
#         # print(printStr)
#         # beta - AF7, AF8
#         buffer_obj.append([printStr1[1], printStr1[2]])
#         new_data2 = {
#             'Beta_AF7': beta_af7.append(printStr1[1]),
#             'Beta_AF8': beta_af7.append(printStr1[2]) 
#         }
#     else:
#         print("Limit reached for Beta")
#         print(new_data2)
#         # add_data_to_buffer(new_data)
        
        

# def add_data_to_buffer(new_data):
#     global buffered_df, buffer_size
#     # Assuming 'new_data' is a dictionary with keys matching the DataFrame columns
#     buffered_df = pd.DataFrame(new_data, index=[0])
#     print("Reached !!!!!!!")
#     # Append the new row to the DataFrame and drop the oldest row if the buffer is full
#     # buffered_df = pd.concat([buffered_df.iloc[1:], new_row], ignore_index=True)


# def process_data():
#     global buffered_df
#     # Preprocess the data as needed, similar to how it was done pre-training
#     # Ensure this function is defined to handle DataFrame input
#     processed_data = preprocess_data(buffered_df)  
#     # Example: Pass the processed data to a machine learning model
#     prediction = model.predict(processed_data)
#     return prediction


# def preprocess_data(df):
#     # Initialize a scaler based on your training data (assume it's globally defined and fitted)
#     scaler = StandardScaler()

#     # Apply scaling or other transformations
#     # Assume that scaler is already fitted to the training data's range
#     scaled_features = scaler.transform(df)
#     return scaled_features



# if __name__ == "__main__":
start_gathering()
    
        
