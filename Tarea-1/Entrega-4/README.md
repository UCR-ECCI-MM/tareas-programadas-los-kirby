# Entrega 4

1. Creación dinámica de los objetos o las estructuras de datos: a la entrega
anterior, se le agrega la capacidad de crear dinámicamente los objetos o
estructuras necesarias para la aplicación.

## Manual de Uso

Para compilar el lexer y parser es necesario importar los siguientes paquetes y módulos al código:

- Para el análisis léxico:

        import ply.lex as lex

- Para leer el archivo XML de entrada:

        from pathlib import Path
  
- Para trabajar con expresiones regulares:

        import re

- Para el parser sintáctico:
    
        import ply.yacc as yacc
  
Para correr el programa introduzca el siguiente comando en la terminal (dependiendo de la versión de Python instalada),
estando dentro de la carpeta [Tarea-1/Entrega-4/src:](Tarea-1/Entrega-4/src)

    python Analizador_Parser.py

    python3 Analizador_Parser.py

En el archivo `health_topics.txt` se muestran todos los datos que se guardaron en las estructuras de datos creadas.
