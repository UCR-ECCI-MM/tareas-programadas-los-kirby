# Explicación Código Algoritmo Genético

## alg_genetico.py

Este código se encarga, mediante el algoritmo genético, de realizar predicciones sobre los precios de "stock" utilizando
un modelo de machine learning (MLPRegressor) y evalúa su
rendimiento con diferentes mercados.

```{py}
import pandas as pd
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
```

* pandas: Se utiliza para la manipulación y análisis de los archivos.
* train_test_split: Se utiliza para dividir los datos que van a ser probados.
* StandardScaler: Mejora la escalabilidad del modelo.
* MLPRegressor: Implementa la red neuronal.
* mean_absolute_error: Calcula la MAE entre los valores predecidos y los valores actuales.
* pygad: Utilizado para el algoritmo genético.
* random: Para la generación de números aleatorios
* time: Utilizado para medir los tiempos de ejecución.
* os: Operaciones con archivos y directorios.
* pyplot: Utilizado para los gráficos
* warnings.filterwarnings("ignore"): Suprime errores (en nuestro caso errores de convergencia)

```{py}
results_folder = 'results'
os.makedirs(results_folder, exist_ok=True)

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

        data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)
        data['Previous Close'] = data['Close/Last'].shift(1)
        data.dropna(inplace=True)

        window_size = 5
        X = data[['Previous Close']]
        y = data['Close/Last'].shift(-1)

        X = X[:-1]
        y = y[:-1]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
```

1. Se crea la carpeta para guardar los resultado y se obtiene
la carpeta de dónde queremos sacar los datos.

2. Se va a analizar todos los datos `.csv` dentro de la carpeta y se reemplazaran a formatos validos para ser leídos.

3. Luego se preprocesan los datos que van a ser entrenados. Revisar [fuerza bruta](../Fuerza_Bruta/README.md) para más información.

```{py}
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
```

Se define la función *fitness* que va a evaluar hiperparámetros y definir si
son óptimo o no.

Se entrena la red neuronal y retorna un MAE negativo, ya que el optimizador minimiza la función objetivo y lo que queremos es maximizarla.

```{py}
# Define the GA parameters
sol_per_pop = 10 # Number of solutions in a population
num_gen = 10     # Number of generations
num_genes = 3    # Number of hyperparameters to optimize
```

Definimos los parámetros para el algoritmo genético:

* Número de soluciones en la población.
* Número de generaciones.
* Número de genes (hiperparámetros a optimizar).

```{py}
hyperparameter_ranges = [
    [10, 100],    
    [100, 2000],  
    [0.0001, 0.1] 
]
```

Aquí definimos los rangos de los hiperparámetros:

1. Rango de la capa escondida.
2. Rando de iteraciones.
3. Rango de la tasa de aprendizaje.

```{py}
    # Create an initial solution (randomly selected hyperparameters within the defined ranges)
    def create_solution():
        return [
            random.randint(hyperparameter_ranges[0][0], hyperparameter_ranges[0][1]),  
            random.randint(hyperparameter_ranges[1][0], hyperparameter_ranges[1][1]),  
            random.uniform(hyperparameter_ranges[2][0], hyperparameter_ranges[2][1])   
        ]
    # Create the initial population
    population = [create_solution() for _ in range(sol_per_pop)]
```

Definimos una función que devuelve los 3 hiperparámetros aleatorios dentro de
el rango. `population` guarda `sol_per_pop` soluciones (10) como una lista.

```{py}
    # Create a callback function to introduce a delay after each generation
    def delay_after_generation(ga_instance):
        time.sleep(1) # Delay for 1 second after each generation
```

Se define un pequeño *delay* con la función de no sobrecargar el programa.

```{py}
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
```

Se crea el objeto del algoritmo genético y luego se corre.

1. num_generation = número de generaciones el cuál el algoritmo va a evolucionar.

2. num_parents_mating = número de padres (soluciones) que se utilizarán para reproducirse
y crear la próxima generacion.

3. fitness_func = función *fitness* utilizada para evaluar el rendimiento de cada
neurona.

4. sol_per_pop = cantidad de soluciones por población

5. num_genes = número de genes (hiperparámetros) por cada solución.

6. gene_type = indica el tipo de datos que son los hiperparámetros, es esto caso float.

7. gene_space = define los rangos posibles de los hiperparámetros. Definidos en
                `hyperparameter_ranges`.
8. parent_selection_type = método utilizado el cuál los padres van a ser elegidos.
                           Se utiliza `rank` para escoger las 5 mejores soluciones.
9. keep_parents = número de padres para mantener intactos para la próxima generación.
                  Se mantiene sólo 1.

10. crossover_type = especifica el tipo de crossover para aplicar entre padres.
                    Se utiliza "uniform" el cuál significa que se escogen los
                    genes de ambos padres aleatoriamente.

11. crossover_probability = probabilidad de un *crossover* entre dos padres
                           durante la reproducción.

12. mutation_type = tipo de mutación a aplicar, forma de introducir pequeños
                   cambios al gen para explorar todo el espacio minuciosamente.
                   Se utiliza *random*, los genes mutan aleatoriamente.

13. mutation_probability =  Probabilidad de que ocurra una mutación en un gen.

14. init_range_low = parte baja del rango para inicializar los genes de la
                     población.

15. init_range_high = parte alta del rango para inicializar los genes de la
                      población.

    NOTA: Estos rango son controlados por `gene_space` y no los parámetros del rango.

16. on_generation: Se toma la función de retraso.
                   En este caso es `delay_after_generation`.

Explicación de `ga_instance.run()`:

* Inicialización: El algoritmo inicializa la primer generación de la población
donde cada individuo se crea con los rangos específicos (`gene_space`).

* Se genera el ciclo dónde se realizan los siguientes pasos `num_generations`
cantidad de veces.

1. *Fitness*: Se realiza la evaluación `fitness_func`
2. Selección: Apartir del rendimiento de los individuos, se eligen los padres
por `rank`.
3. Cruce: Los padres pasan por el proceso de cruce, `crossover_probability`
determina si se realiza o no.
4. Mutación: Se realizan pequeños cambios con el proceso de mutación. Realizar
cambios o no los determina `mutation_probability`.
5. Próxima generación: Se crea la próxima generación tomando en cuenta
`keep_parents`. Se mantiene los que tengan el mejor rango y el resto pasan
por selección, cruce y mutación.

Después de cada generación se llama `on_generation`.
La mejor solución se va a encontrar en `ga_instance.run()`.

```{py}
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
```

Se sacan los resultados y se crea la red neuronal para realizar las
predicciones.

Luego se guarda el modelo, se crea el gráfico y se imprimen los resultados
del modelo.