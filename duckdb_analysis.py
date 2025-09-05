import duckdb
import os

# Connect to an in-memory DuckDB instance
conn = duckdb.connect()
# Load the transformed data into DuckDB tables

conn.execute("""
             CREATE TABLE IF NOT EXISTS fact_orders
             AS SELECT * FROM read_csv_auto('transformed_data/fact_orders.csv')
""")

conn.execute("""
             CREATE TABLE IF NOT EXISTS dim_customers
             AS SELECT * FROM read_csv_auto('transformed_data/dim_customers.csv')
""")
conn.execute("""
             CREATE TABLE IF NOT EXISTS dim_products
             AS SELECT * FROM read_csv_auto('transformed_data/dim_products.csv')
""")
conn.execute("""
             CREATE TABLE IF NOT EXISTS dim_date
             AS SELECT * FROM read_csv_auto('transformed_data/dim_date.csv')
""")

# Verify the data has been loaded correctly
def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Path to SQL query files
sql_folder = "sql"

# Loop through SQL files and read their content

for sql_file in os.listdir(sql_folder):
    if sql_file.endswith(".sql"):
        query_name = sql_file.replace(".sql", "").replace("_", " ").title()
        sql_path = os.path.join(sql_folder, sql_file)
        sql_query = read_sql_file(sql_path)
        
        print(f"\n{query_name}:\n")
        try:
            result = conn.execute(sql_query).fetchdf()
            print(result)
        except Exception as e:
            print(f"Error executing {sql_file}: {e}")

