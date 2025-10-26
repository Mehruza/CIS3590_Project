# Water Quality Data Service

A full-stack data pipeline for water quality observations collected by autonomous surface vehicles (ASVs). This project demonstrates the complete ETL workflow: CSV → Cleaning → Database → API → Visualization.

## Project Overview

This system transforms raw water quality sensor data into an interactive data service with:

- **ETL Pipeline**: Load CSV files, clean data using z-score outlier detection, store in MongoDB
- **REST API**: Flask-based API with filtering, statistics, and outlier detection endpoints
- **Interactive Dashboard**: Streamlit client with real-time data visualization using Plotly

**Data Pipeline Flow:**

```
CSV Files → Data Cleaning (Z-Score) → MongoDB → Flask API → Streamlit Dashboard
```

## Features

### Part 1: Data Cleaning & Database (30 pts)

- ✅ Load multiple CSV files with 60+ sensor fields (temperature, salinity, ODO, GPS, depth, etc.)
- ✅ Clean data using z-score method (|z| > 3.0 threshold)
- ✅ Report cleaning statistics (original rows, removed outliers, final count)
- ✅ Store cleaned data in MongoDB (`water_quality_data` database, `all` collection)
- ✅ Index date field for query performance
- ✅ Generate cleaned CSV files organized by collection date

### Part 2: Flask REST API (40 pts)

- ✅ **GET `/api/health`** - Health check endpoint
- ✅ **GET `/api/observations`** - Retrieve observations with filtering:
  - Query parameters: `start`, `end` (ISO timestamps)
  - Filter ranges: `min_temp`, `max_temp`, `min_sal`, `max_sal`, `min_odo`, `max_odo`
  - Pagination: `limit` (default 100, max 1000), `skip`
  - Returns: `{"count": int, "items": [...]}`
- ✅ **GET `/api/stats`** - Summary statistics for all numeric fields
  - Returns: count, mean, std, min, max, 25%, 50%, 75% percentiles
- ✅ **GET `/api/outliers`** - On-demand outlier detection
  - Parameters: `field`, `method` (iqr/zscore), `k` (IQR multiplier), `z` (z-score threshold)
  - Returns: flagged records with metadata

### Part 3: Streamlit Client (30 pts)

- ✅ **Controls Panel (Sidebar)**:

  - Date range picker (start/end)
  - Min/max filters for temperature, salinity, ODO
  - Pagination controls (limit, skip)

- ✅ **Data Table**: Display filtered observations from `/api/observations`

- ✅ **Visualizations** (4 Plotly charts):

  1. **Histogram**: Salinity distribution
  2. **Scatter Plot**: Temperature vs Salinity (colored by ODO levels)
  3. **Interactive Map**: Geographic path with hover data (lat/lon + sensor readings)
  4. _(Line chart over time can be added)_

- ✅ **Statistics Panel**: Display summary stats from `/api/stats`

- ✅ **Outliers View**: Interactive outlier detection
  - Select any numerical field (60+ options)
  - Choose method (IQR or Z-score)
  - Adjust detection parameters
  - View flagged records in data table

## Project Structure

```
CIS3590_Project/
├── data/
│   ├── datasets/                 # Raw CSV files
│   │   ├── 2021-oct21.csv
│   │   ├── 2021-dec16.csv
│   │   ├── 2022-oct7.csv
│   │   └── 2022-nov16.csv
│   ├── cleaned datasets/         # Cleaned data output
│   │   ├── consolidated.json     # All cleaned data
│   │   ├── 2021-oct21.csv       # Cleaned CSVs by date
│   │   ├── 2021-dec16.csv
│   │   ├── 2022-oct7.csv
│   │   └── 2022-nov16.csv
│   ├── lib/
│   │   └── mongodb.py           # MongoDB connection utilities
│   └── dataAnalysis.py          # ETL pipeline script
│
├── api/
│   ├── helpers/
│   │   ├── filters.py           # Query filtering logic
│   │   ├── outlierMethods.py    # IQR and Z-score methods
│   │   └── utils.py             # API utilities
│   └── waterQualityDataApi.py   # Flask API server
│
├── client/
│   ├── helpers/
│   │   ├── charts.py            # Plotly visualization functions
│   │   ├── datas.py             # API client functions
│   │   ├── filters.py           # Sidebar filter controls
│   │   ├── headers.py           # Dashboard header
│   │   ├── observations.py      # Observations table display
│   │   ├── outliers.py          # Outlier detection interface
│   │   ├── statistics.py        # Statistics panel
│   │   └── utils.py             # Client constants
│   └── waterQualityDataDashboard.py  # Streamlit app
│
├── requirements.txt             # Python dependencies
├── instructions.md              # Project requirements
└── README.md                    # This file
```

## Technology Stack

| Package   | Version | Purpose                          |
| --------- | ------- | -------------------------------- |
| Flask     | 3.1.2   | REST API framework               |
| requests  | 2.32.5  | HTTP client for API calls        |
| pandas    | 2.3.x   | Data manipulation and cleaning   |
| pymongo   | 4.x     | MongoDB driver                   |
| mongomock | 4.x     | In-memory MongoDB for testing    |
| streamlit | 1.50.0  | Interactive dashboard framework  |
| plotly    | 6.0.0+  | Interactive data visualizations  |
| scipy     | Latest  | Statistical functions (z-scores) |

## Setup Instructions

### Prerequisites

- Python 3.10+
- MongoDB (optional - can use mongomock)

### Installation

1. **Clone the repository and cd into the root folder**

   ```bash
   git clone https://github.com/dessources/CIS3590_Project.git
   cd CIS3590_Project
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure MongoDB** (optional)

   Edit `data/lib/mongodb.py` to switch between MongoDB and mongomock:

   ```python
   # For local MongoDB:
   client = MongoClient("mongodb://localhost:27017/")

   # For in-memory testing:
   client = mongomock.MongoClient()

   #For a cloud instance of MongoDB, create a MongoDB account, obtain the following values and place them in a .env file in the root directory:
   MONGO_USER="DB_username"
   MONGO_PASSWORD="DB_password"
   MONGO_CLUSTER_URL="cluster url"

   ```

### Running the Project

#### Step 1: Data Cleaning & Database Loading

Run the ETL pipeline to clean data and load into MongoDB:

```bash
cd data
python dataAnalysis.py
```

**Output:**

- Displays cleaning statistics (rows removed, outliers count)
- Saves `cleaned datasets/consolidated.json`
- Generates cleaned CSVs by date
- Loads data into MongoDB (`water_quality_data.all` collection)

#### Step 2: Start the Flask API

```bash
cd api
python waterQualityDataApi.py
```

The API will run on `http://localhost:5050`

**Test the API:**

```bash
# Health check
curl http://localhost:5050/api/health

# Get observations
curl "http://localhost:5050/api/observations?limit=10"

# Get statistics
curl http://localhost:5050/api/stats

# Detect outliers
curl "http://localhost:5050/api/outliers?field=Temperature%20(c)&method=zscore&z=3"
```

#### Step 3: Launch the Streamlit Dashboard

```bash
cd client
python -m streamlit run waterQualityDataDashboard.py
```

The dashboard will open at `http://localhost:8501`

## API Documentation

### Base URL

`http://localhost:5050`

### Endpoints

#### 1. Health Check

```http
GET /api/health
```

**Response:**

```json
{
  "status": "ok"
}
```

---

#### 2. Get Observations

```http
GET /api/observations
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start` | ISO datetime | - | Filter records after this timestamp |
| `end` | ISO datetime | - | Filter records before this timestamp |
| `min_temp` | float | - | Minimum temperature (°C) |
| `max_temp` | float | - | Maximum temperature (°C) |
| `min_sal` | float | - | Minimum salinity (ppt) |
| `max_sal` | float | - | Maximum salinity (ppt) |
| `min_odo` | float | - | Minimum dissolved oxygen (mg/L) |
| `max_odo` | float | - | Maximum dissolved oxygen (mg/L) |
| `limit` | int | 100 | Results per page (max 1000) |
| `skip` | int | 0 | Number of records to skip |

**Example Request:**

```bash
curl "http://localhost:5050/api/observations?min_temp=25&max_temp=30&limit=50"
```

**Response:**

```json
{
  "count": 503,
  "items": [
    {
      "Date": "10/7/22",
      "Time": "11:02:04",
      "Latitude": 25.91273,
      "Longitude": -80.13782,
      "Temperature (c)": 27.87,
      "Salinity (ppt)": 40.6,
      "ODO mg/L": 3.03,
      ...
    }
  ]
}
```

---

#### 3. Get Statistics

```http
GET /api/stats
```

**Response:**

```json
{
  "Latitude": {
    "count": 3003,
    "mean": 25.9127,
    "std": 0.00045,
    "min": 25.9120,
    "25%": 25.9125,
    "50%": 25.9127,
    "75%": 25.9130,
    "max": 25.9135
  },
  "Temperature (c)": {
    "count": 3003,
    "mean": 27.2,
    ...
  },
  ...
}
```

---

#### 4. Detect Outliers

```http
GET /api/outliers
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `field` | string | - | Column name to analyze |
| `method` | string | `iqr` | Detection method: `iqr` or `zscore` |
| `k` | float | 1.5 | IQR multiplier (only for IQR method) |
| `z` | float | 3.0 | Z-score threshold (only for zscore method) |

**Example Request:**

```bash
curl "http://localhost:5050/api/outliers?field=Temperature%20(c)&method=zscore&z=3"
```

**Response:**

```json
{
  "field": "Temperature (c)",
  "method": "zscore",
  "z": 3.0,
  "k": null,
  "count": 12,
  "outliers": [
    {
      "Date": "10/7/22",
      "Temperature (c)": 35.2,
      ...
    }
  ]
}
```

## Data Cleaning Process

### Z-Score Method

1. **Load Data**: Read all CSV files and merge into single DataFrame
2. **Calculate Z-Scores**: For each numerical column:
   ```
   z-score = (value - mean) / standard_deviation
   ```
3. **Identify Outliers**: Flag rows where any field has `|z-score| > 3.0`
4. **Remove Outliers**: Drop flagged rows from dataset
5. **Report Results**: Display cleaning statistics
6. **Save & Load**:
   - Export cleaned data as JSON and individual CSVs
   - Insert into MongoDB for API access

## Dashboard Features

### Filter Controls

- **Date Range**: Select start and end dates for time-series filtering
- **Temperature Range**: Min/max temperature sliders
- **Salinity Range**: Min/max salinity inputs
- **ODO Range**: Min/max dissolved oxygen filters
- **Pagination**: Control results per page and skip offset

### Visualizations

1. **Salinity Histogram**

   - Distribution of salinity measurements
   - 40 bins for detailed distribution analysis

2. **Temperature vs Salinity Scatter**

   - Bivariate relationship analysis
   - Color-coded by dissolved oxygen levels
   - Interactive hover data

3. **Geographic Map**

   - ASV path visualization with lat/lon coordinates
   - Auto-zoom to fit data extent
   - Hover tooltips show all sensor readings
   - Color-coded by temperature
   - 900px height for detailed view

4. **Statistics Dashboard**

   - Summary statistics for all 60+ numeric fields
   - Interactive DataFrame display

5. **Outlier Detection Tool**
   - Select from all numerical columns
   - Choose IQR or Z-score method
   - Adjust detection sensitivity
   - View flagged records in table

## Error Handling

The client gracefully handles API connection errors:

```python
# If API server is down:
⚠️ Unable to connect to the API server.
Please ensure the server is running.
```

All display functions include try-except blocks to catch `ConnectionError` and show user-friendly messages.

## Development Notes

### Code Organization

- **Modular Design**: Separate helpers for data fetching, filtering, visualization
- **DRY Principles**: Reusable functions for API calls and display logic
- **Constants**: Centralized configuration in `utils.py` files
- **Error Handling**: Connection error handling at display layer

### API Design Decisions

1. **Filtering**: Applied server-side for performance
2. **Pagination**: Default 100 items, max 1000 to prevent overload
3. **Datetime Handling**: Combined Date/Time fields into single datetime column
4. **Response Format**: Consistent `{"count", "items"}` structure

### Performance Optimizations

- MongoDB indexing on Date field
- Server-side filtering reduces data transfer
- Streamlit session state caching for visualizations
- Efficient pandas operations for statistics

## Learning Outcomes

Through this project, I gained experience with:

1. **ETL Pipeline Development**

   - Reading and merging multiple CSV files
   - Statistical outlier detection using z-scores
   - Data transformation and cleaning workflows
   - NoSQL database operations (MongoDB)

2. **REST API Design**

   - Flask route handlers and request parameter parsing
   - JSON response formatting
   - Query filtering and pagination
   - Error handling and status codes

3. **Client-Server Architecture**

   - HTTP request/response cycle
   - API client implementation
   - Connection error handling
   - State management in web apps

4. **Data Visualization**
   - Interactive Plotly charts (histograms, scatter plots, maps)
   - Dashboard layout with Streamlit
   - User controls and form inputs
   - Real-time data updates

## Future Enhancements

In the future these enhancements could be made:

- [ ] User authentication for API endpoints
- [ ] Deployment to cloud platform (AWS/Azure/Heroku)
