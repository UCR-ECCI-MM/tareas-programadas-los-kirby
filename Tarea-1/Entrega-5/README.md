# Entrega 5

1. (20%) Implementación de la aplicación completa: entrega final con toda la
funcionalidad.

## Manual de Uso

Para compilar el lexer, parser y el GUI es necesario importar los siguientes paquetes y módulos al código:

- Para el análisis léxico:

        import ply.lex as lex

- Para leer el archivo XML de entrada:

        from pathlib import Path
  
- Para trabajar con expresiones regulares:

        import re

- Para el parser sintáctico:
    
        import ply.yacc as yacc

- Para la GUI: Tkinter (biblioteca estándar de Python)

        sudo apt-get install python3-tk

- Para los gráficos: NumPy

        pip install numpy


        pip install matplotlib

Para correr el programa y usar el GUI introduzca el siguiente comando en la terminal (dependiendo de la versión de Python instalada),
estando dentro de la carpeta [Tarea-1/Entrega-5/src:](Tarea-1/Entrega-5/src)

    python main.py

    python3 main.py

En el archivo `health_topics.txt` se muestran todos los datos que se guardaron en las estructuras de datos creadas.
