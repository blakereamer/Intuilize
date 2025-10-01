# Intuilize Elasticity Modeling Project

## 📋 Project Overview
This repository contains a comprehensive data science project for **price elasticity modeling** using ACME company's sales, quotes, and inventory data. The project features advanced feature engineering, customer segmentation via RFM analysis, and robust datasets ready for elasticity modeling.

### 🎯 Business Objective
Develop price elasticity models to optimize pricing strategies by understanding how price changes affect customer demand across different customer segments and product categories.

---

## 🗂️ Repository Structure

```
Intuilize Project/
├── 📁 datasets/
│   ├── 📁 enhanced/          # ⭐ MAIN DATASETS (Use These)
│   │   ├── customer_features_enhanced.csv    # 1,077 customers × 69 features
│   │   ├── product_features_enhanced.csv     # 40,359 products × 62 features  
│   │   └── merged_elasticity_dataset_enhanced.csv  # 1.42M transactions × 40 features
│   └── 📁 original/          # 📦 REFERENCE ONLY
│       ├── customer_features.csv            # Original smaller feature set
│       ├── product_features.csv             # Original smaller feature set
│       └── merged_elasticity_dataset.csv    # Original merged dataset
├── 📁 scripts/
│   ├── enhanced_feature_engineering.py      # ⭐ MAIN SCRIPT - Creates enhanced datasets
│   ├── data_exploration_elasticity.py       # Exploratory data analysis
│   ├── data_analysis.py                     # Additional analysis functions
│   └── data_integration_and_feature_engineering_comprehensive.ipynb  # Full notebook
├── 📁 documentation/
│   ├── COMPREHENSIVE_DATA_DICTIONARY.md     # ⭐ FEATURE DOCUMENTATION
│   ├── ENHANCED_FEATURE_ENGINEERING_SUMMARY.md  # Project completion summary
│   ├── ELASTICITY_FEATURES_DOCUMENTATION.md     # Elasticity-specific features
│   └── Intuilize_Project_Plan.md            # Original project plan
├── 📁 Intuilize Data/         # 🔒 SOURCE DATA (Read-only)
│   ├── Intuilize_MNSU_ACME_SalesData.csv    # 1.42M sales transactions
│   ├── Intuilize_MNSU_ACME_QuotesData.csv   # 2.64M quote records
│   └── Intuilize_MNSU_ACME_InventoryData.csv # 33K inventory records
├── 📁 Previous Project/       # 📚 HISTORICAL REFERENCE
└── 📄 Intuilize _ MNSU - Project Descriptions - V4 - 04.30.2025 (1).pdf
```

---

## 🚀 Quick Start

### 1. **For Elasticity Modeling** 
Start with these files:
- **Data**: `datasets/enhanced/merged_elasticity_dataset_enhanced.csv`
- **Documentation**: `documentation/COMPREHENSIVE_DATA_DICTIONARY.md`
- **Key Variables**: `UnitPrice` (price), `SalesQty` (demand), customer context, product context

### 2. **For Customer Segmentation**
- **Data**: `datasets/enhanced/customer_features_enhanced.csv`  
- **Key Features**: `RFMScore`, `CustomerLifetimeValue`, `CustomerLoyaltyScore`

### 3. **For Product Analysis**
- **Data**: `datasets/enhanced/product_features_enhanced.csv`
- **Key Features**: `PriceVolatility`, `CustomerPenetration`, `ProfitMargin`

---

## 📊 Dataset Summary

### Enhanced Datasets vs Original Comparison

| Dataset | Metric | Original | Enhanced | Improvement |
|---------|--------|----------|----------|-------------|
| **Customer Features** | Records | 1,077 | 1,077 | Same (100% coverage) |
|  | Features | 42 | 69 | +27 features (+64.3%) |
|  | New Features | - | RFM Analysis, Loyalty Scores, Advanced Metrics | ✅ |
| **Product Features** | Records | 40,359 | 40,359 | Same (complete catalog) |
|  | Features | 42 | 62 | +20 features (+47.6%) |
|  | New Features | - | Market Penetration, Customer Analytics | ✅ |
| **Merged Dataset** | Records | 2.64M | 1.42M | Focused on sales data |
|  | Features | 131 | 40 | Streamlined for elasticity |
|  | Quality | Many duplicated/messy columns | Clean, focused features | ✅ |

### Key Improvements in Enhanced Datasets:
1. **🎯 Customer Segmentation**: Complete RFM analysis with loyalty scoring
2. **📈 Elasticity Features**: Purpose-built elasticity indicators and proxies  
3. **🧹 Data Quality**: Cleaned, standardized, and focused feature sets
4. **📋 Documentation**: Every feature explained with business context
5. **🔍 Market Intelligence**: Customer penetration and product positioning metrics

---

## 📈 Key Features for Elasticity Modeling

### Core Price Elasticity Variables
- **`UnitPrice`**: Price per unit (independent variable)
- **`SalesQty`**: Quantity demanded (dependent variable)  
- **`PriceElasticityProxy`**: SalesQty / (UnitPrice + 1) - demand sensitivity indicator
- **`PriceVolatility`**: Price variation measure - elasticity indicator

### Customer Context (Control Variables)
- **`RFMScore`**: Customer segment (e.g., "555" = high value, recent, frequent)
- **`CustomerLifetimeValue`**: Total customer worth
- **`CustomerLoyaltyScore`**: Composite loyalty metric
- **`Recency`**, **`Frequency`**, **`Monetary`**: RFM components

### Product Context (Control Variables)  
- **`CustomerPenetration`**: Market reach of product
- **`ProfitMargin`**: Product profitability
- **`SalesFrequency`**: Demand pattern indicator
- **`CustomerBase`**: Number of customers buying product

---

## 🛠️ Technical Details

### Data Scope
- **Customer Coverage**: 1,077 unique customers (100% of available)
- **Product Coverage**: 40,359 unique products (complete catalog)
- **Transaction Coverage**: 1,420,050 sales transactions
- **Total Revenue**: $264,759,655.99
- **Date Range**: October 2021 - September 2025

### Data Quality
- **Missing Values**: Handled with appropriate fill strategies
- **Customer Sampling**: Stratified by value (20% high, 60% mid, 20% low)
- **Feature Engineering**: RFM analysis, temporal metrics, elasticity proxies
- **Validation**: Complete data dictionary with business interpretations

### Key Scripts
- **`enhanced_feature_engineering.py`**: Main script to regenerate enhanced datasets
- **`data_integration_and_feature_engineering_comprehensive.ipynb`**: Interactive analysis notebook

---

## 📚 Documentation

### Must-Read Documents
1. **`COMPREHENSIVE_DATA_DICTIONARY.md`** - Explains every feature in detail
2. **`ENHANCED_FEATURE_ENGINEERING_SUMMARY.md`** - Project completion overview
3. **This README.md** - Project organization and quick start

### Feature Categories Explained
- **Revenue & Financial**: Total revenue, profit margins, cost structures
- **Behavioral**: Purchase patterns, order frequency, loyalty metrics  
- **Temporal**: Customer lifetime, purchase cycles, seasonal patterns
- **Market**: Customer penetration, product positioning, demand strength
- **Elasticity**: Price sensitivity indicators, demand proxies, volatility measures

---

## 🎯 Next Steps for Analysis

### Immediate Actions
1. **Load Enhanced Data**: Use `datasets/enhanced/merged_elasticity_dataset_enhanced.csv`
2. **Review Features**: Study `documentation/COMPREHENSIVE_DATA_DICTIONARY.md`
3. **Segment Analysis**: Explore RFM customer segments for different elasticity patterns
4. **Model Development**: Build elasticity models using price-quantity relationships

### Advanced Modeling
1. **Segment-Specific Models**: Different elasticity by customer tier (RFM segments)
2. **Product Category Analysis**: Elasticity patterns by product characteristics  
3. **Time-Series Modeling**: Temporal elasticity changes using enhanced features
4. **Cross-Elasticity**: Product substitution using comprehensive product features

### Business Applications
1. **Dynamic Pricing**: Optimize prices using elasticity models
2. **Customer Targeting**: Personalized pricing based on loyalty segments
3. **Inventory Planning**: Demand forecasting with enhanced product features
4. **Profitability**: Balance pricing and margins using comprehensive metrics

---

## ⚠️ Important Notes

### File Usage Guidelines
- **✅ USE**: `datasets/enhanced/` - These are the main, cleaned datasets
- **📦 REFERENCE**: `datasets/original/` - Keep for comparison, don't use for modeling
- **🔒 PRESERVE**: `Intuilize Data/` - Original source data, don't modify

### Customer Count Clarification
The **1,077 customers** represents **100% of unique customers** in the source data. This may seem small compared to 1.4M transactions, but indicates high customer activity with many repeat purchases.

### Data Freshness
Enhanced datasets were generated on September 30, 2025, and include all available historical data through that date.

---

## 🔧 Environment Requirements

### Python Dependencies
```python
pandas>=2.0.0
numpy>=1.20.0
scikit-learn>=1.0.0
```

### Recommended Setup
```bash
# Load main dataset
import pandas as pd
df = pd.read_csv('datasets/enhanced/merged_elasticity_dataset_enhanced.csv')

# Review features
features_doc = open('documentation/COMPREHENSIVE_DATA_DICTIONARY.md').read()
```

---

## 📞 Project Context

**Client**: ACME Company  
**Objective**: Price elasticity modeling for dynamic pricing optimization  
**Data Source**: Sales, Quotes, and Inventory systems  
**Scope**: Complete transaction history with customer and product context  
**Deliverable**: Enhanced datasets with comprehensive feature engineering for elasticity analysis

---

*Last Updated: September 30, 2025*  
*Repository Status: ✅ Complete and Ready for Elasticity Modeling*