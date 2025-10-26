import pandas as pd
from requests.exceptions import ConnectionError
from client.helpers.datas import get_outliers
from client.helpers.utils import NUMERICAL_COLUMNS

def display_outliers(st):
    """Display outliers detection interface"""
    st.subheader("Outlier Detection")

    # Outlier controls
    col1, col2, col3 = st.columns(3)

    with col1:
        field = st.selectbox(
            "Select Field",
            NUMERICAL_COLUMNS,
            key="outlier_field"
        )

    with col2:
        method = st.selectbox(
            "Detection Method",
            ["iqr", "zscore"],
            key="outlier_method"
        )

    with col3:
        if method == "iqr":
            k = st.number_input("IQR Multiplier (k)", value=1.5, step=0.1, key="outlier_k")
            z = None
        else:
            z = st.number_input("Z-Score Threshold", value=3.0, step=0.1, key="outlier_z")
            k = None

    # Fetch outliers button
    if st.button("Detect Outliers"):
        params = {
            "field": field,
            "method": method
        }
        if k is not None:
            params["k"] = k
        if z is not None:
            params["z"] = z

        try:
            response = get_outliers(params)

            if response.status_code == 200:
                data = response.json()

                st.metric("Outliers Found", data['count'])
                st.write(f"**Field:** {data['field']}")
                st.write(f"**Method:** {data['method']}")
                if data.get('k'):
                    st.write(f"**IQR Multiplier:** {data['k']}")
                if data.get('z'):
                    st.write(f"**Z-Score Threshold:** {data['z']}")

                if data['count'] > 0:
                    outliers_df = pd.DataFrame(data['outliers'])
                    st.dataframe(outliers_df, use_container_width=True)
                else:
                    st.info("No outliers detected with current parameters")
            else:
                st.error(f"Error detecting outliers: {response.status_code}\n, Message: {response.json()['message']}")
        except ConnectionError:
            st.error("⚠️ Unable to connect to the API server. Please ensure the server is running.")
