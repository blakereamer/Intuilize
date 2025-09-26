#!/usr/bin/env python
# coding: utf-8

# This file finds the selected features for the monthly prediction approach

# In[4]:


import os
import pandas as pd
import numpy as np

def process_file(file_path, output_dir, global_customers):
    # Read the monthly CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert SalesDate to datetime
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])
    
    # --------------------
    # Step 1: Product-Level Aggregations
    product_metrics = df.groupby('ProductID').agg(
        TotalSalesPrice=('ExtPrice', 'sum'),
        TotalCost=('ExtCost', 'sum'),
        TotalProfit=('Profit', 'sum'),
        AvgUnitPrice=('UnitPrice', 'mean'),
        AvgUnitCost=('UnitCost', 'mean'),
        TotalSalesQty=('SalesQty', 'sum'),
        TotalOrders=('OrderNumber', 'nunique'),
        UniqueCustomers=('CustomerName', 'nunique'),
        PriceVolatility=('UnitPrice', 'std')
    ).reset_index()
    
    # Step 2: Compute Additional Metrics at Product Level
    product_metrics['ProfitMargin'] = product_metrics['TotalProfit'] / product_metrics['TotalSalesPrice']
    product_metrics['AvgOrderSize'] = product_metrics['TotalSalesQty'] / product_metrics['TotalOrders']
    product_metrics['RepeatPurchaseRatio'] = product_metrics['TotalOrders'] / product_metrics['UniqueCustomers']
    
    # Step 3: Identify Customers Who Bought Each Product
    product_customers = df.groupby('ProductID')['CustomerName'].unique().reset_index()
    product_customers['CustomerCount'] = product_customers['CustomerName'].apply(len)
    
    # Merge product metrics with customer count
    product_metrics = product_metrics.merge(product_customers[['ProductID', 'CustomerCount']], on='ProductID', how='left')
    
    # --------------------
    # Step 4: Compute Customer Lifetime
    customer_lifetime = df.groupby("CustomerName").agg(
        FirstPurchase=("SalesDate", "min"),
        LastPurchase=("SalesDate", "max")
    ).reset_index()
    customer_lifetime["CustomerLifetimeDays"] = (customer_lifetime["LastPurchase"] - customer_lifetime["FirstPurchase"]).dt.days
    
    # --------------------
    # Step 5: Compute Customer-Level Aggregations
    customer_metrics = df.groupby("CustomerName").agg(
        TotalRevenue=("ExtPrice", "sum"),
        TotalProfit=("Profit", "sum"),
        TotalUnitPrice=("UnitPrice", "sum"),
        TotalSalesQty=("SalesQty", "sum"),
        OrderCount=("OrderNumber", "nunique"),
        NumDistinctProducts=("ProductID", "nunique"),
        NumDistinctProductGroups=("ProductGroupID", "nunique"),
        BranchCount=("BranchName", "nunique"),
        TopProductID=("ProductID", lambda x: x.value_counts().idxmax()),
        TopProductGroupID=("ProductGroupID", lambda x: x.value_counts().idxmax()),
        ProductDiversityIndex=("ProductID", lambda x: len(x.unique()) / x.count()),
        ProductConcentrationIndex=("ExtPrice", lambda x: x.max() / x.sum()),
        TopProductRevenueShare=("ExtPrice", lambda x: x.groupby(df["ProductID"]).sum().max() / x.sum()),
        TopProductGroupRevenueShare=("ExtPrice", lambda x: x.groupby(df["ProductGroupID"]).sum().max() / x.sum())
    ).reset_index()
    
    # Merge customer lifetime data
    customer_metrics = customer_metrics.merge(customer_lifetime[["CustomerName", "CustomerLifetimeDays"]], on="CustomerName", how="left")
    
    # --------------------
    # Step 6: Compute Additional Customer Features
    customer_metrics['AvgOrderValue'] = customer_metrics['TotalRevenue'] / customer_metrics['OrderCount']
    customer_metrics['RepeatPurchaseRatio'] = customer_metrics['OrderCount'] / customer_metrics['NumDistinctProducts']
    
    # --------------------
    # Step 7: Merge Product-Level Profitability Metrics into Transactions DataFrame
    product_profit = product_metrics[['ProductID', 'TotalProfit']]
    df = df.merge(product_profit, on='ProductID', how='left')
    
    # --------------------
    # Step 8: Identify High-Profit and Popular Products
    high_profit_threshold = product_metrics['TotalProfit'].quantile(0.75)  # Top 25% profitable
    popular_product_threshold = product_metrics['TotalSalesQty'].quantile(0.75)  # Top 25% sold
    
    df['HighProfitProduct'] = df['Profit'] >= high_profit_threshold
    df['PopularProduct'] = df['SalesQty'] >= popular_product_threshold
    
    # --------------------
    # Step 9: Compute Customer Engagement with High-Profit & Popular Products
    customer_product_engagement = df.groupby('CustomerName').agg(
        HighProfitProductShare=('HighProfitProduct', 'mean'),
        PopularProductShare=('PopularProduct', 'mean'),
        HighProfitOrderRatio=('HighProfitProduct', 'sum'),
        PopularOrderRatio=('PopularProduct', 'sum')
    ).reset_index()
    
    # Final merge: Combine customer metrics with engagement features
    customer_metrics = customer_metrics.merge(customer_product_engagement, on='CustomerName', how='left')
    
    # --------------------
    # New Step: Ensure Every Customer Appears
    # Merge with global_customers (master list for 2022/2023) so every customer is included.
    # Assume global_customers has at least the column "CustomerName".
    global_names = global_customers["CustomerName"].unique()

    # Reindex the monthly customer_metrics to include all global_names
    customer_metrics = customer_metrics.set_index("CustomerName").reindex(global_names).reset_index()

    # Fill missing numeric values with 0 for customers who had no purchases that month
    numeric_cols = customer_metrics.select_dtypes(include=[np.number]).columns
    customer_metrics[numeric_cols] = customer_metrics[numeric_cols].fillna(0)
    
    # Alphabetize the customer metrics by CustomerName (a-z)
    customer_metrics = customer_metrics.sort_values("CustomerName")

    #Remove Customers if they have over 3000000 in profit in global customers
    low_profit_customers = global_customers.loc[global_customers["TotalProfit"] < 3000000, "CustomerName"].unique()
    customer_metrics = customer_metrics[customer_metrics["CustomerName"].isin(low_profit_customers)]

    # --------------------
    # Export the customer metrics file
    input_filename = os.path.basename(file_path)
    output_filename = f"customer_metrics_{input_filename}"
    output_path = os.path.join(output_dir, output_filename)
    customer_metrics.to_csv(output_path, index=False)
    print(f"Processed {file_path} -> {output_path}")

def main():
    # Directory containing monthly data CSV files
    input_dir = "../data/cleaned/monthlydata"
    # Output directory for the customer metrics files
    output_dir = "../data/cleaned/monthlymetrics"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load global customers (master list of every customer across 2022/2023)
    global_customers_path = "../data/cleaned/customer_metrics.csv"
    global_customers = pd.read_csv(global_customers_path)
    
    # Process each CSV file in the input directory
    for file in os.listdir(input_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(input_dir, file)
            process_file(file_path, output_dir, global_customers)

if __name__ == "__main__":
    main()

