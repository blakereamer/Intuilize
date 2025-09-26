# INTUILIZE PRICE ELASTICITY MODELING - FEATURES & CONNECTIONS DOCUMENTATION
**Date:** September 23, 2025  
**Project:** Price Sensitivity/Elasticity Prediction Model  
**Phase:** Pre-Development Documentation  

---

## 📊 DATASET OVERVIEW

### **1. Sales Data** (`Intuilize_MNSU_ACME_SalesData.csv`)
- **Size:** 1,420,050 records
- **Quality:** Extremely clean, no missing critical fields
- **Purpose:** Historical transaction data showing actual purchases and realized prices

**Schema (20 fields):**
```
BranchID, BranchName, OrderNumber, InvoiceNumber, LineNumber, 
OrderDate, SalesDate, SalesPersonID, SalesPersonName, 
ProductID, ProductGroupID, CustomerID, CustomerName, 
ExtPrice, ExtCost, SalesQty, UnitPrice, UnitCost, UOM, UnitSize
```

### **2. Quotes Data** (`Intuilize_MNSU_ACME_QuotesData.csv`)
- **Size:** 2,635,612 records
- **Quality:** Clean, complete records
- **Purpose:** Price experiments and customer responses - CRITICAL for elasticity

**Schema (19 fields):**
```
BranchID, BranchName, QuoteID, QuoteVersion, QuoteDate, ExpirationDate, 
SalesPersonID, SalesPersonName, CustomerID, CustomerName, 
ProductID, ProductGroupID, QuoteQty, UnitPrice, UOM, UnitSize, 
QuoteStatus, ConvertedToOrderNumber, ConversionDate
```

### **3. Inventory Data** (`Intuilize_MNSU_ACME_InventoryData.csv`)
- **Size:** 33,793 records
- **Quality:** Minor issue with ~1% missing ProductIDs
- **Purpose:** Supply context for elasticity calculations

**Schema (4 fields):**
```
BranchID, BranchName, ProductID, QtyOnHand
```

---

## 🔗 CRITICAL DATA CONNECTIONS

### **Primary Connection: Quote-to-Sale Pipeline**
**DISCOVERY:** Quotes data contains direct links to sales via `ConvertedToOrderNumber` field!

**Connection Pattern:**
```
Quote (Q00000000) → Conversion → Order (2040100) → Sale Record
```

**Examples Found:**
- Quote Q00000000: $26.95 → Won → Order 2040100
- Quote Q00000001: $22.925 → Won → Order 2041740  
- Quote Q00000004: $6.98 → Revised to $10.24 → Won → Order 2042746

### **Secondary Connections:**
1. **Customer-Product Pairs:** Same customers/products appear across datasets
2. **Temporal Relationships:** Quote dates precede sales dates
3. **Price Negotiations:** Multiple quote versions show price sensitivity

---

## 🎯 ELASTICITY-CRITICAL FEATURES

### **From Sales Data:**
**Direct Elasticity Indicators:**
- `UnitPrice` - Realized prices after negotiation
- `SalesQty` - Actual demand at realized prices
- `ExtPrice` - Total transaction value
- `SalesDate` - Timing of purchase decision

**Segmentation Features:**
- `CustomerID` - Customer behavior patterns
- `ProductID` - Product characteristics
- `ProductGroupID` - Product category elasticity
- `BranchID` - Regional price sensitivity

**Profitability Context:**
- `ExtCost` - Cost basis for pricing flexibility
- `UnitCost` - Margin calculations

### **From Quotes Data (GOLDMINE for Elasticity):**
**Price Sensitivity Indicators:**
- `QuoteStatus` - Win/Loss at specific prices
  - "Won" (77.6%) - Price accepted
  - "Revised" (22.4%) - Price negotiation required
- `UnitPrice` - Quoted prices across spectrum
- `QuoteQty` - Quantity sensitivity to price

**Negotiation Patterns:**
- `QuoteVersion` - Price revision cycles
- `QuoteDate` vs `ConversionDate` - Decision timing
- `ConvertedToOrderNumber` - Success tracking

**Time-Based Analysis:**
- `QuoteDate` - When price was offered
- `ExpirationDate` - Urgency factors
- `ConversionDate` - Purchase timing

### **From Inventory Data:**
**Supply Constraints:**
- `QtyOnHand` - Stock availability affecting elasticity
- Filter out supply-constrained periods from elasticity analysis

---

## 🧮 ELASTICITY CALCULATION OPPORTUNITIES

### **1. Quote Win/Loss Analysis**
```
Price Sensitivity = f(Quote Price, Win Rate, Quantity)

Example Pattern Discovered:
- Product YLV-338-KN7: $26.95 → 100% win rate (CUST1)
- Product YLV-338-KN7: $22.925 → 100% win rate (CUST2)  
- Same product, different customers → Customer segments!
```

### **2. Price Revision Analysis**
**Discovered Pattern:** Multiple quote versions show negotiation
```
Quote Q00000004: Version 1: $6.98 → Version 2: $10.24 → Won
Price Elasticity = % Change in acceptance / % Change in price
```

### **3. Cross-Time Price Analysis**
**Historical price changes across seasons/periods for same products**

### **4. Customer-Specific Elasticity**
**Same product, different prices to different customers**

---

## 🏗️ PREVIOUS PROJECT ASSETS TO LEVERAGE

### **Existing Customer Segmentation Models:**
1. **Fuzzy C-Means Clustering** - Sophisticated customer segments
2. **Hierarchical Clustering** - Customer tier identification  
3. **K-Means** - Basic customer groupings

**Key Files to Reuse:**
- `fuzzy_cmeans_model.pkl` - Trained customer segments
- `customer_metrics_with_product_related_features.csv` - Rich customer features
- `feature_creation.ipynb` - Feature engineering pipeline

### **Feature Engineering Framework:**
**From `feature_creation.ipynb`:**
```python
# Customer Metrics Already Built:
- TotalSalesPrice, TotalCost, TotalProfit
- AvgUnitPrice, AvgUnitCost
- ProfitMargin, AvgOrderSize  
- RepeatPurchaseRatio, PriceVolatility
```

---

## 💡 STRATEGIC ELASTICITY FEATURES TO CREATE

### **Phase 2 Feature Engineering Priorities:**

**1. Price Sensitivity Scores:**
```python
# Customer-level
customer_price_sensitivity = quote_win_rate_by_price_tier
customer_negotiation_frequency = quote_revisions / total_quotes

# Product-level  
product_elasticity_coefficient = %_demand_change / %_price_change
product_price_volatility = std(unit_prices) / mean(unit_prices)
```

**2. Quote-to-Sale Conversion Metrics:**
```python
conversion_rate_by_price = sales_count / quotes_count (by price bands)
average_negotiation_cycles = avg(quote_versions)
price_concession_patterns = final_price / initial_quote_price
```

**3. Time-Based Elasticity:**
```python
seasonal_price_sensitivity = elasticity by month/quarter
urgency_elasticity = conversion_rate by (expiration_date - quote_date)
```

**4. Segment-Specific Elasticity:**
```python
# Combining existing customer segments with new price features
customer_segment_elasticity = elasticity by fuzzy_cluster
product_category_elasticity = elasticity by product_group
```

---

## 🎯 STRATEGIC APPROACH - HYBRID SEGMENTATION-ELASTICITY METHODOLOGY

### **Phase 1: Enhanced Customer & Product Segmentation**
**Primary Approach: Build upon previous fuzzy c-means foundation with elasticity-focused enhancements**

#### **Customer Segmentation Enhancement:**
- **Base Model**: Leverage existing fuzzy c-means customer segmentation from previous work
- **Enhancement Strategy**: 
  - ✅ Retrain models using complete dataset (Sales + Quotes + Inventory, not just Sales)
  - ✅ Add elasticity-specific features: quote response rates, price change sensitivity, negotiation patterns
  - ✅ Incorporate temporal patterns: seasonal behavior, purchase frequency evolution
- **New Features**: Quote-to-sale conversion rates, price negotiation history, volume sensitivity patterns

#### **Product Segmentation Development:**
- **New Implementation**: Create product segments based on price elasticity characteristics
- **Key Dimensions**: 
  - 📊 Price sensitivity levels (from quote acceptance/rejection patterns)
  - 📊 Volume elasticity (quantity changes vs. price changes)  
  - 📊 Competitive positioning (market share impact on pricing flexibility)
  - 📊 Seasonal demand patterns (inventory turnover rates)

### **Phase 2: Segment-Specific Elasticity Modeling**
**Approach: Train separate elasticity models for each customer-product segment combination**

#### **Model Architecture:**
- **Segmented Models**: Individual elasticity predictors for each customer segment × product segment combination
- **Feature Engineering**: Segment-specific elasticity indicators using quote conversion data
- **Cross-Segment Learning**: Transfer learning between similar segments to handle sparse data

#### **Elasticity Prediction Framework:**
- **Primary Signal**: Quote-to-sale conversion patterns (`ConvertedToOrderNumber` field)
- **Supporting Signals**: 
  - 💰 Price change impact on quote acceptance (77.6% baseline win rate)
  - 📦 Volume bundling effects from quantity analysis
  - ⚔️ Competitive response patterns from market data
  - 📅 Seasonal demand variations from temporal analysis

### **Phase 3: Integrated Prediction System**
**Output: Unified elasticity prediction system combining segment insights**

#### **Model Integration:**
- **Segment Assignment**: Automatic customer/product classification using enhanced clustering models
- **Elasticity Prediction**: Apply segment-specific models for price sensitivity forecasting
- **Business Intelligence**: Provide actionable insights for pricing optimization

#### **Validation Strategy:**
- **Ground Truth**: Quote win/loss rates (77.6% baseline win rate provides excellent signal)
- **Performance Metrics**: Conversion prediction accuracy, price sensitivity ranking correlation
- **Business Impact**: Revenue optimization potential, competitive positioning improvement

---

## 🏗️ REUSABILITY ASSESSMENT - PREVIOUS MODELS

### **RECOMMENDED: Partial Reuse with Enhancement**

#### **✅ Assets to Leverage:**
1. **Fuzzy C-Means Framework**: High-quality clustering methodology proven effective
2. **Feature Engineering Pipeline**: Existing customer metrics provide solid foundation
3. **Data Processing Infrastructure**: Established workflows for data integration
4. **Validation Methods**: Cross-validation and model evaluation frameworks

#### **🔄 Assets Requiring Enhancement:**
1. **Customer Segments**: Retrain with complete data (Sales + Quotes, not just Sales)
2. **Feature Set**: Add price sensitivity and negotiation behavior features
3. **Target Variable**: Shift from transaction-based to elasticity-based outcomes
4. **Temporal Modeling**: Incorporate quote timing and seasonal patterns

#### **❌ Assets Not Suitable:**
1. **Existing Trained Models**: Based on incomplete data (Sales-only, 2022-2023)
2. **Product-Only Focus**: Previous work primarily customer-focused
3. **Static Segmentation**: Need dynamic segments incorporating price behavior

---

## � IMPLEMENTATION ROADMAP - UPDATED

### **Phase 1: Foundation Enhancement** (Week 1-2)
1. **Data Integration**: Merge Sales + Quotes + Inventory using discovered connections
2. **Feature Engineering**: Create elasticity-specific features from quote conversion patterns
3. **Customer Segmentation**: Retrain fuzzy c-means with complete dataset and price features
4. **Product Segmentation**: Develop new product elasticity clusters

### **Phase 2: Elasticity Modeling** (Week 3-4)  
1. **Segment-Specific Models**: Build elasticity predictors for each customer-product segment
2. **Quote Conversion Modeling**: Predict quote success probability based on price/segment
3. **Price Sensitivity Quantification**: Calculate elasticity coefficients by segment
4. **Cross-Validation**: Test segment predictions against held-out quote outcomes

### **Phase 3: Integration & Optimization** (Week 5-6)
1. **Unified Prediction System**: Integrate segment assignment + elasticity prediction
2. **Business Intelligence Tools**: Create pricing optimization dashboards
3. **Validation**: Test against business outcomes and quote win rate improvements  
4. **Documentation**: Create deployment guides and model interpretation tools

---

## 📈 EXPECTED BUSINESS IMPACT - ENHANCED

### **Strategic Deliverables:**
1. **Customer-Product Elasticity Matrix**: Precise elasticity by segment combination (not just customer OR product)
2. **Dynamic Pricing Optimization**: Real-time price recommendations based on segment + market conditions
3. **Quote Success Predictor**: Probability of quote acceptance at different price points
4. **Negotiation Intelligence**: Optimal pricing strategies by customer segment
5. **Revenue Impact Calculator**: Quantify expected revenue changes from pricing decisions

### **Competitive Advantages:**
- 🏆 **Quote Data Goldmine**: Unique access to negotiation and conversion patterns (most companies lack this)
- 🎯 **Sophisticated Segmentation**: Building on proven fuzzy c-means methodology
- 📊 **Clean, Complete Data**: Near-perfect data quality enables advanced modeling
- 💡 **Hybrid Approach**: Combining best of customer segmentation + direct elasticity modeling
- ⚡ **77.6% Win Rate Signal**: Strong baseline for model validation and improvement

### **Measurable Outcomes:**
- **Quote Win Rate Optimization**: Target 80-85% through better pricing
- **Revenue Growth**: 5-15% through optimized pricing strategies  
- **Margin Improvement**: Better cost-price optimization by segment
- **Customer Retention**: Personalized pricing maintains relationships

---

**STATUS:** Strategy Refined with Hybrid Segmentation-Elasticity Approach ✅  
**NEXT ACTION:** Begin Phase 1 - Enhanced Foundation with Complete Dataset
**KEY INSIGHT:** Leverage existing fuzzy c-means excellence while adding elasticity dimensions