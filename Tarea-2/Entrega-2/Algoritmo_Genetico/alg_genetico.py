import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import pygad
import random
import time
import os
import matplotlib.pyplot as plt
import joblib
import warnings
warnings.filterwarnings("ignore")

# Create directories for results and future predictions csv files
results_folder = 'results'
os.makedirs(results_folder, exist_ok=True)

# Process each CSV file in the LargeData folder
data_folder = '../Small_Data'
for file_name in os.listdir(data_folder):
    if file_name.endswith('.csv'):
        print(f"Processing file: {file_name}")
        # Start time for each file
        start_time = time.time()
        # Load the data
        file_path = os.path.join(data_folder, file_name)
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Clean data: Remove '$' and ',' from 'Close/Last' and convert to float
        data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)
        data['Previous Close'] = data['Close/Last'].shift(1)
        data.dropna(inplace=True)

        # Create a rolling window of the previous 5 days' closing prices (features for X)
        window_size = 5
        X = data[['Previous Close']]

        # Create the target y: the next day's closing price (shifted by -1)
        y = data['Close/Last'].shift(-1)

        # Now we need to align X and y
        X = X[:-1]  # Drop the last row of X, because y is shifted by -1 (next day's value)
        y = y[:-1]  # Drop the last row of y (because it's shifted up, and its corresponding X row has been dropped)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale the features (standardization)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        def fitness_func(ga_instance, solution, solution_idx):
            # Correctly unpack the solution array
            hidden_layer_size = int(solution[0])   
            max_iter = int(solution[1])            
            learning_rate_init = solution[2]       
            # Create and train the MLPRegressor model with the given hyperparameters
            model = MLPRegressor(hidden_layer_sizes=(hidden_layer_size,), 
                                 max_iter=max_iter, 
                                 learning_rate_init=learning_rate_init, 
                                 random_state=42)
            
            model.fit(X_train, y_train)
            # Evaluate the model on the test set
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            # Return the negative MAE (since GA tries to maximize the fitness function)
            return -mae
        # Define the GA parameters
        sol_per_pop = 10 # Number of solutions in a population
        num_gen = 10     # Number of generations
        num_genes = 3    # Number of hyperparameters to optimize (hidden_layer_size, max_iter, learning_rate_init)

        hyperparameter_ranges = [
            [10, 100],    
            [100, 2000],  
            [0.0001, 0.1] 
        ]

        # Create an initial solution (randomly selected hyperparameters within the defined ranges)
        def create_solution():
            return [
                random.randint(hyperparameter_ranges[0][0], hyperparameter_ranges[0][1]),  
                random.randint(hyperparameter_ranges[1][0], hyperparameter_ranges[1][1]),  
                random.uniform(hyperparameter_ranges[2][0], hyperparameter_ranges[2][1])   
            ]
        # Create the initial population
        population = [create_solution() for _ in range(sol_per_pop)]
        
        # Create a callback function to introduce a delay after each generation
        def delay_after_generation(ga_instance):
            time.sleep(1) # Delay for 1 second after each generation

        # Set up the genetic algorithm
        ga_instance = pygad.GA(
            num_generations=num_gen,
            num_parents_mating=5,           # Number of parents to mate
            fitness_func=fitness_func,      # The fitness function to optimize
            sol_per_pop=sol_per_pop,        # Number of solutions (individuals) per population
            num_genes=num_genes,            # Number of genes in each solution (hyperparameters)
            gene_type=float,                # The type of each gene (float for learning rate, int for others)
            gene_space=hyperparameter_ranges,  # The ranges for each hyperparameter
            parent_selection_type="rank",   # Selection method
            keep_parents=1,                 # Number of parents to keep for the next generation
            crossover_type="uniform",       # Crossover type
            crossover_probability=0.7,      # Crossover probability
            mutation_type="random",         # Mutation type
            mutation_probability=0.2,       # Mutation probability
            init_range_low=0,               # Lower bound for initial population
            init_range_high=1,               # Upper bound for initial population
            on_generation=delay_after_generation
        )
        # Run the genetic algorithm optimization
        ga_instance.run()
        # Get the best solution and its fitness (best_solution() returns a tuple)
        # Unpack the result into three variables
        best_solution, best_solution_fitness, best_solution_idx = ga_instance.best_solution()
        # Train the final model with the best hyperparameters
        best_hidden_layer_sizes = (int(best_solution[0]),)
        best_max_iter = int(best_solution[1])
        best_learning_rate_init = best_solution[2]

        final_model = MLPRegressor(hidden_layer_sizes=best_hidden_layer_sizes, 
                                   max_iter=best_max_iter, 
                                   learning_rate_init=best_learning_rate_init, 
                                   random_state=42)
        final_model.fit(X_train, y_train)
        # Evaluate the final model on the test set
        y_pred_final = final_model.predict(X_test)
        final_mae = mean_absolute_error(y_test, y_pred_final)
        # print(f"Final Model MAE for {file_name}: {final_mae}")

        # Save the results to CSV and plot the actual vs predicted values
        results = pd.DataFrame({
            'Actual': y_test,
            'Predicted': y_pred_final
        }, index=y_test.index).sort_index(ascending=False)

        results_file_path = os.path.join(results_folder, f'results_{file_name}')
        results.to_csv(results_file_path)

        plt.figure(figsize=(12, 6))
        plt.plot(results.index, results['Actual'], label='Actual', color='blue')
        plt.plot(results.index, results['Predicted'], label='Predicted', color='orange')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.legend()
        plt.title(f'Genetic Algorithm - Actual vs Predicted Close Price (Genetic Algorithm) - {file_name}')
        plot_file_path = os.path.join(results_folder, f'plot_{file_name}.png')
        plt.savefig(plot_file_path)
        plt.close()

        # Calculate execution time for each file
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time for {file_name}: {execution_time:.4f} seconds")

        # Save the final model to a file
        model_file_path = os.path.join(results_folder, f'final_model_{file_name}.pkl')
        joblib.dump(final_model, model_file_path)
        print(f"Final model saved for {file_name} to: {model_file_path}")
        print(f"Best Solution Fitness for {file_name}: {best_solution_fitness}")
        print(f"Best Solution (Hyperparameters) for {file_name}: {best_solution}")
        print(f"Best Solution Index for {file_name}: {best_solution_idx}")
print("All files processed :D")