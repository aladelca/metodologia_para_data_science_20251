"""Utility functions for generating Jupyter notebooks."""

import json
from pathlib import Path

def create_notebook(cells, output_path):
    """Create a Jupyter notebook from a list of cells.
    
    Args:
        cells (list): List of dictionaries containing cell content and metadata
        output_path (str or Path): Path where to save the notebook
    """
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

def markdown_cell(source):
    """Create a markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.split('\n')
    }

def code_cell(source):
    """Create a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.split('\n')
    }

# Ejemplo de uso:
if __name__ == "__main__":
    # Crear un notebook básico de Python
    cells = [
        markdown_cell("# Introducción a Python\n\nEste notebook cubre los conceptos básicos de Python."),
        code_cell("# Este es un ejemplo de código\nprint('¡Hola, mundo!')"),
        markdown_cell("## Variables y Tipos de Datos"),
        code_cell("""# Ejemplos de variables
x = 42          # entero
y = 3.14        # flotante
nombre = 'Ana'  # cadena
activo = True   # booleano

print(f"x es de tipo {type(x)}")
print(f"y es de tipo {type(y)}")
print(f"nombre es de tipo {type(nombre)}")
print(f"activo es de tipo {type(activo)}")""")
    ]
    
    create_notebook(cells, "src/notebooks/learning_path/ejemplo.ipynb") 