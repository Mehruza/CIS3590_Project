import plotly.express as px
import pandas as pd

def display_salinity_histogram(st, df):
    """Display histogram for salinity distribution"""
    if 'Salinity (ppt)' in df.columns:
        fig = px.histogram(
            df,
            x='Salinity (ppt)',
            nbins=15,
            title='Salinity Distribution',
            labels={'Salinity (ppt)': 'Salinity (ppt)'},
            color_discrete_sequence=['#636EFA']
        )

        fig.update_layout(
            xaxis_title='Salinity (ppt)',
            yaxis_title='Frequency',
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Salinity column not found in data")


def display_temp_salinity_scatter(st, df):
    """Display scatter plot of temperature vs salinity, colored by ODO"""
    required_cols = ['Temperature (c)', 'Salinity (ppt)', 'ODO mg/L']

    if all(col in df.columns for col in required_cols):
        fig = px.scatter(
            df,
            x='Temperature (c)',
            y='Salinity (ppt)',
            color='ODO mg/L',
            title='Temperature vs Salinity (colored by ODO)',
            labels={
                'Temperature (c)': 'Temperature (°C)',
                'Salinity (ppt)': 'Salinity (ppt)',
                'ODO mg/L': 'ODO (mg/L)'
            },
            color_continuous_scale='Viridis',
            hover_data=['ODO mg/L']
        )

        fig.update_layout(
            xaxis_title='Temperature (°C)',
            yaxis_title='Salinity (ppt)'
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Required columns (Temperature, Salinity, ODO) not found in data")


def display_map(st, df):
    """Display map with latitude/longitude and hover data"""
    required_cols = ['Latitude', 'Longitude']

    if all(col in df.columns for col in required_cols):
        # Add hover data columns
        hover_cols = ['Temperature (c)', 'Salinity (ppt)', 'ODO mg/L', 'Date m/d/y   ', 'Time hh:mm:ss']
        available_hover = [col for col in hover_cols if col in df.columns]

        # Calculate center and zoom to fit the data points
        center_lat = df['Latitude'].mean()
        center_lon = df['Longitude'].mean()

        # Calculate zoom level based on data spread
        lat_range = df['Latitude'].max() - df['Latitude'].min()
        lon_range = df['Longitude'].max() - df['Longitude'].min()
        max_range = max(lat_range, lon_range)

        # Zoom level calculation (inverse relationship)
        if max_range < 0.01:
            zoom = 14
        elif max_range < 0.05:
            zoom = 12
        elif max_range < 0.1:
            zoom = 11
        else:
            zoom = 10

        fig = px.scatter_mapbox(
            df,
            lat='Latitude',
            lon='Longitude',
            hover_name='Date m/d/y   ' if 'Date m/d/y   ' in df.columns else None,
            hover_data=available_hover,
            color='Temperature (c)' if 'Temperature (c)' in df.columns else None,
            title='Water Quality Sample Locations',
            zoom=zoom,
            height=900,
            color_continuous_scale='RdYlBu_r'
        )

        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": center_lat, "lon": center_lon},
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Latitude and Longitude columns not found in data")
