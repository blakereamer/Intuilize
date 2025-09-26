import pandas as pd

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

def ExcelToCleanedCSV(file_path):
    # Read the Excel file with Pandas
    df = pd.read_excel(file_path)

    #Do all of the neccecary conversions so that the code can actually run without breaking!
    df['ExtPrice'] = df['ExtPrice'].replace('[\$,]', '', regex=True).astype(float)
    df['ExtCost'] = df['ExtCost'].replace('[\$,]', '', regex=True).astype(float)
    df['UnitCost'] = df['UnitCost'].replace('[\$,]', '', regex=True).astype(float)
    df['UnitPrice'] = df['UnitPrice'].replace('[\$,]', '', regex=True).astype(float)

    # Convert the date column to datetime format
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])

    print(df.dtypes) # This is for us programmers. This data does not matter.

    df.to_csv('SampleDataCleaned-ALLTIME.csv', index=False) #Only Need To Use This Once...




def ClassificationCSV(file_path, Months):
    # Read the sample data
    data = pd.read_csv(file_path)

    columns_to_drop = ['Recency', 'Frequency', 'MonetaryValue', 'CLV']
    data = data.drop(columns=columns_to_drop)
    # Convert 'SalesDate' to datetime
    data['SalesDate'] = pd.to_datetime(data['SalesDate'])

    # Calculate Recency, Frequency, MonetaryValue
    max_sales_date = data['SalesDate'].max()
    
    months_ago = max_sales_date - pd.DateOffset(months = Months)
    active_customers_df = data[data['SalesDate'] >= months_ago]
    snapshot_date = max(active_customers_df['SalesDate']) + pd.DateOffset(days=1)
    active_customers_df['Recency'] = (snapshot_date - active_customers_df['SalesDate']).dt.days
    rfm_data = active_customers_df.groupby('CustomerCode').agg({
        'Recency': 'min',
        'InvoiceNumber': 'count',
        'ExtPrice': 'sum'
    }).reset_index()
    rfm_data.columns = ['CustomerCode', 'Recency', 'Frequency', 'MonetaryValue']

    # Calculate RFM Score
    rfm_data['Recency'] = snapshot_date - pd.to_datetime(rfm_data['Recency'], unit='D')
    rfm_data['Recency'] = rfm_data['Recency'].dt.days
    rfm_data['RFM_Score'] = rfm_data['Recency'] + rfm_data['Frequency'] + rfm_data['MonetaryValue']

    # Normalize RFM Score to range 1-10
    rfm_data['RFM_Rank'] = pd.qcut(rfm_data['RFM_Score'], q=10, labels=False)

    # Calculate AvgPurchasePrice at the customer level
    avg_purchase_price = data.groupby('CustomerCode').apply(lambda x: x['ExtPrice'].sum() / x['CustomerCode'].count()).reset_index(name='AvgPurchasePrice')

    # Merge with AvgPurchasePrice
    final_data = pd.merge(rfm_data, avg_purchase_price, on='CustomerCode', how='left')

    # Calculate AvgDaysBetweenOrders
    # Sort the data by 'CustomerCode' and 'SalesDate' columns
    active_customers_df.sort_values(by=['CustomerCode', 'SalesDate'], inplace=True)

    # Calculate AvgDaysBetweenOrders
    active_customers_df['SalesDate_shifted'] = active_customers_df.groupby('CustomerCode')['SalesDate'].shift(1)
    active_customers_df['DaysBetweenOrders'] = (active_customers_df['SalesDate'] - active_customers_df['SalesDate_shifted']).dt.days

    avg_days_between_orders = active_customers_df.groupby('CustomerCode')['DaysBetweenOrders'].mean().reset_index()
    avg_days_between_orders.columns = ['CustomerCode', 'AvgDaysBetweenOrders']

    # Merge RFM data with AvgDaysBetweenOrders
    final_data = pd.merge(final_data, avg_days_between_orders, on='CustomerCode', how='left')



    # Save to CSV
    final_data = pd.merge(active_customers_df, final_data, on='CustomerCode', how='left')
    final_data.to_csv('Data/CustomerStats.csv', index=False)

    print("CSV file created successfully!")

def main():
    #Intuilize_MNSU_SampleSales_V1_011524 - Intuilize_SampleSales_V1_011524.csv
    file_path = 'Data\\SampleDataCleaned.csv'
    file_path_excel = 'Data\\Intuilize_MNSU_SampleSales_V1_011524.xlsx'

    #ExcelToCleanedCSV(file_path)
    ClassificationCSV(file_path, 36)
    #ExcelToCleanedCSV(file_path_excel)




if __name__ == "__main__":
    main()