import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error

# Load the data
data = pd.read_csv('apple_historical_data.csv')
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

# Define training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define and train the model
model = MLPRegressor(hidden_layer_sizes=(16, 8), activation='relu', solver='adam', max_iter=500, learning_rate_init=0.01)
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Dataframe to store the results
results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': predictions
}, index=y_test.index)

print("Actual vs Predicted Data:")
print(results)

# Measure the performance of the model
mae = mean_absolute_error(y_test, predictions)
accuracy = model.score(X_test, y_test)
print(f"MAE: {mae:.2f}")
print(f"Accuracy:  {accuracy * 100:.2f}%")
