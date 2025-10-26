

API_URL="http://localhost:5050"
OBSERVATIONS_ENDPOINT = "/api/observations"
STATS_ENDPOINT = "/api/stats"
OUTLIERS_ENDPOINT = "/api/outliers"

# Numerical columns for outlier detection (excluding ROSEM Command Type)
NUMERICAL_COLUMNS = [
    "Latitude", "Longitude", "Number of Sats", "GPS Speed (Kn)", "GPS True Heading",
    "GPS Magnetic Variation", "HDOP", "C Magnetic Heading", "C True Heading",
    "Pitch Angle", "Roll Angle", "C Inside Temp (c)", "DFS Depth (m)", "DTB Height (m)",
    "Total Water Column (m)", "Batt Percent", "Power Watts", "Watt-Hours", "Batt Volts",
    "Batt Ampers", "Time to Empty", "Current Step", "Dist To Next (m)", "Next Speed (kn)",
    "Vehicle Speed (kn)", "Motor Speed CMD", "Next Heading", "Next Long", "Next Lat",
    "Next Depth (m)", "Depth Goal (m)", "Distance to Track (m)", "Fin Pitch R",
    "Fin Pitch L", "Pitch Goal", "Fin Yaw T", "Fin Yaw B", "Yaw Goal", "Fin Roll",
    "DVL-Depth (m)", "DVL -Altitude (m)", "DVL -Water Column (m)", "DVL-FixType",
    "DVL-FixQuality", "DVL-Temperature", "Conductivity (mmhos/cm)", "Temperature (c)",
    "Salinity (ppt)", "Sound Speed (m/s)", "Temp C", "SpCond mS/cm", "Sal ppt",
    "Depth feet", "pH", "pH mV", "Turbid+ NTU", "Chl ug/L", "BGA-PC cells/mL",
    "ODOsat %", "ODO mg/L", "Battery volts"
]