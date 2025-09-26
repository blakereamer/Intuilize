import pandas as pd
import numpy as np
import os

def analyze_datasets():
    data_dir = r'c:\Users\Bream\Desktop\Intuilize Project\Intuilize Data'
    
    datasets = {
        'Sales': 'Intuilize_MNSU_ACME_SalesData.csv',
        'Inventory': 'Intuilize_MNSU_ACME_InventoryData.csv', 
        'Quotes': 'Intuilize_MNSU_ACME_QuotesData.csv'
    }
    
    print("🔍 DATASET ANALYSIS REPORT")
    print("="*50)
    
    for name, filename in datasets.items():
        filepath = os.path.join(data_dir, filename)
        
        try:
            print(f"\n📊 {name} Dataset:")
            
            # Read a sample to understand structure
            sample_df = pd.read_csv(filepath, nrows=10)
            print(f"   Sample shape: {sample_df.shape}")
            print(f"   Columns: {list(sample_df.columns)}")
            
            # Get full dataset info (just shape)
            full_df = pd.read_csv(filepath)
            print(f"   Full shape: {full_df.shape}")
            print(f"   Memory usage: {full_df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Show data types
            print(f"   Data types:")
            for col, dtype in full_df.dtypes.items():
                print(f"      {col}: {dtype}")
            
            # Show sample data
            print(f"   Sample rows:")
            print(sample_df.head(3).to_string())
            print()
            
        except Exception as e:
            print(f"   ❌ Error loading {name}: {str(e)}")
            continue

if __name__ == "__main__":
    analyze_datasets()