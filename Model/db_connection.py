from pymongo import MongoClient


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

update_user_data()