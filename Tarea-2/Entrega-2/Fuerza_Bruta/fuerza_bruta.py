import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import time
import os

# Use Test code as a base (Tarea-2/Entrega-2/Test/testing.py)

# Define the path where your CSV files are located
data_folder = '../Data/'
csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

# Define hyperparameters to test
hidden_layer_options = [(16, 8), (32, 16), (64, 32)]
learning_rate_options = [0.001, 0.01, 0.1]
max_iter_options = [200, 500, 1000]

# Loop through each CSV file
for csv_file in csv_files:
    print(f"\nProcessing file: {csv_file}")
    
    # Start time for each file
    start_time = time.time()
    
    # Load the data
    data = pd.read_csv(os.path.join(data_folder, csv_file))
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Clean data
    data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    # Use the previous close price as a feature
    data['Previous Close'] = data['Close/Last'].shift(1)
    data.dropna(inplace=True)  # Delete empty values

    # Define X and y
    X = data[['Previous Close']]
    y = data['Close/Last'].shift(-1)
    y = y[:-1]
    X = X[:-1]

    # Define training and testing data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Variables to store the best model
    best_mae = float('inf')
    best_params = {}
    best_model = None

    # Brute force search for the best model
    for hidden_layers in hidden_layer_options:
        for learning_rate in learning_rate_options:
            for max_iter in max_iter_options:
                # Define and train the model
                model = MLPRegressor(hidden_layer_sizes=hidden_layers, 
                                     activation='relu', 
                                     solver='adam', 
                                     learning_rate_init=learning_rate, 
                                     max_iter=max_iter,
                                     random_state=42)
                model.fit(X_train, y_train)
                
                # Predict and measure the performance with MAE
                predictions = model.predict(X_test)
                mae = mean_absolute_error(y_test, predictions)
                
                # Update the best model if found
                if mae < best_mae:
                    best_mae = mae
                    best_params = {
                        'hidden_layers': hidden_layers,
                        'learning_rate': learning_rate,
                        'max_iter': max_iter
                    }
                    best_model = model
    accuracy = best_model.score(X_test, y_test)

    # Print the best model parameters and results for the current CSV
    print(f"Best Model for {csv_file}:")
    print(f"Hidden Layers: {best_params['hidden_layers']}")
    print(f"Learning Rate: {best_params['learning_rate']}")
    print(f"Max Iterations: {best_params['max_iter']}")
    print(f"Best MAE: {best_mae:.4f}")
    print(f"Accuracy: {accuracy * 100:.2f}%")

    # Make predictions and display results in a DataFrame
    final_predictions = best_model.predict(X_test)
    results = pd.DataFrame({
        'Actual': y_test,
        'Predicted': final_predictions
    }, index=y_test.index)

    print("\nActual vs Predicted Data:")
    print(results)

    # Calculate execution time for each file
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for {csv_file}: {execution_time:.4f} seconds")
