import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import time
import os
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

# Warnings de no convergencia aparecen en la consola, pero no afectan el resultado final ya que al final encuentra la solución más óptima

# Use Test code as a base (Tarea-2/Entrega-2/Test/testing.py)

# Define the path where your CSV files are located
data_folder = '../Large_Data/' # Change folder depending on size of data wanted to test
csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

# Create directories for results and future predictions csv files
results_folder = 'results'
future_predictions_folder = 'future_predictions'
os.makedirs(results_folder, exist_ok=True)
os.makedirs(future_predictions_folder, exist_ok=True)

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

    # Sort results by date in descending order
    results = results.sort_index(ascending=False)

    # Save the results to a CSV file in the results folder
    results_file_path = os.path.join(results_folder, f'results_{csv_file}')
    results.to_csv(results_file_path)
    
    # Plotting the Actual vs Predicted values
    plt.figure(figsize=(12, 6))
    plt.plot(results.index, results['Actual'], label='Actual', color='blue')
    plt.plot(results.index, results['Predicted'], label='Predicted', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    plt.title(f'Brute Force - Actual vs Predicted Close Prices for {csv_file}')
    
    # Save the plot in the results folder
    plot_file_path = os.path.join(results_folder, f'actual_vs_predicted_{csv_file}.png')
    plt.savefig(plot_file_path)
    plt.close()  # Close the plot to free memory

    # Calculate execution time for each file
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time for {csv_file}: {execution_time:.4f} seconds")

    import joblib

    # Save the best model to a file
    model_file_path = os.path.join(results_folder, f'model_{csv_file}.pkl')
    joblib.dump(best_model, model_file_path)

    print(f"Model saved to {model_file_path}")