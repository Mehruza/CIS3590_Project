

def apply_filters(filtered_df, **filters):
    import pandas as pd

    # Create datetime column if it doesn't already exist
    if 'datetime' not in filtered_df.columns:
        if 'Date m/d/y   ' in filtered_df.columns and 'Time hh:mm:ss' in filtered_df.columns:
            filtered_df['datetime'] = pd.to_datetime(
                filtered_df['Date m/d/y   '] + ' ' + filtered_df['Time hh:mm:ss'],
                format='%m/%d/%y %H:%M:%S',
                errors='coerce'
            )

    # Apply filters conditionally
    if filters.get("min_temp") is not None:
        filtered_df = filtered_df[filtered_df['Temperature (c)'] >= filters["min_temp"]]
    if filters.get("max_temp") is not None:
        filtered_df = filtered_df[filtered_df['Temperature (c)'] <= filters["max_temp"]]
    if filters.get("min_sal") is not None:
        filtered_df = filtered_df[filtered_df['Salinity (ppt)'] >= filters["min_sal"]]
    if filters.get("max_sal") is not None:
        filtered_df = filtered_df[filtered_df['Salinity (ppt)'] <= filters["max_sal"]]
    if filters.get("min_odo") is not None:
        filtered_df = filtered_df[filtered_df['ODO mg/L'] >= filters["min_odo"]]
    if filters.get("max_odo") is not None:
        filtered_df = filtered_df[filtered_df['ODO mg/L'] <= filters["max_odo"]]

    # Handle timestamp filtering if provided (ISO format expected)
    if filters.get("start") is not None:
        start_dt = pd.to_datetime(filters["start"], errors='coerce')
        if start_dt is not None and 'datetime' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['datetime'] >= start_dt]

    if filters.get("end") is not None:
        end_dt = pd.to_datetime(filters["end"], errors='coerce')
        if end_dt is not None and 'datetime' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['datetime'] <= end_dt]
    
    # Get count before pagination
    count = len(filtered_df)

    # Get pagination parameters
    skip = filters.get("skip", 0)
    limit = filters.get("limit", 100)

    # Enforce max limit of 1000
    if limit > 1000:
        limit = 1000

    # Apply pagination
    paginated_df = filtered_df.iloc[skip:skip+limit]

    # Convert to dict and return with count
    return {
        "count": count,
        "items": paginated_df.to_dict('records')
    }