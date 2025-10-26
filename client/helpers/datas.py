import requests
from  CIS3590_Project.client.helpers.utils import *

def get_observations(params):
    response = requests.get(API_URL+OBSERVATIONS_ENDPOINT, params=params)
    return response

def get_stats():
    """Fetch summary statistics from API"""
    response = requests.get(API_URL + STATS_ENDPOINT)
    return response

def get_outliers(params):
    """Fetch outliers from API with optional parameters"""
    response = requests.get(API_URL + OUTLIERS_ENDPOINT, params=params)
    return response