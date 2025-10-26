

def display_filters(st):
    st.sidebar.header("Filters")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    # Temperature filters
    st.sidebar.subheader("Temperature (°C)")
    min_temp = st.sidebar.number_input("Min Temperature", value=None, step=0.1)
    max_temp = st.sidebar.number_input("Max Temperature", value=None, step=0.1)

    # Salinity filters
    st.sidebar.subheader("Salinity (ppt)")
    min_sal = st.sidebar.number_input("Min Salinity", value=None, step=0.1)
    max_sal = st.sidebar.number_input("Max Salinity", value=None, step=0.1)

    # ODO filters
    st.sidebar.subheader("ODO (mg/L)")
    min_odo = st.sidebar.number_input("Min ODO", value=None, step=0.1)
    max_odo = st.sidebar.number_input("Max ODO", value=None, step=0.1)

    # Pagination stuff...
    st.sidebar.subheader("Pagination")
    limit = st.sidebar.slider(
        "Results per page", min_value=10, max_value=1000, value=100, step=10)
    skip = st.sidebar.number_input("Skip rows", min_value=0, value=0, step=100)
    st.divider()

    return {
        "start": start_date,
        "end": end_date,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "min_odo": min_odo,
        "max_odo": max_odo,
        "min_sal": min_sal,
        "max_sal": max_sal,
        "limit": limit,
        "skip": skip
    }
