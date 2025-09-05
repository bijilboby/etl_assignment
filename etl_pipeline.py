import pandas as pd
import os

df_customers = pd.read_csv("raw_data/customers_raw.csv")
df_orders = pd.read_csv("raw_data/orders_raw.csv")
df_products = pd.read_csv("raw_data/products_raw.csv")

#remove duplicates if any exists
df_customers.drop_duplicates(inplace=True)
df_products.drop_duplicates(inplace=True)
df_orders.drop_duplicates(inplace=True)

#drop null values if any in the
df_customers.dropna(inplace=True)
df_orders.dropna(inplace=True)
df_products.dropna(inplace=True)

# Standardize text: lowercase category, strip emails
df_products['category'] = df_products['category'].str.strip().str.lower()
df_customers['email'] = df_customers['email'].str.strip().str.lower()

#creating a date dataframe
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'])

df_date = df_orders[['order_date']].drop_duplicates().copy()
df_date['date_id'] = df_date['order_date'].dt.strftime('%Y%m%d').astype(int)
df_date['year'] = df_date['order_date'].dt.year
df_date['month'] = df_date['order_date'].dt.month
df_date['day'] = df_date['order_date'].dt.day
df_date['weekday'] = df_date['order_date'].dt.day_name()

#merge price to order table on by product_id and compute total amount
df_orders = df_orders.merge(df_products[['product_id','price']], on = 'product_id')
df_orders['total_amount'] = df_orders['price']*df_orders['quantity']

#merge date_id into order table
df_orders = df_orders.merge(df_date[['order_date','date_id']], on = 'order_date')

#create final output tables
fact_orders = df_orders[['order_id','product_id','customer_id','date_id','quantity','total_amount']]
dim_products = df_products.copy()
dim_customers = df_customers.copy()
dim_date = df_date.copy()

# Load data to CSV files

os.makedirs("transformed_data", exist_ok=True)

dim_customers.to_csv("transformed_data/dim_customers.csv", index=False)
dim_products.to_csv("transformed_data/dim_products.csv", index=False)
dim_date.to_csv("transformed_data/dim_date.csv", index=False)
fact_orders.to_csv("transformed_data/fact_orders.csv", index=False)

print("ETL process completed successfully. Transformed data saved in 'transformed_data' directory.")
