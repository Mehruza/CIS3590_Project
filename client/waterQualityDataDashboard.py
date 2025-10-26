import streamlit as st
import pandas as pd
import plotly.express as px

from helpers.filters import *
from helpers.headers import *
from helpers.observations import display_observations

API_URL = "http://localhost:5050"

display_headers(st)
params = display_filters(st)

display_observations(st, params)

observation_table = st.table