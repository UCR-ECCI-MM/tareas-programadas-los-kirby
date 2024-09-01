# Segundo avance

1. (20%) Este segundo avance debe incluir:

- Analizador léxico funcionando: en esta entrega la herramienta debe ser
capaz de reconocer todos los tokens necesarios para procesar el archivo de
entrada.

## Manual de Uso

Para poder ejecutar el analizador léxico no es necesario instalar ninguna
biblioteca de Python. Sin embargo, es necesario mantener la carpeta
[ply](src/ply) en la carpeta `src` junto al ejecutable
[AnalizadorLexico.py](src/AnalizadorLexico.py).

A su vez, también es necesario importar los siguientes paquetes y módulos al
código:

- Para el análisis léxico:

        import ply.lex as lex

- Para leer el archivo XML de entrada:

        from pathlib import Path

- Para trabajar con expresiones regulares:

    En nuestro caso usamos
    la función `re.sub(pattern, repl, string)` para reemplazar cambios de línea
    dentro del patrón con espacios en blanco en la cadena para evitar dividir una
    oración.

        import re

Para correr el programa introduzca el siguiente comando en la terminal (dependiendo de la versión de Python instalada),
estando dentro de la carpeta [Tarea-1/Entrega-2/src:](Tarea-1/Entrega-2/src)

    python AnalizadorLexico.py

    python3 AnalizadorLexico.py
