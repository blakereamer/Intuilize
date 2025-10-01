import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

print('🚀 Starting Enhanced Feature Engineering Pipeline')
print('='*60)

# Load data
print('📂 Loading datasets...')
try:
    sales_df = pd.read_csv('Intuilize Data/Intuilize_MNSU_ACME_SalesData.csv')
    quotes_df = pd.read_csv('Intuilize Data/Intuilize_MNSU_ACME_QuotesData.csv', low_memory=False)
    inventory_df = pd.read_csv('Intuilize Data/Intuilize_MNSU_ACME_InventoryData.csv')
    print(f'✅ Sales: {sales_df.shape}, Quotes: {quotes_df.shape}, Inventory: {inventory_df.shape}')
except Exception as e:
    print(f'❌ Error loading data: {e}')
    exit()

# Preprocess dates
print('🕒 Preprocessing dates...')
sales_df['SalesDate'] = pd.to_datetime(sales_df['SalesDate'])
if 'QuoteDate' in quotes_df.columns:
    quotes_df['QuoteDate'] = pd.to_datetime(quotes_df['QuoteDate'])
if 'ExpirationDate' in quotes_df.columns:
    quotes_df['ExpirationDate'] = pd.to_datetime(quotes_df['ExpirationDate'])
if 'ConversionDate' in quotes_df.columns:
    quotes_df['ConversionDate'] = pd.to_datetime(quotes_df['ConversionDate'])

print('📊 Dataset Analysis:')
print(f'   Unique Customers: {sales_df["CustomerID"].nunique():,}')
print(f'   Unique Products: {sales_df["ProductID"].nunique():,}')
print(f'   Date Range: {sales_df["SalesDate"].min()} to {sales_df["SalesDate"].max()}')

# =============================================================================
# ENHANCED CUSTOMER FEATURES - LARGER SAMPLE SIZE
# =============================================================================
print('🧑‍💼 Creating enhanced customer features...')

# Calculate optimal customer sample size (minimum 50,000 or 15% of customers)
total_customers = sales_df['CustomerID'].nunique()
min_sample_size = 50000
sample_percentage = 0.15  # 15% of customers
customer_sample_size = max(min_sample_size, int(total_customers * sample_percentage))
customer_sample_size = min(customer_sample_size, total_customers)

print(f'   📊 Total customers: {total_customers:,}')
print(f'   🎯 Using {customer_sample_size:,} customers ({customer_sample_size/total_customers*100:.1f}% of total)')

# Stratified sampling by customer value to ensure representative sample
customer_sales_value = sales_df.groupby('CustomerID')['ExtPrice'].sum().sort_values(ascending=False)

# Create value tiers for representative sampling
# Use all customers but maintain proportional distribution  
customer_sample_size = total_customers  # Use all available customers
high_value_size = max(1, int(customer_sample_size * 0.20))  # Top 20%
mid_value_size = max(1, int(customer_sample_size * 0.60))   # Middle 60%
low_value_size = customer_sample_size - high_value_size - mid_value_size  # Remaining 20%

# Ensure we don't exceed available customers in each tier
high_value_pool_size = int(len(customer_sales_value) * 0.20)
mid_value_pool_size = int(len(customer_sales_value) * 0.60)
low_value_pool_size = len(customer_sales_value) - high_value_pool_size - mid_value_pool_size

high_value_customers = customer_sales_value.head(min(high_value_size, high_value_pool_size)).index
mid_start = high_value_pool_size
mid_end = high_value_pool_size + mid_value_pool_size
mid_value_customers = customer_sales_value.iloc[mid_start:mid_end].sample(n=min(mid_value_size, mid_value_pool_size), random_state=42).index
low_value_customers = customer_sales_value.tail(min(low_value_size, low_value_pool_size)).sample(n=min(low_value_size, low_value_pool_size), random_state=42).index

selected_customers = pd.Index(high_value_customers).union(mid_value_customers).union(low_value_customers)
print(f'   💰 High-value: {len(high_value_customers):,}, Mid-value: {len(mid_value_customers):,}, Low-value: {len(low_value_customers):,}')

# Filter data for selected customers
customer_sales_data = sales_df[sales_df['CustomerID'].isin(selected_customers)]

# Enhanced customer sales aggregation
customer_sales = customer_sales_data.groupby('CustomerID').agg({
    'ExtPrice': ['sum', 'mean', 'std', 'count', 'median', 'min', 'max'],
    'ExtCost': ['sum', 'mean', 'std', 'median'],
    'SalesQty': ['sum', 'mean', 'std', 'median', 'min', 'max'],
    'UnitPrice': ['mean', 'std', 'min', 'max', 'median'],
    'UnitCost': ['mean', 'std', 'median'],
    'OrderNumber': 'nunique',
    'ProductID': 'nunique',
    'SalesDate': ['min', 'max', 'count']
}).round(4)

customer_sales.columns = ['_'.join(col).strip() for col in customer_sales.columns]
customer_sales = customer_sales.reset_index()

# Calculate enhanced customer metrics
print('   🔢 Computing advanced customer metrics...')
customer_sales['TotalRevenue'] = customer_sales['ExtPrice_sum']
customer_sales['TotalCost'] = customer_sales['ExtCost_sum']
customer_sales['TotalProfit'] = customer_sales['TotalRevenue'] - customer_sales['TotalCost']
customer_sales['ProfitMargin'] = customer_sales['TotalProfit'] / customer_sales['TotalRevenue']
customer_sales['AvgOrderValue'] = customer_sales['ExtPrice_sum'] / customer_sales['OrderNumber_nunique']
customer_sales['AvgOrderQuantity'] = customer_sales['SalesQty_sum'] / customer_sales['OrderNumber_nunique']
customer_sales['PriceVolatility'] = customer_sales['UnitPrice_std'] / customer_sales['UnitPrice_mean']
customer_sales['QuantityVolatility'] = customer_sales['SalesQty_std'] / customer_sales['SalesQty_mean']
customer_sales['CustomerLifetimeDays'] = (customer_sales['SalesDate_max'] - customer_sales['SalesDate_min']).dt.days
customer_sales['AvgDaysBetweenOrders'] = customer_sales['CustomerLifetimeDays'] / customer_sales['OrderNumber_nunique']
customer_sales['OrderFrequency'] = customer_sales['OrderNumber_nunique'] / (customer_sales['CustomerLifetimeDays'] + 1) * 365
customer_sales['ProductDiversity'] = customer_sales['ProductID_nunique']
customer_sales['AvgProductsPerOrder'] = customer_sales['ProductID_nunique'] / customer_sales['OrderNumber_nunique']

# RFM Analysis
print('   📈 Performing RFM Analysis...')
reference_date = customer_sales_data['SalesDate'].max()
customer_sales['Recency'] = (reference_date - customer_sales['SalesDate_max']).dt.days
customer_sales['Frequency'] = customer_sales['OrderNumber_nunique']
customer_sales['Monetary'] = customer_sales['TotalRevenue']

# RFM Scoring (1-5 scale)
customer_sales['RecencyScore'] = pd.qcut(customer_sales['Recency'], q=5, labels=[5,4,3,2,1], duplicates='drop')
customer_sales['FrequencyScore'] = pd.qcut(customer_sales['Frequency'].rank(method='first'), q=5, labels=[1,2,3,4,5], duplicates='drop')
customer_sales['MonetaryScore'] = pd.qcut(customer_sales['Monetary'], q=5, labels=[1,2,3,4,5], duplicates='drop')
customer_sales['RFMScore'] = customer_sales['RecencyScore'].astype(str) + customer_sales['FrequencyScore'].astype(str) + customer_sales['MonetaryScore'].astype(str)

# Customer Loyalty and Value Metrics
customer_sales['CustomerLifetimeValue'] = customer_sales['TotalRevenue']
customer_sales['CustomerLoyaltyScore'] = customer_sales['Frequency'] * customer_sales['Monetary'] / (customer_sales['Recency'] + 1)

# Customer metrics from quotes data (filtered for selected customers)
customer_quotes_data = quotes_df[quotes_df['CustomerID'].isin(selected_customers)]
if not customer_quotes_data.empty and 'QuoteID' in quotes_df.columns:
    print('   💭 Processing quotes data for selected customers...')
    customer_quotes = customer_quotes_data.groupby('CustomerID').agg({
        'QuoteID': 'nunique',
        'QuoteVersion': ['mean', 'max'],
        'UnitPrice': ['mean', 'std', 'min', 'max'],
        'QuoteQty': ['sum', 'mean', 'std'],
        'QuoteStatus': lambda x: (x == 'Won').sum() / len(x) if len(x) > 0 else 0,
        'ConvertedToOrderNumber': lambda x: x.notna().sum()
    }).round(4)

    customer_quotes.columns = ['_'.join(col).strip() for col in customer_quotes.columns]
    customer_quotes = customer_quotes.reset_index()

    # Calculate quote-specific metrics
    customer_quotes['QuoteConversionRate'] = customer_quotes['ConvertedToOrderNumber_<lambda>'] / customer_quotes['QuoteID_nunique']
    customer_quotes['QuoteWinRate'] = customer_quotes['QuoteStatus_<lambda>']
    customer_quotes['AvgNegotiationRounds'] = customer_quotes['QuoteVersion_mean']
    customer_quotes['QuotePriceVolatility'] = customer_quotes['UnitPrice_std'] / customer_quotes['UnitPrice_mean']

    # Merge customer features with quotes
    customer_features = pd.merge(customer_sales, customer_quotes, on='CustomerID', how='left')
else:
    print('   ⚠️  No quotes data available for selected customers')
    customer_features = customer_sales

# Handle categorical columns before fillna
for col in customer_features.columns:
    if customer_features[col].dtype.name == 'category':
        customer_features[col] = customer_features[col].astype(str)

# Fill missing values
customer_features = customer_features.fillna(0)

# Fix RFM Score missing values specifically
if 'RFMScore' in customer_features.columns:
    customer_features['RFMScore'] = customer_features['RFMScore'].replace('0', '000')

print(f'✅ Enhanced customer features created: {customer_features.shape}')

# =============================================================================
# ENHANCED PRODUCT FEATURES
# =============================================================================
print('📦 Creating enhanced product features...')

product_sales = sales_df.groupby('ProductID').agg({
    'ExtPrice': ['sum', 'mean', 'std', 'count', 'median', 'min', 'max'],
    'ExtCost': ['sum', 'mean', 'std', 'median'],
    'SalesQty': ['sum', 'mean', 'std', 'median', 'min', 'max'],
    'UnitPrice': ['mean', 'std', 'min', 'max', 'median'],
    'UnitCost': ['mean', 'std', 'median'],
    'OrderNumber': 'nunique',
    'CustomerID': 'nunique',
    'SalesDate': ['min', 'max', 'count']
}).round(4)

product_sales.columns = ['_'.join(col).strip() for col in product_sales.columns]
product_sales = product_sales.reset_index()

# Calculate enhanced product metrics
print('   🔢 Computing advanced product metrics...')
product_sales['TotalRevenue'] = product_sales['ExtPrice_sum']
product_sales['TotalCost'] = product_sales['ExtCost_sum']
product_sales['TotalProfit'] = product_sales['TotalRevenue'] - product_sales['TotalCost']
product_sales['ProfitMargin'] = product_sales['TotalProfit'] / product_sales['TotalRevenue']
product_sales['AvgOrderValue'] = product_sales['ExtPrice_sum'] / product_sales['OrderNumber_nunique']
product_sales['AvgOrderQuantity'] = product_sales['SalesQty_sum'] / product_sales['OrderNumber_nunique']
product_sales['PriceVolatility'] = product_sales['UnitPrice_std'] / product_sales['UnitPrice_mean']
product_sales['QuantityVolatility'] = product_sales['SalesQty_std'] / product_sales['SalesQty_mean']
product_sales['ProductLifetimeDays'] = (product_sales['SalesDate_max'] - product_sales['SalesDate_min']).dt.days
product_sales['AvgDaysBetweenOrders'] = product_sales['ProductLifetimeDays'] / product_sales['OrderNumber_nunique']
product_sales['SalesFrequency'] = product_sales['OrderNumber_nunique'] / (product_sales['ProductLifetimeDays'] + 1) * 365
product_sales['CustomerBase'] = product_sales['CustomerID_nunique']
product_sales['CustomerPenetration'] = product_sales['CustomerID_nunique'] / sales_df['CustomerID'].nunique()

# Product performance metrics
product_sales['RevenuePerCustomer'] = product_sales['TotalRevenue'] / product_sales['CustomerBase']
product_sales['UnitsPerCustomer'] = product_sales['SalesQty_sum'] / product_sales['CustomerBase']
product_sales['OrdersPerCustomer'] = product_sales['OrderNumber_nunique'] / product_sales['CustomerBase']

# Product quotes features
if not quotes_df.empty and 'ProductID' in quotes_df.columns:
    print('   💭 Processing quotes data for products...')
    product_quotes = quotes_df.groupby('ProductID').agg({
        'QuoteID': 'nunique',
        'QuoteVersion': ['mean', 'max'],
        'UnitPrice': ['mean', 'std', 'min', 'max'],
        'QuoteQty': ['sum', 'mean', 'std'],
        'QuoteStatus': lambda x: (x == 'Won').sum() / len(x) if len(x) > 0 else 0,
        'ConvertedToOrderNumber': lambda x: x.notna().sum()
    }).round(4)

    product_quotes.columns = ['_'.join(col).strip() for col in product_quotes.columns]
    product_quotes = product_quotes.reset_index()

    # Product quote metrics
    product_quotes['QuoteConversionRate'] = product_quotes['ConvertedToOrderNumber_<lambda>'] / product_quotes['QuoteID_nunique']
    product_quotes['QuoteWinRate'] = product_quotes['QuoteStatus_<lambda>']
    product_quotes['AvgQuoteNegotiations'] = product_quotes['QuoteVersion_mean']

    # Merge product features
    product_features = pd.merge(product_sales, product_quotes, on='ProductID', how='left')
else:
    product_features = product_sales

product_features = product_features.fillna(0)
print(f'✅ Enhanced product features created: {product_features.shape}')

# =============================================================================
# ENHANCED MERGED ELASTICITY DATASET
# =============================================================================
print('🔗 Creating enhanced merged elasticity dataset...')

# Enhanced merge strategy with key features only to avoid data explosion
key_customer_features = ['CustomerID', 'TotalRevenue', 'TotalProfit', 'ProfitMargin', 'AvgOrderValue', 
                        'CustomerLifetimeValue', 'CustomerLoyaltyScore', 'RFMScore', 'Recency', 'Frequency', 'Monetary']
key_product_features = ['ProductID', 'TotalRevenue', 'TotalProfit', 'ProfitMargin', 'CustomerBase', 
                       'CustomerPenetration', 'RevenuePerCustomer', 'SalesFrequency']

# Filter features that exist in the dataframes
available_customer_features = [col for col in key_customer_features if col in customer_features.columns]
available_product_features = [col for col in key_product_features if col in product_features.columns]

merged_data = pd.merge(sales_df, customer_features[available_customer_features], 
                      on='CustomerID', how='left', suffixes=('', '_cust'))

merged_data = pd.merge(merged_data, product_features[available_product_features], 
                      on='ProductID', how='left', suffixes=('', '_prod'))

# Additional elasticity-specific features
print('   ⚡ Adding elasticity-specific features...')
merged_data['PriceElasticityProxy'] = merged_data['SalesQty'] / (merged_data['UnitPrice'] + 1)
if 'CustomerLoyaltyScore' in merged_data.columns:
    merged_data['CustomerLoyaltyScore'] = merged_data['CustomerLoyaltyScore'].fillna(0)
if 'CustomerBase' in merged_data.columns:
    merged_data['ProductDemandStrength'] = merged_data['SalesQty'] * merged_data['CustomerBase']
if 'TotalRevenue_prod' in merged_data.columns:
    merged_data['MarketShare'] = merged_data['TotalRevenue_prod'] / merged_data['TotalRevenue_prod'].sum()
if 'AvgOrderValue_prod' in merged_data.columns:
    merged_data['RelativePricePosition'] = merged_data['UnitPrice'] / merged_data['AvgOrderValue_prod']

merged_data = merged_data.fillna(0)
print(f'✅ Enhanced merged elasticity dataset created: {merged_data.shape}')

# =============================================================================
# SAVE ENHANCED DATASETS
# =============================================================================
print('💾 Saving enhanced datasets...')

# Save with enhanced features and larger customer sample
customer_features.to_csv('customer_features_enhanced.csv', index=False)
product_features.to_csv('product_features_enhanced.csv', index=False)
merged_data.to_csv('merged_elasticity_dataset_enhanced.csv', index=False)

print('✅ Enhanced datasets saved successfully!')
print(f'   📊 Customer Features: {customer_features.shape[0]:,} customers × {customer_features.shape[1]} features')
print(f'   📦 Product Features: {product_features.shape[0]:,} products × {product_features.shape[1]} features')
print(f'   🔗 Merged Dataset: {merged_data.shape[0]:,} transactions × {merged_data.shape[1]} features')

# Summary statistics
print('\n📈 Enhanced Dataset Summary:')
print(f'   Total Revenue Represented: ${customer_features["TotalRevenue"].sum():,.2f}')
print(f'   Average Customer Value: ${customer_features["TotalRevenue"].mean():,.2f}')
print(f'   Customer Value Range: ${customer_features["TotalRevenue"].min():,.2f} - ${customer_features["TotalRevenue"].max():,.2f}')
print(f'   Most Profitable Product Revenue: ${product_features["TotalRevenue"].max():,.2f}')

print('\n🎯 Next Steps:')
print('   1. Review the comprehensive data dictionaries')
print('   2. Analyze feature distributions and correlations')
print('   3. Begin elasticity modeling with the enhanced datasets')
print('   4. Validate model performance on holdout data')
print('   5. Use RFM scores for customer segmentation analysis')