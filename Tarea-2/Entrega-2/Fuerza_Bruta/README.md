# Explicación Código

## fuerza_bruta.py

Este código se encarga, mediante fuerza bruta, de realizar predicciones sobre los precios de "stock" utilizando
un modelo de machine learning (MLPRegressor) y evalúa su
rendimiento con diferentes mercados.

```{py}
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
```

* pandas: Se utiliza para la manipulación y análisis de los archivos.
* train_test_split: Se utiliza para dividir los datos que van a ser probados.
* StandardScaler: Mejora la escalabilidad del modelo.
* MLPRegressor: Implementa la red neuronal.
* mean_absolute_error: Calcula la MAE entre los valores predecidos y los valores actuales.
* time: Utilizado para medir los tiempos de ejecución.
* os: Operaciones con archivos y directorios.
* pyplot: Utilizado para los gráficos
* warnings.filterwarnings("ignore"): Suprime errores (en nuestro caso errores de convergencia)

```{py}
data_folder = '../Large_Data/' 
csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]

results_folder = 'results'
future_predictions_folder = 'future_predictions'
os.makedirs(results_folder, exist_ok=True)
os.makedirs(future_predictions_folder, exist_ok=True)
```

En esta sección se define la carpeta en los cuales están los datos que queremos analizar y localiza sólo aquellos con `.csv`. Después de eso se crean carpetas que van a contener los resultados finales.

```{py}
hidden_layer_options = [(16, 8), (32, 16), (64, 32)]
learning_rate_options = [0.001, 0.01, 0.1]
max_iter_options = [200, 500, 1000]
```

Aquí se definen los hiperparámetros:

1. hidden_layer_options: Una red neuronal consiste de múltiples capas de neuronas:

    * Capa de entrada -> Los datos entrantes para el modelo
    * Capa escondida  -> Dónde el modelo aprende patrones
    * Capa de salida  -> Las predicciones del modelo

    Aquí nosotros definimos un triplete de duplas para las dos diferentes capas escondidas que hay en el modelo, cada vez incrementando la cantidad de neuronas. Esto  para que se de un buen ajuste del modelo en caso de que existan pocos datos o muchos datos.

2. learning_rate_options: Este triplete controla la velocidad y el peso de cambia que va a tener el modelo en cada iteración. Entre más pequeño más preciso va a ser, pero va a requerir más iteraciones. Entre más grande puede diverger e incluso calcular mal la solución óptima, pero será más rápida. `0.01` es un buen medio el cuál balancea una buena velocidad de convergencia y estabilidad.

3. max_iter_options: Triplete definido con la cantidad de iteraciones máximas a realizar.

```{py}
for csv_file in csv_files:
    print(f"\nProcessing file: {csv_file}")
    start_time = time.time()
```

Ciclo para procesar todos los archivos definidos anteriormente. Se tomará el tiempo de ejecución de cada archivo.

```{py}
data = pd.read_csv(os.path.join(data_folder, csv_file))
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

data['Close/Last'] = data['Close/Last'].replace({'\$': '', ',': ''}, regex=True).astype(float)
data['Previous Close'] = data['Close/Last'].shift(1)
data.dropna(inplace=True)
```

* Archivos son cargados al DataFrame de `pandas`.
* Se convierte la columna al formato de `datetime`.
* Limpia la columna de `Close/Last` para que sean números flotantes.
* Se crea una columna `Previous Close` con un `shift` de la columna `Close/Last`. El `shift` mueve para abajo la columna.
* Borrar columnas que no tengan o les falten datos.

```{py}
X = data[['Previous Close']]
y = data['Close/Last'].shift(-1)
y = y[:-1]
X = X[:-1]
```

* X = `Previous Close`, va a ser utilizado para entrenar el modelo.
* Y = `Close/Last`, también utilizado para entrenar el modelo.

Estos valores se utilizan para que el modelo comprenda la relación entre `Previous Close` y `Close/Last`, y así predecir el `Close/Last` del próximo día.

Por último se elimina la última fila de `X` y `Y` para alinear la predicción con los datos disponibles.

```{py}
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

Divide los datos para entrenar el 80% y el 20% para pruebas.
Se mejora la X utilizando `StandardScaler` para obtener un rango estándar de las características de escalabilidad.

```{py}
best_mae = float('inf')
best_params = {}
best_model = None
for hidden_layers in hidden_layer_options:
    for learning_rate in learning_rate_options:
        for max_iter in max_iter_options:
            model = MLPRegressor(hidden_layer_sizes=hidden_layers, 
                                 activation='relu', 
                                 solver='adam', 
                                 learning_rate_init=learning_rate, 
                                 max_iter=max_iter,
                                 random_state=42)
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mae = mean_absolute_error(y_test, predictions)
            if mae < best_mae:
                best_mae = mae
                best_params = {
                    'hidden_layers': hidden_layers,
                    'learning_rate': learning_rate,
                    'max_iter': max_iter
                }
                best_model = model
```

Se va a iterar por todos los `hidden_layer_options`, `learning_rate_options` and `max_iter_options` así utilizando MAE para encontrar el mejor modelo. Este método se le llama fuerza bruta.

Para cada iteración se crea un modelo, estos son los parámetros nuevos que se utilizan:

* activation: especifíca la función de activación que va a ser utilizado por las neuronas. Aquí se utiliza la `relu` (Rectified Linear Unit). Se usa para dejar pasar salidas sólo positivas o 0.

* solver: se utiliza para encontrar los pesos dela red neuronal. Se utiliza `adam` el cuál ajusta basado en información de gradiente pasada.

* random_state: se define una sola semilla ya que la generación de números "muy aleatorios podrían perjudicar los resultados y la función optima.

Para las funciones:

* fit(): se utiliza para entrenar el modelo, así ajustando pesos y minimizando el error entre las predicciones y valores actuales.

* prediction(): realiza las predicciones utilizando el modelo entrenado. Toma nuevos datos de entrada `X_test` y genera las predicciones al valor objetivo `y_test`.

```{py}
accuracy = best_model.score(X_test, y_test)
print(f"Best Model for {csv_file}:")
print(f"Hidden Layers: {best_params['hidden_layers']}")
print(f"Learning Rate: {best_params['learning_rate']}")
print(f"Max Iterations: {best_params['max_iter']}")
print(f"Best MAE: {best_mae:.4f}")
print(f"Accuracy: {accuracy * 100:.2f}%")
```

Los resultados del modelo son impresos, se guardan.

```{py}
final_predictions = best_model.predict(X_test)
results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': final_predictions
}, index=y_test.index)
results = results.sort_index(ascending=False)
results_file_path = os.path.join(results_folder, f'results_{csv_file}')
results.to_csv(results_file_path)
```

Se hacen las predicciones con los datos que queríamos utilizando el mejor modelo encontrado y se guardan.

```{py}
plt.figure(figsize=(12, 6))
plt.plot(results.index, results['Actual'], label='Actual', color='blue')
plt.plot(results.index, results['Predicted'], label='Predicted', color='orange')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.title(f'Actual vs Predicted Close Prices for {csv_file}')
plot_file_path = os.path.join(results_folder, f'actual_vs_predicted_{csv_file}.png')
plt.savefig(plot_file_path)
plt.close()
```

Se crea el gráfico.

```{py}
execution_time = end_time - start_time
print(f"Execution time for {csv_file}: {execution_time:.4f} seconds")
```

Se calcula el tiempo de ejecución de cada archivo.

```{py}
    import joblib

    # Save the best model to a file
    model_file_path = os.path.join(results_folder, f'model_{csv_file}.pkl')
    joblib.dump(best_model, model_file_path)

    print(f"Model saved to {model_file_path}")
```
