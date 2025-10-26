import requests
from utils import API_URL

def get_observations(params):
    response = requests.get(API_URL, params=params)
    return response