import pandas as pd
from requests.exceptions import ConnectionError
from client.helpers.datas import get_observations

def display_observations(st, params):
    #Gotta filter the none values or else 💥
    params = {k:v for k, v in params.items() if v is not None}

    try:
        response = get_observations(params)
        if response.status_code == 200:
            data = response.json()

            st.write(f"Total results: {data['count']}")
            df = pd.DataFrame(data['items'])
            st.dataframe(df)

            # Store in session state for charts
            st.session_state['df'] = df

            return df
        else:
            st.error(f"Error fetching data:\n status code: {response.status_code} \n message {response.json()['message']}")
            return None
    except ConnectionError:
        st.error("⚠️ Unable to connect to the API server. Please ensure the server is running at " + st.code("http://localhost:5050"))
        return None
        
        
        
        