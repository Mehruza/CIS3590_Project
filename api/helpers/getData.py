import os
import json

def get_data():

    data_path = os.path.join(os.path.dirname(__file__), "..","..","data")
    clean_file_path = os.path.join(data_path, "cleaned datasets", "consolidated.json")
    with open(clean_file_path, 'r') as read_file:
        data = json.load(read_file)
        return data
