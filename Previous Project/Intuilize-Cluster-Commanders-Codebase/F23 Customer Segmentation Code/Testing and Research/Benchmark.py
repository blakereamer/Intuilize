import pandas as pd
import matplotlib.pyplot as plt
import time

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


def plot_purchase_history(file_path, customer_id):
    # Record the start time
    start_time = time.time()

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Filter data for the specified customer ID
    customer_data = df[df['CustomerCode'] == customer_id]

    # Check if the customer ID exists in the dataset
    if customer_data.empty:
        print(f"No data found for customer ID {customer_id}")
        return

    # Sort data by date for a chronological plot
    customer_data = customer_data.sort_values(by='SalesDate')

    # Create a line plot for purchase history
    plt.plot(customer_data['SalesDate'], customer_data['ExtPrice'], marker='o')
    plt.title(f'Purchase History for Customer ID {customer_id}')
    plt.xlabel('Date')
    plt.ylabel('Purchase Total?')
    plt.xticks(rotation=45)
    plt.show()

    # Record the end time
    end_time = time.time()

    # Calculate and print the time taken
    elapsed_time = end_time - start_time
    print(f'Time taken to generate the chart: {elapsed_time:.2f} seconds')


def find_largest_spender(file_path):
    # Record the start time
    start_time = time.time()

    # Read the Excel file
    df = pd.read_excel(file_path)

    # Group the data by customer ID and calculate the total purchase amount for each customer
    customer_totals = df.groupby('CustomerCode')['ExtPrice'].sum()

    # Find the customer with the highest total purchase amount
    largest_spender_id = customer_totals.idxmax()
    largest_spender_amount = customer_totals.max()

    # Print information about the largest spender
    print(f"Largest Spender ID: {largest_spender_id}")
    print(f"Total Purchase Amount: {largest_spender_amount:.2f}")

    # Record the end time
    end_time = time.time()

    # Calculate and print the time taken
    elapsed_time = end_time - start_time
    print(f'Time taken to find the largest spender: {elapsed_time:.2f} seconds')

    return largest_spender_id


if __name__ == "__main__":
    file_path = 'Data/Intuilize_MNSU_SampleSales_V1_011524.csv'
    customer_id_to_plot = 17314 # randomly selected

    plot_purchase_history(file_path, find_largest_spender(file_path))