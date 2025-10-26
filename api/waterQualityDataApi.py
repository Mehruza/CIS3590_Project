import os
from flask import Flask, jsonify, request
import json
import pandas as pd
from helpers.getData import *
from helpers.outlierMethods import *
from helpers.filters import *

app = Flask(__name__)
data = get_data()
df = pd.DataFrame(data)


@app.route("/")
def index():
    return jsonify({
        "routes": {
            "/api/health": "API status check",
            "/api/observations": "return documents with optional query parameters",
            "/api/statistics": "return summary stats",
            "/api/outlier": "Find outliers using z-score"
        }
    })


@app.route("/api/health", methods=["GET"])
def health():
    return {"status": "ok"}, 200


@app.route("/api/observations")
def observations():
    start = request.args.get('start')
    end = request.args.get('end')
    min_temp = request.args.get('min_temp', type=float)
    max_temp = request.args.get('max_temp', type=float)
    min_sal = request.args.get('min_sal', type=float)
    max_sal = request.args.get('max_sal', type=float)
    min_odo = request.args.get('min_odo', type=float)
    max_odo = request.args.get('max_odo', type=float)
    limit = request.args.get('limit', default=100, type=int)
    skip = request.args.get('skip', default=0, type=int)

    # Copy data frame so we can filter it at will
    filtered_df = df.copy()

    # Apply filters and get result
    result = apply_filters(
        filtered_df,
        start=start,
        end=end,
        min_temp=min_temp,
        max_temp=max_temp,
        min_sal=min_sal,
        max_sal=max_sal,
        min_odo=min_odo,
        max_odo=max_odo,
        limit=limit,
        skip=skip
    )

    return jsonify(result), 200


@app.route("/api/stats")
def stats():
    return jsonify(df.describe().to_dict()), 200


@app.route("/api/outliers")
def outliers():
    field = request.args.get('field', default="Temperature (c)")
    method = request.args.get("method", default='zscore')
    k = request.args.get("k", default=1.5, type=float)
    z = request.args.get("z", default=3, type=float)
    if field not in df.columns:
        return jsonify({"message": "Invalid field name provided"}), 400
    outliers = zScore(
        df, field, z) if method == "zscore" else iqr(df, field, k)
    return jsonify({
        "field": field,
        "method": method,
        "k": k if method == "iqr" else None,
        "z": z if method == "zscore" else None,
        "count": len(outliers),
        "outliers": outliers.to_dict(orient="records")
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5050)