Introduction
In this project, you will transform raw water quality data into an interactive data service. You will:

Load CSV files containing water quality observations.

Clean the data by removing outliers using the z-score method.

Store the cleaned data in a NoSQL database (MongoDB or mongomock locally).

Build a Flask REST API to make the data available with filters and statistics.

Develop a Streamlit client that requests data from your API, displays tables, and creates interactive Plotly charts.

This assignment connects the full pipeline:
CSV → Cleaning → Database → API → Client (Visualization)

Learning Outcomes
By completing this assignment, you will:

Practice ETL (Extract, Transform, Load) by reading CSVs, cleaning data, and loading into a database.

Learn how to design and build REST APIs with Flask.

Understand how a client (Streamlit) communicates with an API.

Create interactive data visualizations with Plotly.

Tech Requirements
Package Current / Recent Version(s) Notes / constraints
Flask 3.1.2 (latest release) PyPILinks to an external site. Flask 3.x is supported; Flask’s changelog shows releases up to 3.1.x
requests 2.32.5 (latest) PyPI+1Links to an external site. requests officially supports Python 3.9+
pandas 2.3.x series (e.g. 2.3.3) Pandas+1Links to an external site. Pandas 2.3 is one of the newer stable series compatible with Python 3.10+
pymongo 4.x series (e.g. 4.9.2) PyMongo DocumentationLinks to an external site. PyMongo 4.x is the modern major line; e.g. version 4.9.2 is referenced in the changelog. PyMongo DocumentationLinks to an external site.
mongomock 4.x or above (adapts to PyMongo) PyPILinks to an external site. The mongomock project encourages using version 4+ so it can adapt its API to the installed PyMongo version. PyPILinks to an external site.
streamlit 1.50.0 (latest as of Sept 2025) Streamlit DocsLinks to an external site. Streamlit’s release notes show 1.50.0 as the current version. Streamlit DocsLinks to an external site.
plotly 6.0.0 (latest major) GitHubLinks to an external site. Plotly’s release notes indicate the minimum supported version is now 7.0.0 (for some dependencies) and that 6.0.0 is a major version. GitHubLinks to an external site.
You may use mongomock for zero-install development. If you have MongoDB locally, you may use it. Your code must run with either by switching the client creation.

Data
I will provide multiple CSVs with fields like:

Latitude,Longitude,Time,Date,Number of Sats,GPS Speed (Kn),GPS True Heading,GPS Magnetic Variation,HDOP,C Magnetic Heading,C True Heading,Pitch Angle,Roll Angle,C Inside Temp (c),DFS Depth (m),DTB Height (m),Total Water Column (m),Batt Percent,Power Watts,Watt-Hours,Batt Volts,Batt Ampers,Batt State,Time to Empty,Current Step,Dist To Next (m),Next Speed (kn),Vehicle Speed (kn),Motor Speed CMD,Next Heading,Next Long,Next Lat,Next Depth (m),Depth Goal (m),Vehicle State,Error State,Distance to Track (m),Fin Pitch R,Fin Pitch L,Pitch Goal,Fin Yaw T,Fin Yaw B,Yaw Goal,Fin Roll,DVL-Depth (m),DVL -Altitude (m),DVL -Water Column (m),DVL-FixType,DVL-FixQuality,DVL-Temperature,Conductivity (mmhos/cm),Temperature (c),Salinity (ppt),Sound Speed (m/s),Date m/d/y ,Time hh:mm:ss,Temp C,SpCond mS/cm,Sal ppt,Depth feet,pH,pH mV,Turbid+ NTU,Chl ug/L,BGA-PC cells/mL,ODOsat %,ODO mg/L,Battery volts,ROSEM Command Type
You may assume timestamps are ISO or parseable by pandas; numeric fields should be floats.

Part 1 — Data Cleaning & Database Setup (30 pts)
Load the CSV files (provided).
Example columns:

timestamp, latitude, longitude, temperature, salinity, odo
Clean the data using the z-score method:

Compute z-scores for numeric fields (temperature, salinity, odo).

Drop any row where any field has |z| > 3.0

Report:

Total rows originally

Rows removed as outliers

Rows remaining after cleaning

Insert the cleaned data into a NoSQL database:

Use MongoDB (if installed) or mongomock (for in-memory DB).

Store the data in a database called water_quality_data and a collection called asv_1.

Index at least one field (e.g., timestamp or temperature) to demonstrate performance awareness (OPTIONAL).

Part 2 — Flask REST API (40 pts)
You will expose your cleaned data through a REST API. All endpoints must return JSON.

Required Endpoints
Health check
GET /api/health → { "status": "ok" }

Observations
GET /api/observations → return documents with optional query parameters:

start / end (ISO timestamps)

min_temp, max_temp

min_sal, max_sal

min_odo, max_odo

limit (default 100, max 1000)

skip (for pagination)

Example response:

{ "count": 503, "items": [ {"timestamp": "...", "temperature": 27.2, "salinity": 35.1, "odo": 6.7}, ... ] }
Statistics
GET /api/stats → return summary stats for numeric fields:

count, mean, min, max, and percentiles (25%, 50%, 75%).

Outliers
GET /api/outliers?field=temperature&method=iqr&k=1.5

Allow re-checking outliers on demand using IQR or z-score.

Return a list of flagged records.

Part 3 — Streamlit Client (30 pts)
You will create a Streamlit app that acts as the client for your API.

Requirements
Controls panel (sidebar):

Date range

Min/max filters (temperature, salinity, odo)

Limit and pagination

Data table:

Display results from /api/observations.

Visualizations (at least 3 Plotly charts):

Line chart (e.g., temperature over time)

Histogram (e.g., salinity distribution)

Scatter plot (e.g., temperature vs salinity, color by ODO)

Maps (e.g., latitude, longitude and the dataframe displayed as user hovers over the path)
Statistics panel:

Call /api/stats and display summary stats.

Outliers view:

Call /api/outliers and display flagged records.

Deliverables
Code repository with:

/data/ → CSV files (raw + cleaned)

/api/ → Flask API

/client/ → Streamlit app

README.md with setup instructions and API documentation

requirements.txt

Demo video (≤5 minutes) showing:

Loading & cleaning the CSVs

Running the API

Using the Streamlit client

Short write-up (1–2 pages) explaining:

How you cleaned the data (z-score results)

How you designed your endpoints

What you learned
