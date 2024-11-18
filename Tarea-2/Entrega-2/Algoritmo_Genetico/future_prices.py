import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Same code as in Tarea-2/Entrega-2/Fuerza_Bruta/future_prices.py

# Path to the directory containing the CSV files and models
data_folder = '../Large_Data'  # Folder containing the CSV files
model_folder = 'results/Models'  # Folder containing the models
output_folder = 'future_predictions'  # Folder to save future predictions
plot_folder = 'future_plots'  # Folder to save plots of historical and future prices

# Create the output and plot folders if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(plot_folder, exist_ok=True)

# Loop through all CSV files in the data folder
for csv_file in os.listdir(data_folder):
    if csv_file.endswith('.csv'):
        # Load the corresponding model for the CSV file
        model_file_path = os.path.join(model_folder, f'final_model_{csv_file}.pkl')
        model = joblib.load(model_file_path)

        # Load the data from the CSV file
        data_file_path = os.path.join(data_folder, csv_file)
        data = pd.read_csv(data_file_path)

        data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y')
        data.set_index('Date', inplace=True)

        data = data.sort_index().drop_duplicates()

        # Check if the data contains dates from 2015 to 2024
        if data.index.min() > pd.Timestamp('2015-01-01') or data.index.max() < pd.Timestamp('2024-10-31'):
            print(f"Not enough data for {csv_file}. Skipping...")
            continue

        # Filter data for the range 2015-2024
        data_2020_2024 = data.loc['2015-01-01':'2024-10-31'].copy()

        # Prepare the data for prediction
        data_2020_2024['Previous Close'] = data_2020_2024['Close/Last'].replace({'\$': '', '': '0'}, regex=True).astype(float).shift(1)
        data_2020_2024.dropna(inplace=True)

        # Scale the data using the same scaler used in the training
        scaler = StandardScaler()
        X_future = scaler.fit_transform(data_2020_2024[['Previous Close']])

        # Predict future values for 2025 using the model
        future_dates = pd.date_range(start='2024-11-01', periods=365, freq='B')  # 365 business days in 2025
        future_predictions = model.predict(X_future[-365:])

        # Create a DataFrame for future predictions
        future_predictions_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Predicted Close'])

        # Save the future predictions to a CSV file
        future_predictions_file_path = os.path.join(output_folder, f'future_predictions_{os.path.splitext(csv_file)[0]}_2025.csv')
        future_predictions_df.to_csv(future_predictions_file_path)

        # Plot historical and future predicted prices
        plt.figure(figsize=(12, 6))
        plt.plot(data.index, data['Close/Last'].replace({'\$': '', '': '0'}, regex=True).astype(float), label='Historical Close', color='blue')
        plt.plot(future_predictions_df.index, future_predictions_df['Predicted Close'], label='Predicted Close', color='orange', linestyle='--')
        plt.title(f'Genetic Algorithm - Historical and Predicted Closing Prices for {os.path.splitext(csv_file)[0]}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid()
        plt.tight_layout()

        # Save the plot as a PNG file
        plot_file_path = os.path.join(plot_folder, f'plot_{os.path.splitext(csv_file)[0]}_2025.png')
        plt.savefig(plot_file_path)
        plt.close()  # Close the plot to free memory

        print(f"Future predictions for {csv_file} saved successfully and plotted.")

