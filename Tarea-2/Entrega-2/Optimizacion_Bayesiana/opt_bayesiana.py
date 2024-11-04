import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from bayes_opt import BayesianOptimization
import time

# Use Test code as a base (Tarea-2/Entrega-2/Test/testing.py)

# TODO: Iterate through all the CSV files in the Data folder and optimize the hyperparameters for each one

# Start time
start_time = time.time()

# Load the data
data = pd.read_csv('../Data/apple_historical_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Clean data 
data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)

# Use the previous close price as a feature
data['Previous Close'] = data['Close/Last'].shift(1) 
data.dropna(inplace=True)  # Delete empty values

# Define X and y (features and target)
X = data[['Previous Close']] 
y = data['Close/Last'].shift(-1)  # Predict the next day's close price
y = y[:-1]
X = X[:-1]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the function to optimize
def optimize_mlp(hidden_layer1, hidden_layer2, learning_rate, max_iter):
    # Create the model with the specified parameters
    model = MLPRegressor(
        hidden_layer_sizes=(int(hidden_layer1), int(hidden_layer2)),
        activation='relu',
        solver='adam',
        learning_rate_init=learning_rate,
        max_iter=int(max_iter),
        random_state=42
    )
    # Train the model
    model.fit(X_train, y_train)
    
    # Predict and calculate MAE on the test set
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    
    # Return the negative MAE as Bayesian optimization minimizes the objective function
    return -mae

# Define the parameter bounds
param_bounds = {
    'hidden_layer1': (8, 64),       # Range for the first hidden layer
    'hidden_layer2': (4, 32),       # Range for the second hidden layer
    'learning_rate': (0.001, 0.1),  # Range for the learning rate
    'max_iter': (200, 1000)         # Range for max iterations
}

# Run Bayesian Optimization
optimizer = BayesianOptimization(
    f=optimize_mlp,
    pbounds=param_bounds,
    random_state=42,
    verbose=2
)

# Perform the optimization
optimizer.maximize(init_points=5, n_iter=15)

# Get the best parameters
best_params = optimizer.max['params']
print("\nBest Hyperparameters found:")
print(best_params)

# Train the best model
best_model = MLPRegressor(
    hidden_layer_sizes=(int(best_params['hidden_layer1']), int(best_params['hidden_layer2'])),
    activation='relu',
    solver='adam',
    learning_rate_init=best_params['learning_rate'],
    max_iter=int(best_params['max_iter']),
    random_state=42
)
best_model.fit(X_train, y_train)

# Make predictions and show results
final_predictions = best_model.predict(X_test)

# Create a DataFrame to store the actual vs predicted values
results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': final_predictions
}, index=y_test.index)

print("\nActual vs Predicted Data:")
print(results)

# Measure the performance of the model
mae = mean_absolute_error(y_test, final_predictions)
accuracy = best_model.score(X_test, y_test)
print(f"MAE: {mae:.2f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

# Calculate execution time for each file
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time {execution_time:.4f} seconds")