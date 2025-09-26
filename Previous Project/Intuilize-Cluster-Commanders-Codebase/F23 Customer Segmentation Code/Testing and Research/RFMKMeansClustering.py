import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.cluster import KMeans
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import MaxAbsScaler, RobustScaler

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

def get_active_customers(df, Months):
    print("--------------------------------Active Customers Within Last 12 Months-----------------------------------")
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])
    
    
    max_sales_date = df['SalesDate'].max()
    
    twelve_months_ago = max_sales_date - pd.DateOffset(months=Months)
    active_customers_df = df[df['SalesDate'] >= twelve_months_ago]
    num_active_customers = active_customers_df['CustomerCode'].nunique()
    
    print(f'The number of active customers within the last 12 months is: {num_active_customers}')
    
    # Return the dataframe of active customers if needed
    return active_customers_df


def analyze_clusters(clustered_rfm_df):
    # Analyze each segment to understand customer characteristics
    segment_analysis = clustered_rfm_df.groupby('Cluster').mean()
    print("Segment Analysis:")
    print(segment_analysis)

def perform_rfm_analysis(active_customers_df):
    # Perform RFM analysis
    rfm_df = active_customers_df.groupby('CustomerCode').agg({
        'SalesDate': lambda date: (active_customers_df['SalesDate'].max().date() - date.max().date()).days,
        'InvoiceNumber': 'nunique',
        'ExtPrice': 'sum'
    }).reset_index()

    # Rename columns
    rfm_df.columns = ['CustomerCode', 'Recency', 'Frequency', 'MonetaryValue']

    print(rfm_df.head(5))

    return rfm_df

def perform_kmeans_clustering(rfm_df):
    # Standardize the RFM features
    scaler = MaxAbsScaler()
    X_scaled = scaler.fit_transform(rfm_df)
    
    # Perform KMeans clustering
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(X_scaled)
    
    # Add cluster labels to the RFM dataframe
    rfm_df['Cluster'] = kmeans.labels_
    
    return rfm_df


def visualize_clusters(clustered_rfm_df):
    # Plot the clusters based on RFM features
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Recency', y='Frequency', hue='Cluster', data=clustered_rfm_df, palette='viridis', legend='full')
    plt.title('RFM Clusters')
    plt.xlabel('Recency')
    plt.ylabel('Frequency')
    plt.show()

def visualize_clusters_customers(clustered_rfm_df):
    # Plot each customer point based on RFM features
    plt.figure(figsize=(10, 6))
    for index, row in clustered_rfm_df.iterrows():
        plt.scatter(row['Recency'], row['Frequency'], color=plt.cm.viridis(row['Cluster'] / max(clustered_rfm_df['Cluster'])), alpha=0.5)
    plt.title('RFM Clusters')
    plt.xlabel('Recency')
    plt.ylabel('Frequency')
    plt.show()


def visualize_clusters_3D(clustered_rfm_df):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Scatter plot
    ax.scatter(clustered_rfm_df['Recency'], clustered_rfm_df['Frequency'], clustered_rfm_df['MonetaryValue'], c=clustered_rfm_df['Cluster'], cmap='viridis')

    # Set labels and title
    ax.set_xlabel('Recency')
    ax.set_ylabel('Frequency')
    ax.set_zlabel('Monetary Value')
    ax.set_title('RFM Clusters')

    # Show plot
    print('Yo HERE IS THE MIN MONETARY VALUE' , min(clustered_rfm_df['MonetaryValue']))
    plt.show()


def customer_lifetime_value(df):
    # Calculate total revenue per customer
    revenue_per_customer = df.groupby('CustomerCode')['ExtPrice'].sum()

    # Calculate the average lifespan of a customer (in months)
    # Assuming lifespan is calculated based on the difference between the first and last transaction dates
    lifespan_per_customer = df.groupby('CustomerCode')['SalesDate'].agg(['min', 'max'])
    lifespan_per_customer['Lifespan'] = (lifespan_per_customer['max'] - lifespan_per_customer['min']).dt.days / 30
    
    # Filter out customers with zero lifespans (AKA They only purchased once.)
    lifespan_per_customer = lifespan_per_customer[lifespan_per_customer['Lifespan'] > 0]

    # Calculate CLV as the product of average revenue per month and lifespan
    clv = (revenue_per_customer / lifespan_per_customer['Lifespan']).fillna(0)

    # Update the original DataFrame with CLV values
    df['CLV'] = df['CustomerCode'].map(clv)




def main():
    #Intuilize_MNSU_SampleSales_V1_011524 - Intuilize_SampleSales_V1_011524.csv
    file_path = 'Data/SampleDataCleaned.csv'

    # Read the Excel file with Pandas
    df = pd.read_csv(file_path)

    get_active_customers(df, 12)


    # Convert the date column to datetime format
    df['SalesDate'] = pd.to_datetime(df['SalesDate'])
    df_2023 = df[(df['SalesDate'] >= '2023-01-01') & (df['SalesDate'] <= '2023-12-31')] 
    df_2023['SalesDate'].sort_values()
    
    # Get active customers within the last 12 months
    active_customers_df = get_active_customers(df_2023, 3)
    
    # Perform RFM analysis on active customers
    rfm_df = perform_rfm_analysis(active_customers_df)
    
    new_file_path = 'Data/RFM_Analyzed_Data.csv'  
    rfm_df.to_csv(new_file_path, index=False)

    # Perform KMeans clustering on RFM features
    clustered_rfm_df = perform_kmeans_clustering(rfm_df)
    
    # Analyze clusters and prioritize customers within each segment
    analyze_clusters(clustered_rfm_df)

    # Visualize clusters
    visualize_clusters(clustered_rfm_df)
    visualize_clusters_customers(clustered_rfm_df)
    visualize_clusters_3D(clustered_rfm_df)

    group = clustered_rfm_df.groupby(['Cluster'])[['Recency','Frequency','MonetaryValue']].mean()
    group

    #TODO Create a 'Impact' column that shows the impact of the customers spending over the total GP


    
if __name__ == "__main__":
    main()