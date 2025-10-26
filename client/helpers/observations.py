import pandas as pd
from data import get_observations

def display_observations(st, params):
    #Gotta filter the none values or else 💥
    params = {k:v for k, v in params.items() if v is not None}
    
    response = get_observations(params)
    if response.status_code == 200:
        data = response.json()
        
        st.write(f"Total results: {data['count']}")
        df = pd.DataFrame(data=['items'])
        st.dataframe(df)
    else:
        st.error(f"Error fetching data:\n status code: {response.status_code} \n message {response.json()['message']}")
        
        
        
        