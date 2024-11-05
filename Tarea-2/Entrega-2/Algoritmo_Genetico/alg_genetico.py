import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
import pygad
print(pygad.__version__)
import random
import time

# Load the data
data = pd.read_csv('../Large_Data/apple_large_data.csv')  # Change this to the actual path of your CSV file
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Clean data: Remove '$' and ',' from 'Close/Last' and convert to float
data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)
data['Previous Close'] = data['Close/Last'].shift(1)
data.dropna(inplace=True)

# Create a rolling window of the previous 5 days' closing prices (features for X)
window_size = 5
X = pd.DataFrame()

# for i in range(1, window_size + 1):
    # X[f'Prev_{i}'] = data['Close/Last'].shift(i)

X = data[['Previous Close']]

# Drop rows with NaN in X (resulting from the shift)
# X.dropna(inplace=True)

# Create the target y: the next day's closing price (shifted by -1)
y = data['Close/Last'].shift(-1)

# Now we need to align X and y
# After shifting, the last row of `y` and first rows of `X` have NaN, so drop the corresponding rows.
X = X[:-1]  # Drop the last row of X, because y is shifted by -1 (next day's value)
y = y[:-1]  # Drop the last row of y (because it's shifted up, and its corresponding X row has been dropped)

# Check if X and y have the same number of samples
print(f"X shape: {X.shape}, y shape: {y.shape}")  # Should be the same number of rows

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features (standardization)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def fitness_func(ga_instance, solution, solution_idx):
    # Correctly unpack the solution array
    hidden_layer_size = int(solution[0])   # Number of neurons in the hidden layer (int)
    max_iter = int(solution[1])             # Max iterations (int)
    learning_rate_init = solution[2]       # Learning rate (float)
    
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
sol_per_pop = 10  # Number of solutions in a population
num_gen = 10      # Number of generations
num_genes = 3     # Number of hyperparameters to optimize (hidden_layer_size, max_iter, learning_rate_init)

# Define the ranges for the hyperparameters
hyperparameter_ranges = [
    [10, 100],    # hidden_layer_sizes: number of neurons (between 10 and 100)
    [100, 2000],  # max_iter: number of iterations (between 100 and 2000)
    [0.0001, 0.1] # learning_rate_init: learning rate (between 0.0001 and 0.1)
]

# Create an initial solution (randomly selected hyperparameters within the defined ranges)
def create_solution():
    return [
        random.randint(hyperparameter_ranges[0][0], hyperparameter_ranges[0][1]),  # hidden_layer_sizes (int)
        random.randint(hyperparameter_ranges[1][0], hyperparameter_ranges[1][1]),  # max_iter (int)
        random.uniform(hyperparameter_ranges[2][0], hyperparameter_ranges[2][1])   # learning_rate_init (float)
    ]

# Create the initial population
population = [create_solution() for _ in range(sol_per_pop)]

# Create a callback function to introduce a delay after each generation
def delay_after_generation(ga_instance):
    time.sleep(1)  # Delay for 1 second after each generation

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

# Print the best solution and its fitness
print(f"Best Solution (Hyperparameters): {best_solution}")
print(f"Best Solution Fitness: {best_solution_fitness}")
print(f"Best Solution Index: {best_solution_idx}")

# Print the best solution and its fitness
print(f"Best Solution: {best_solution}")
print(f"Best Solution Fitness: {best_solution_fitness}")

# Print the best solution and its fitness
print(f"Best Solution: {best_solution}")
print(f"Best Solution Fitness (Negative MAE): {best_solution_fitness}")


print(f"Best Solution: {best_solution}")
print(f"Best Solution Fitness (Negative MAE): {best_solution_fitness}")

# Optionally, train the final model with the best hyperparameters
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
print(f"Final Model MAE: {final_mae}")

