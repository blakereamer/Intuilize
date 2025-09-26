import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression #NOT USED
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
    df.insert(1, "Recency", 0.0)
    df.insert(2, "Frequency", 0.0)
    df.insert(3, "MonetaryValue", 0.0)
    df.insert(4, "CLV", 0.0)

    df.to_csv(file_path, index=False)
'''


class PurchasePredictor:
    def __init__(self, data, features):
        self.data = data
        self.features = features

    def preprocess_data(self):
        X = self.data[self.features]
        y_price = self.data['ExtPrice']  # Assuming 'ExtPrice' is the purchase price column
        y_date = pd.to_datetime(self.data['SalesDate']).astype('int64')
        return X, y_price, y_date

    def train_model(self, X, y_price, y_date):
        X_train, X_test, y_price_train, y_price_test, y_date_train, y_date_test = train_test_split(X, y_price, y_date, test_size=0.2, random_state=42)

        price_regressor = RandomForestRegressor(random_state=42)
        price_regressor.fit(X_train, y_price_train)

        date_regressor = RandomForestRegressor(random_state=42)
        date_regressor.fit(X_train, y_date_train)

        return price_regressor, date_regressor, X_test, y_price_test, y_date_test

    def evaluate_model(self, price_regressor, date_regressor, X_test, y_price_test, y_date_test):
        y_price_pred = price_regressor.predict(X_test)
        y_date_pred = date_regressor.predict(X_test)

        mse_price = mean_squared_error(y_price_test, y_price_pred)
        mse_date = mean_squared_error(y_date_test, y_date_pred)

        print("Mean Squared Error (Price):", mse_price)
        print("Mean Squared Error (Date):", mse_date)

    def predict(self, price_regressor, date_regressor, customer_code):
        # Get the features for the specified customer
        customer_features = self.data[self.data['CustomerCode'] == customer_code][self.features]

        # Predict the next purchase price and date for the customer
        next_purchase_price = price_regressor.predict(customer_features)
        next_purchase_date = date_regressor.predict(customer_features)

        return next_purchase_price, next_purchase_date
    
#TODO this is un-usable right now but it will be fixed once we create training data for it
def new_predictions():

    # Load your preprocessed data
    data = pd.read_csv("Data\\CustomerStats.csv")

    # Define features and target variables
    X = data[['Recency', 'Frequency', 'MonetaryValue', 'AvgPurchasePrice', 'AvgDaysBetweenOrders']]
    y_date = data['NextPurchaseDate']  # Next purchase date
    y_price = data['NextPurchasePrice']  # Next purchase price

    # Split data into training and testing sets
    X_train, X_test, y_date_train, y_date_test = train_test_split(X, y_date, test_size=0.2, random_state=42)
    X_train, X_test, y_price_train, y_price_test = train_test_split(X, y_price, test_size=0.2, random_state=42)

    # Train linear regression models
    model_date = LogisticRegression()
    model_date.fit(X_train, y_date_train)

    model_price = LogisticRegression()
    model_price.fit(X_train, y_price_train)

    # Make predictions
    predictions_date = model_date.predict(X_test)
    predictions_price = model_price.predict(X_test)

    # Evaluate models
    mae_date = mean_absolute_error(y_date_test, predictions_date)
    mse_date = mean_squared_error(y_date_test, predictions_date)
    rmse_date = mse_date ** 0.5

    mae_price = mean_absolute_error(y_price_test, predictions_price)
    mse_price = mean_squared_error(y_price_test, predictions_price)
    rmse_price = mse_price ** 0.5

    print("Date Prediction:")
    print(f"Mean Absolute Error: {mae_date}")
    print(f"Mean Squared Error: {mse_date}")
    print(f"Root Mean Squared Error: {rmse_date}")

    print("\nPrice Prediction:")
    print(f"Mean Absolute Error: {mae_price}")
    print(f"Mean Squared Error: {mse_price}")
    print(f"Root Mean Squared Error: {rmse_price}")

def main():

    df = pd.read_csv('Data\\CustomerStats.csv')

    # THIS IS USED FOR RFM_RANK
    # TODO: 'ProductGroup', 'ProductCode' Encode these 
    # Split features (X) and target variable (y)

    # Drop columns with NaN values
    df = df.dropna(axis=1)

    # Split features (X) and target variable (y)
    y = df['RFM_Rank']
    X = df.drop(columns=['LocationName', 'BranchName',
            'ProductGroup', 'ProductCode', 'CustomerName', 'SalesDate', 'RFM_Rank'])
    

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None, shuffle=True)

    # Train the model
    model = LogisticRegression()

    model.fit(X_train, y_train)

    # Evaluate the model
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)

    print('Accuracy of the classifier on the training set: {:.2f}'.format(train_accuracy))
    print('Accuracy of the classifier on the test set: {:.2f}'.format(test_accuracy))

    # Example of calculating mean squared error (MSE) for linear regression

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_mse = mean_squared_error(y_train, train_predictions)
    test_mse = mean_squared_error(y_test, test_predictions)

    print('Mean Squared Error (MSE) on the training set: {:.2f}'.format(train_mse))
    print('Mean Squared Error (MSE) on the test set: {:.2f}'.format(test_mse))
    
        # Compare predicted RFM ranks with actual RFM ranks
    train_comparison = pd.DataFrame({'Actual RFM Rank': y_train, 'Predicted RFM Rank': train_predictions})
    test_comparison = pd.DataFrame({'Actual RFM Rank': y_test, 'Predicted RFM Rank': test_predictions})

    print('\nComparison of Actual vs Predicted RFM Ranks for Training Set:')
    train_mismatch = train_comparison[train_comparison['Actual RFM Rank'] != train_comparison['Predicted RFM Rank']]
    print(train_mismatch)

    print('\nComparison of Actual vs Predicted RFM Ranks for Test Set:')
    test_mismatch = test_comparison[test_comparison['Actual RFM Rank'] != test_comparison['Predicted RFM Rank']]
    print(test_mismatch)


    '''
    file_path = 'Data\SampleDataCleaned.csv'

    data = pd.read_csv(file_path)

    predictor = PurchasePredictor(data, features=['SalesQty', 'UnitCost', 'UnitPrice', 'CustomerCode'])

    X, y_price, y_date = predictor.preprocess_data()

    price_regressor, date_regressor, X_test, y_price_test, y_date_test = predictor.train_model(X, y_price, y_date)

    predictor.evaluate_model(price_regressor, date_regressor, X_test, y_price_test, y_date_test)

    # Predict next purchase price and date for a specific customer
    customer_code = '17314'
    next_purchase_price, next_purchase_date = predictor.predict(price_regressor, date_regressor, customer_code)

    print("Predicted Next Purchase Price:", next_purchase_price)
    print("Predicted Next Purchase Date:", next_purchase_date)'''

if __name__ == "__main__":
    main()