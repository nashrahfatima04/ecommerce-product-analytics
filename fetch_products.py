import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Step 1: Fetch data from API
api_url = "https://dummyjson.com/products"

try:
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()

    data = response.json()
    products = data["products"]

    print("API data fetched successfully")

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
    raise

# Step 2: Convert API data into DataFrame
df = pd.DataFrame(products)

print("\nOriginal columns:")
print(df.columns.tolist())

# Step 3: Select required columns
required_columns = [
    "id",
    "title",
    "category",
    "price",
    "discountPercentage",
    "rating",
    "stock"
]

df = df[required_columns].copy()

# Step 4: Data quality checks
print("\nFirst 5 rows:")
print(df.head())

print("\nDataFrame information:")
df.info()

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

# Step 5: Clean the data
df = df.drop_duplicates()

df = df.dropna(
    subset=["id", "title", "category", "price", "stock"]
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["discountPercentage"] = pd.to_numeric(
    df["discountPercentage"], errors="coerce"
)
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["stock"] = pd.to_numeric(df["stock"], errors="coerce")

df = df.dropna(
    subset=["price", "discountPercentage", "rating", "stock"]
)

print("\nCleaned data:")
print(df.head())

print("\nCleaned row count:", len(df))

# Step 6: Connect to PostgreSQL securely
db_password = os.getenv("DB_PASSWORD")

if not db_password:
    raise ValueError(
        "DB_PASSWORD is not set. Set it before running the script."
    )

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=db_password,
    host="localhost",
    port=5432,
    database="ecommerce_data"
)

engine = create_engine(connection_url)

# Step 7: Load data into PostgreSQL
try:
    with engine.connect() as connection:
        print("\nDatabase connected successfully")

    df.to_sql(
        "product_table_name",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded into PostgreSQL successfully")

finally:
    engine.dispose()