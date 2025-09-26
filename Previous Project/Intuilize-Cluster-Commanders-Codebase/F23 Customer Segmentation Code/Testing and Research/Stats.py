
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


#Fields/Column Names
    #Location ID
    #Location
    #Branch ID
    #Branch Name
    #Sales Date
    #Invoice Number
    #Product Group
    #Product ID or Code
    #Customer ID or Code
    #Customer Name
    #ExtCost
    #ExtPrice
    #Sales Quantity
    #UnitCost
    #UnitPrice
    #GM%


#DEFINITIONS:
#GM% = Gross Margin, or Profit Margin CALCULATED AS: (ExtPrice - ExtCost)/ExtPrice
#ExtCost = How much it costs the seller
#Sales Quantity = Sales Quantity from Sales Transactions
#ExtPrice = Sales Amount
#UnitCost = ExtCost divided by SalesQty
#UnitPrice = ExtPrice divided by SalesQty


#Planned Stats:
'''
Sales Analysis:
    Total sales volume.
    Revenue by product, service, or category.
    Profit margins on sales.
    Sales trends over time.
    Seasonal variations in sales.
Customer Analysis:
    Number of unique customers.
    ~~~~~~Customer segmentation based on transaction behavior~~~~~ This is for AJ and Nift.
    Customer lifetime value.
Product/Service Performance:
    Top-selling products or services.
    Product popularity over time.
    Seasonal variations in product sales.

Fraud Detection:
    Anomalies or irregular patterns in transaction data. <<<<<<<<<<<<-------------------------------- We Are HERE!
    Unusual transaction amounts or frequencies.

######################NAHOM WORK BELOW##############################
Customer Retention:
    Churn rate.
Cross-Selling and Upselling Opportunities:
    Identifying products frequently purchased together.
    Recommender systems for cross-selling.
    Recurring Revenue Analysis
    Revenue from recurring sources.
'''


def basic_statistics(df):
    print("--------------------------------Basic Statistics------------------------------------------------")
    print(df.describe())

def amount_of_unique_customers(df):
    print("--------------------------------Amount Of Unique Customers------------------------------------------------")
    unique_customers = df['CustomerCode'].nunique()
    print(f'The number of unique customers is: {unique_customers}')

def best_sellers(df):
    print("--------------------------------Best Sellers------------------------------------------------")
    top_products = df.groupby('ProductCode')['ExtPrice'].sum().nlargest(10)  # Using nlargest for top 10
    formatted_top_products = top_products.apply(lambda x: "$" + '{:,.0f}'.format(x))
    print(formatted_top_products)

def revenue_by_product(df):
    print("--------------------------------Revenue By Product------------------------------------------------")
    revenue_by_product = df.groupby('ProductCode')['ExtPrice'].sum()
    print("Revenue by Product:")
    print(revenue_by_product)

def profit_margin_data(df):

    print("--------------------------------Total Sales Volume------------------------------------------------")
    total_sales_volume = df['ExtPrice'].sum()
    print(f'Total Sales Volume: ${total_sales_volume:,.2f}')

    print("--------------------------------Profit Margin On Sales(Total Over All Sales)------------------------------------------------")
    df['Profit'] = df['ExtPrice'] - df['ExtCost']
    total_profit = df['Profit'].sum()
    total_revenue = df['ExtPrice'].sum()
    profit_margin = (total_profit / total_revenue) * 100
    print(f'Profit Margin on Sales: {profit_margin:.2f}%')

    print("--------------------------------Total Gross Profit------------------------------------------------")
    raw_profit_margin = profit_margin/100
    total_gross_profit = total_sales_volume * (raw_profit_margin)
    print(total_gross_profit)

def sales_trends_over_time(df):
    print("--------------------------------Sales Trends Over Time (By Month Sales)------------------------------------------------")
    # Extract year and month from SalesDate
    df['Year'] = df['SalesDate'].dt.year
    df['Month'] = df['SalesDate'].dt.month

    # Group by Year and Month and sum the sales
    sales_trends = df.groupby(['Year', 'Month'])['ExtPrice'].sum()

    # Create a separate line for each year
    plt.figure(figsize=(10, 6))
    for year in sales_trends.index.levels[0]:
        year_sales = sales_trends.loc[year]
        plt.plot(year_sales.index.get_level_values('Month'), year_sales.values, marker='o', label=year)

    plt.title('Sales Trends Over Time (By Month)')
    plt.xlabel('Month')
    plt.ylabel('Total Sales(In Tens Of Millions)')
    plt.grid(True)
    plt.xticks(range(1, 13))
    plt.legend(title='Year')
    plt.tight_layout() #NOCLIP CHEAT
    plt.show()
    print(sales_trends)

def customer_lifetime_value(df):
    print("--------------------------------Customer Lifetime Value (CLV - In Days)----------------------------------------")
    # Calculate total revenue per customer
    revenue_per_customer = df.groupby('CustomerCode')['ExtPrice'].sum()

    # Calculate the average lifespan of a customer (in months)
    # Assuming lifespan is calculated based on the difference between the first and last transaction dates
    lifespan_per_customer = df.groupby('CustomerCode')['SalesDate'].agg(['min', 'max'])
    lifespan_per_customer['Lifespan'] = (lifespan_per_customer['max'] - lifespan_per_customer['min']).dt.days / 30
    
    # Filter out customers with zero lifespans (AKA They only purchased once.)
    lifespan_per_customer = lifespan_per_customer[lifespan_per_customer['Lifespan'] > 0]

    print("Customer Lifetime In Months: ")
    print(lifespan_per_customer)

    # Calculate CLV as the product of average revenue per month and lifespan
    clv = (revenue_per_customer / lifespan_per_customer['Lifespan']).fillna(0)

    print("Customer Lifetime Value (CLV):")
    print(clv)

    top_clv = clv.nlargest(10)

    print("--------------------------------Top Ten Customers By CLV-----------------------------------")
    for key, value in top_clv.items():
        print(f"{key}: {value:.2f}")

    highest_lifetimes = lifespan_per_customer.nlargest(10, 'Lifespan')

    print("--------------------------------Top Ten Customers By Lifespan-----------------------------------")
    print(highest_lifetimes)


def main():
    #Intuilize_MNSU_SampleSales_V1_011524 - Intuilize_SampleSales_V1_011524.csv
    file_path = 'Data/SampleDataCleaned.csv'

    # Read the Excel file with Pandas
    df = pd.read_csv(file_path)

    #Do all of the neccecary conversions so that the code can actually run without breaking!
    #TODO Just do this once and save it to a new file...
    #df['ExtPrice'] = df['ExtPrice'].replace('[\$,]', '', regex=True).astype(float)
    #df['ExtCost'] = df['ExtCost'].replace('[\$,]', '', regex=True).astype(float)
    #df['UnitCost'] = df['UnitCost'].replace('[\$,]', '', regex=True).astype(float)
    #df['UnitPrice'] = df['UnitPrice'].replace('[\$,]', '', regex=True).astype(float)

    # Convert the date column to datetime format
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])

    #print(df.dtypes) # This is for us programmers. This data does not matter.

    basic_statistics(df)
    amount_of_unique_customers(df)
    best_sellers(df)
    profit_margin_data(df)
    revenue_by_product(df)
    sales_trends_over_time(df)
    customer_lifetime_value(df)


    #df.to_csv('SampleDataCleaned.csv', index=False) #Only Need To Use This Once...





if __name__ == "__main__":
    main()