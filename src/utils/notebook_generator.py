"""Utility functions for generating Jupyter notebooks."""

import json
from pathlib import Path
from typing import Dict, List, Union

# Type aliases
Cell = Dict[str, Union[str, Dict, List[str], None]]
Cells = List[Cell]
PathLike = Union[str, Path]


def create_notebook(cells: Cells, output_path: PathLike) -> None:
    """Create a Jupyter notebook from a list of cells.

    Creates a new Jupyter notebook file with the specified cells and saves it to the
    given path. The notebook will use Python 3 kernel and include standard metadata.
    ----------------------------------------------------------------------------

    Args:
    ----
        cells: List of dictionaries containing cell content and metadata.
        output_path: Path where to save the notebook.
    """
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)


def markdown_cell(source: str) -> Cell:
    """Create a markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": source.split("\n")}


def code_cell(source: str) -> Cell:
    """Create a code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.split("\n"),
    }
