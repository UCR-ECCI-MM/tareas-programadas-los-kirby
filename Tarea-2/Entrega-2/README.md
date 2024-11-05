# Manual de uso y Bibliotecas a instalar

## General

Para activar un ambiente virtual de Python:

```bash
sudo apt install python3.8-venv
python3 -m venv myenv
source myenv/bin/activate
```

## Bibliotecas NumPy, Scikit-Learn, Pandas, Bayesian-Optimization y Matplotlib:

```bash
python -m pip install ipython numpy matplotlib scikit-learn pandas bayesian-optimization
```

## Fuerza Bruta

Dentro de la carpeta `Tarea-2/Entrega-2`

```bash
cd Fuerza_Bruta
python3 fuerza_bruta.py
```
## Optimización Bayesiana

Dentro de la carpeta `Tarea-2/Entrega-2`

```bash
cd Optimizacion_Bayesiana
python3 opt_bayesiana.py
```

## Algoritmo Genético

Dentro de la carpeta `Tarea-2/Entrega-2`

```bash
cd Algoritmo_Genetico
python3 alg_genetico.py
```

## Datos obtenidos

Los datos históricos fueron obtenidos de la siguiente página: [Nasdaq](https://www.nasdaq.com/market-activity/stocks/)

## Explicación de carpetas

1. `Fuerza_Bruta`, `Optimizacion_Bayesiana` y `Algoritmo_Genetico` son las carpetas base en donde se encontrarán los programas **.py** y los resultados de las predicciones.

Dentro de estas carpetas, se encuentran las siguientes subcarpetas:

- `results`: Contiene los resultados predecidos de los datos actuales, es decir, en base a los datos históricos predice los precios para el día siguiente, y los gráficos comparando estas predicciones con los precios reales.

- `future_plots`: Contiene los gráficos de los datos históricos y la continuación con los precios futuros predecidos.

- `future_predictions`: Contiene los resultados predecidos de datos futuros no existentes, toma como base los datos históricos y predice los precios para Noviembre y Diciembre del 2024, y del año 2025. Únicamente se utilizan los datos grandes de entrada para una mejor predicción.

2. `Small_Data`, `Medium_Data` y `Large_Data` son los datos de entrada de diferentes tamaños para alimentar el modelo de red neuronal y para comparar su rendimiento y eficacia dependiendo del tamaño de entrada.

3. `Test` contiene un programa **.py** con la base de la red neuronal.

4. `Comparaciones` contiene un **README.md** detallado comparando diferentes aspectos con respecto a la red neuronal y las 3 técnicas utilizadas para la configuración de hiperparámetros.