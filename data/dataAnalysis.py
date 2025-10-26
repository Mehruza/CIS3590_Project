import os
import numpy as np
import pandas as pd
from lib import mongodb as mongo


Z_SCORE_TRESHOLD = 3

# Reading the data
cwd = os.path.dirname(__file__)
datasets = [
    pd.read_csv(os.path.join(cwd, "datasets/2021-oct21.csv")),
    pd.read_csv(os.path.join(cwd, "datasets/2021-dec16.csv")),
    pd.read_csv(os.path.join(cwd, "datasets/2022-oct7.csv")),
    pd.read_csv(os.path.join(cwd, "datasets/2022-nov16.csv")),
]


# Inspect individual datasets before merging
for i, df in enumerate(datasets):
    print(f"Dataset {i+1}:")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Shape: {df.shape}")
    print()

# Merge all datasets vertically (stack rows)
merged_data = pd.concat(datasets, axis=0, ignore_index=True)



# Here any row with a value having a z-score with absolute alue greater than 3 will be removed

numerical_columns = merged_data.select_dtypes(include=['number']).columns
outlier_rows = []  # to store the position of the outlier rows
for column in numerical_columns:
    mean = merged_data[column].mean()
    std = merged_data[column].std()
    if std == 0:
        print(f"Skipping column '{column}' - std is 0 (all values identical)")
        continue
    
    for i, value in enumerate(merged_data[column]):
        if  np.isnan(value):
            continue
        elif abs((value - mean)/std) > Z_SCORE_TRESHOLD:
            outlier_rows.append(i)
cleaned_data = merged_data.drop(index=outlier_rows)

print("\n")
print("Original row count ", len(merged_data))
print("Total rows removed as outliers", len(outlier_rows))
print("Total rows remaining ", len(cleaned_data), "\n")

# Saving cleaned data
cleaned_data.to_json(os.path.join(cwd, "cleaned datasets",
                     "consolidated.json"), orient="records", indent=2)
exit(0)
# DB stuff
db_client = mongo.connect_to_db()
db = db_client["water_quality_data"]
asv_1 = db["all"]

data_as_dict = cleaned_data.to_dict(orient='records')
if asv_1.count_documents({}) <= 1:
    try:
        asv_1.insert_many(data_as_dict)
    except Exception as e:
        print(e)
        
#Checking data was correctly uploaded
print("Length of local data ", len(cleaned_data))
print("Length of uploaded data ", asv_1.count_documents({}))

#Creating index on Date field
asv_1.create_index("Date")
mongo.disconnect_from_db(db_client)
