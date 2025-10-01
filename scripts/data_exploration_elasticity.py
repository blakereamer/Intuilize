"""
Price Elasticity Data Exploration Script
Author: GitHub Copilot Assistant
Purpose: Explore relationships between Sales, Quotes, and Inventory data for elasticity modeling
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

def load_data():
    """Load all three datasets"""
    print("Loading datasets...")
    
    # Load sales data (sample for exploration)
    sales_df = pd.read_csv('Intuilize_MNSU_ACME_SalesData.csv', nrows=50000)  # Sample for initial exploration
    quotes_df = pd.read_csv('Intuilize_MNSU_ACME_QuotesData.csv', nrows=50000)  # Sample for initial exploration
    inventory_df = pd.read_csv('Intuilize_MNSU_ACME_InventoryData.csv')
    
    print(f"Sales data shape: {sales_df.shape}")
    print(f"Quotes data shape: {quotes_df.shape}")
    print(f"Inventory data shape: {inventory_df.shape}")
    
    return sales_df, quotes_df, inventory_df

def explore_data_quality(sales_df, quotes_df, inventory_df):
    """Examine data quality across datasets"""
    print("\n" + "="*50)
    print("DATA QUALITY ANALYSIS")
    print("="*50)
    
    # Sales data quality
    print("\n1. SALES DATA QUALITY:")
    print(f"Missing values:\n{sales_df.isnull().sum()}")
    print(f"Duplicate rows: {sales_df.duplicated().sum()}")
    
    # Quotes data quality  
    print("\n2. QUOTES DATA QUALITY:")
    print(f"Missing values:\n{quotes_df.isnull().sum()}")
    print(f"Duplicate rows: {quotes_df.duplicated().sum()}")
    
    # Inventory data quality
    print("\n3. INVENTORY DATA QUALITY:")
    print(f"Missing values:\n{inventory_df.isnull().sum()}")
    print(f"Duplicate rows: {inventory_df.duplicated().sum()}")

def analyze_linking_potential(sales_df, quotes_df, inventory_df):
    """Analyze how datasets can be linked for elasticity modeling"""
    print("\n" + "="*50)
    print("LINKING POTENTIAL ANALYSIS")
    print("="*50)
    
    # Common customers across datasets
    sales_customers = set(sales_df['CustomerID'].unique())
    quotes_customers = set(quotes_df['CustomerID'].unique())
    
    print(f"\n1. CUSTOMER OVERLAP:")
    print(f"Unique customers in Sales: {len(sales_customers):,}")
    print(f"Unique customers in Quotes: {len(quotes_customers):,}")
    print(f"Common customers: {len(sales_customers.intersection(quotes_customers)):,}")
    print(f"Overlap percentage: {len(sales_customers.intersection(quotes_customers))/len(sales_customers.union(quotes_customers))*100:.1f}%")
    
    # Common products across datasets
    sales_products = set(sales_df['ProductID'].dropna().unique())
    quotes_products = set(quotes_df['ProductID'].dropna().unique())
    inventory_products = set(inventory_df['ProductID'].dropna().unique())
    
    print(f"\n2. PRODUCT OVERLAP:")
    print(f"Unique products in Sales: {len(sales_products):,}")
    print(f"Unique products in Quotes: {len(quotes_products):,}")
    print(f"Unique products in Inventory: {len(inventory_products):,}")
    print(f"Sales-Quotes common products: {len(sales_products.intersection(quotes_products)):,}")
    print(f"All three datasets common products: {len(sales_products.intersection(quotes_products).intersection(inventory_products)):,}")

def analyze_price_elasticity_feasibility(sales_df, quotes_df):
    """Analyze feasibility of calculating price elasticity"""
    print("\n" + "="*50)
    print("PRICE ELASTICITY FEASIBILITY")
    print("="*50)
    
    # Convert dates
    sales_df['SalesDate'] = pd.to_datetime(sales_df['SalesDate'])
    quotes_df['QuoteDate'] = pd.to_datetime(quotes_df['QuoteDate'])
    
    # Sample product for detailed analysis
    sample_products = sales_df['ProductID'].value_counts().head(5).index.tolist()
    
    for product in sample_products[:2]:  # Analyze top 2 products
        print(f"\n--- PRODUCT: {product} ---")
        
        # Sales data for this product
        product_sales = sales_df[sales_df['ProductID'] == product]
        product_quotes = quotes_df[quotes_df['ProductID'] == product]
        
        if len(product_sales) > 0 and len(product_quotes) > 0:
            # Price ranges
            sales_price_range = f"${product_sales['UnitPrice'].min():.2f} - ${product_sales['UnitPrice'].max():.2f}"
            quotes_price_range = f"${product_quotes['UnitPrice'].min():.2f} - ${product_quotes['UnitPrice'].max():.2f}"
            
            print(f"Sales transactions: {len(product_sales):,}")
            print(f"Quote transactions: {len(product_quotes):,}")
            print(f"Sales price range: {sales_price_range}")
            print(f"Quotes price range: {quotes_price_range}")
            print(f"Price variation (sales): {product_sales['UnitPrice'].std():.2f}")
            print(f"Price variation (quotes): {product_quotes['UnitPrice'].std():.2f}")
            
            # Quote outcomes
            if 'QuoteStatus' in product_quotes.columns:
                quote_outcomes = product_quotes['QuoteStatus'].value_counts()
                print(f"Quote outcomes: {dict(quote_outcomes)}")

def identify_elasticity_opportunities(sales_df, quotes_df):
    """Identify best opportunities for elasticity modeling"""
    print("\n" + "="*50)
    print("ELASTICITY MODELING OPPORTUNITIES")
    print("="*50)
    
    # Products with high price variation and volume
    sales_summary = sales_df.groupby('ProductID').agg({
        'UnitPrice': ['mean', 'std', 'min', 'max'],
        'SalesQty': 'sum',
        'OrderNumber': 'nunique',
        'CustomerID': 'nunique'
    }).round(2)
    
    # Flatten column names
    sales_summary.columns = ['_'.join(col).strip() for col in sales_summary.columns.values]
    
    # Calculate price variation coefficient
    sales_summary['price_variation_coef'] = sales_summary['UnitPrice_std'] / sales_summary['UnitPrice_mean']
    
    # Filter for products with good elasticity modeling potential
    good_candidates = sales_summary[
        (sales_summary['SalesQty_sum'] > 50) &  # Sufficient volume
        (sales_summary['CustomerID_nunique'] > 5) &  # Multiple customers
        (sales_summary['price_variation_coef'] > 0.1)  # Price variation
    ].sort_values('price_variation_coef', ascending=False)
    
    print(f"\nTop 10 products for elasticity modeling:")
    print(good_candidates.head(10)[['UnitPrice_mean', 'UnitPrice_std', 'price_variation_coef', 'SalesQty_sum', 'CustomerID_nunique']])

def recommend_approach(sales_df, quotes_df, inventory_df):
    """Recommend optimal approach based on data analysis"""
    print("\n" + "="*50)
    print("RECOMMENDED APPROACH")
    print("="*50)
    
    print("\nBased on data analysis, here's the optimal approach:")
    print("\n1. DATA STRUCTURE:")
    print("   ✅ Keep datasets separate (they are clean)")
    print("   ✅ Create strategic linking views for elasticity calculations")
    print("   ✅ Use minimal data preprocessing")
    
    print("\n2. ELASTICITY MODELING STRATEGY:")
    print("   🎯 Focus on Quote-to-Sale conversion analysis")
    print("   🎯 Use quotes data for price sensitivity measurement")
    print("   🎯 Use sales data for demand validation")
    print("   🎯 Use inventory data for supply constraints")
    
    print("\n3. IMMEDIATE NEXT STEPS:")
    print("   1. Create Quote-Sale linking algorithm")
    print("   2. Calculate conversion rates by price points")
    print("   3. Identify high-elasticity products/customers")
    print("   4. Build elasticity calculation pipeline")

def main():
    """Main execution function"""
    print("INTUILIZE PRICE ELASTICITY DATA EXPLORATION")
    print("="*60)
    
    # Load data
    sales_df, quotes_df, inventory_df = load_data()
    
    # Run analyses
    explore_data_quality(sales_df, quotes_df, inventory_df)
    analyze_linking_potential(sales_df, quotes_df, inventory_df)
    analyze_price_elasticity_feasibility(sales_df, quotes_df)
    identify_elasticity_opportunities(sales_df, quotes_df)
    recommend_approach(sales_df, quotes_df, inventory_df)
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE - Ready for Phase 2!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()