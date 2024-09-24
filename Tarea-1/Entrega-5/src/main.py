# ------------------------------------------------------------------------------
# main.py
#
# Daniel Gómez Solís
# María Fernanda Herrera Gutiérrez
# Grupo: los kirbys
# ------------------------------------------------------------------------------

from pathlib import Path
from lexer import build_lexer
from parser import build_parser, diccionary_health_content, list_health_topics
import sys


# Define a rule to read data from file
def read_data():
    file_name = Path(__file__).parent / "test.xml"
    with open(file_name, 'r') as file:
        data = file.read()
    return data

# Main function
def main():
    # Read data from file
    data = read_data()

    # Build lexer and parser
    lexer = build_lexer()
    parser = build_parser()

    # Analizar los datos
    parser.parse(data, lexer=lexer)

    print("Information parsed successfully and stored in health_topics.txt")
if __name__ == "__main__":
    main()
