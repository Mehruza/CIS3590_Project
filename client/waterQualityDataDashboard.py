import streamlit as st
import pandas as pd
import plotly.express as px

from helpers.filters import *
from helpers.headers import *
from helpers.observations import display_observations
from helpers.charts import display_salinity_histogram, display_temp_salinity_scatter, display_map
from helpers.statistics import display_statistics
from helpers.outliers import display_outliers


display_headers(st)
params = display_filters(st)

st.subheader("Observations")
display_observations(st, params)

# Display visualizations if data is available
if 'df' in st.session_state and st.session_state['df'] is not None:
    st.subheader("Salinity Distribution")
    display_salinity_histogram(st, st.session_state['df'])

    st.subheader("Temperature vs Salinity")
    display_temp_salinity_scatter(st, st.session_state['df'])

    st.subheader("Sample Locations")
    display_map(st, st.session_state['df'])

# Statistics panel
st.divider()
st.header("Statistics")
display_statistics(st)

# Outliers view
st.divider()
display_outliers(st)