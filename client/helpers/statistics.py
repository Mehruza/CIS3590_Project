import pandas as pd
from CIS3590_Project.client.helpers.datas import get_stats

def display_statistics(st):
    """Display summary statistics from API"""
    response = get_stats()

    if response.status_code == 200:
        stats_data = response.json()

        # Convert to DataFrame for better display
        stats_df = pd.DataFrame(stats_data)

        st.write("Summary Statistics for All Numeric Fields:")
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.error(f"Error fetching statistics: {response.status_code}")
