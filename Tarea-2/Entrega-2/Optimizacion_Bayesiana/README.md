# Explicación Código

## opt_bayesiana.py

Este código se encarga, mediante la optimización bayesiana, de realizar predicciones sobre los precios de "stock" utilizando
un modelo de machine learning (MLPRegressor) y evalúa su
rendimiento con diferentes mercados.

```{py}
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from bayes_opt import BayesianOptimization
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
* BayesianOptimization: Utilizado para realizar afinamiento de hiperparámetros.
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

Estos valores se utilizan para que el modelo comprenda la relación entre `Previous Close` y `Close/Last` y así predecir el `Close/Last` del próximo día.

Por último se elimina la última fila de `X` y `Y` para alinear la predicción con los datos disponibles.

```{py}
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

Se dividen los datos, un 80% para entrenar y el 20% para pruebas.
Se mejora la X utilizando `StandardScaler` para obtener un rango estándar de las características de escalabilidad.

```{py}
def optimize_mlp(hidden_layer1, hidden_layer2, learning_rate, max_iter):
    model = MLPRegressor(
        hidden_layer_sizes=(int(hidden_layer1), int(hidden_layer2)),
        activation='relu',
        solver='adam',
        learning_rate_init=learning_rate,
        max_iter=int(max_iter),
        random_state=42
    )
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    return -mae
```

Esta función existe con el propósito de definir el modelo y la métrica (MAE) para
optimización.

Esta función toma como parámetros:

* hidden_layer1 = capa escondida 1 de la red neuronal
* hidden_layer2 = capa escondida 2 de la red neuronal
* learning_rate = tasa de aprendizaje
* max_iter = número máximo de iteraciones

El valor de retorno (MAE) se devuelve negativo ya que el optimizador minimiza
la función objetivo.

```{py}
param_bounds = {
    'hidden_layer1': (8, 64),
    'hidden_layer2': (4, 32),
    'learning_rate': (0.001, 0.1),
    'max_iter': (200, 1000)
}

optimizer = BayesianOptimization(
    f=optimize_mlp,
    pbounds=param_bounds,
    random_state=42,
    verbose=2
)
optimizer.maximize(init_points=5, n_iter=15)
```

Se realiza la configuración para la Optimización Bayesiana:

* param_bounds = se definen los rangos de los hiperparámetros a optimizar

    1. hidden_layer1 = primera dupla de neuronas
    2. hidden_layer2 = segunda dupla de neuronas
    3. learning_rate = tasa de aprendizaje
    4. rango de iteraciones

* optimizar = inicializa el optimizador

    1. f = función de optimización (`optimize_mp`)
    2. pbounds = hiperparámetros
    3. random_state = semilla para números aleatorios.

Por último se corre la función `maximize` el cual ejecuta la optimización
bayesiana con:

* init_points = cantidad de inicializaciones aleatorias
* n_iter = número de iteraciones

```{py}
best_params = optimizer.max['params']
best_model = MLPRegressor(
    hidden_layer_sizes=(int(best_params['hidden_layer1']), int(best_params['hidden_layer2'])),
    activation='relu',
    solver='adam',
    learning_rate_init=best_params['learning_rate'],
    max_iter=int(best_params['max_iter']),
    random_state=42
)
best_model.fit(X_train, y_train)
```

Tras haber encontrado los mejores hiperparámetros, se entrena el mejor modelo.

```{py}
final_predictions = best_model.predict(X_test)
results = pd.DataFrame({
    'Actual': y_test,
    'Predicted': final_predictions
}, index=y_test.index)
```

Con el mejor modelo, realizamos las predicciones con los datos que queremos.

```{py}
results = results.sort_index(ascending=False)
results_file_path = os.path.join(results_folder, f'results_{csv_file}')
results.to_csv(results_file_path)

plt.figure(figsize=(12, 6))
plt.plot(results.index, results['Actual'], label='Actual', color='blue')
plt.plot(results.index, results['Predicted'], label='Predicted', color='orange')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title(f'Actual vs Predicted Close Prices for {csv_file}')
plot_file_path = os.path.join(results_folder, f'actual_vs_predicted_{csv_file}.png')
plt.savefig(plot_file_path)
plt.close()

mae = mean_absolute_error(y_test, final_predictions)
accuracy = best_model.score(X_test, y_test)
print(f"MAE: {mae:.2f}")
print(f"Accuracy: {accuracy * 100:.2f}%")

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time {execution_time:.4f} seconds")

import joblib
model_file_path = os.path.join(results_folder, f'model_{csv_file}.pkl')
joblib.dump(best_model, model_file_path)
print(f"Model saved to {model_file_path}")
```

1. Resultados son guardados.
2. Se crea un gráfico con las comparaciones.
3. Se imprime el rendimiento del modelo.
4. Se guarda el modelo.
