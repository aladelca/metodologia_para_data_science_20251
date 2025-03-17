"""Unit tests for notebook generator functions."""

import json

import pytest

from utils.notebook_generator import code_cell, create_notebook, markdown_cell


@pytest.fixture
def temp_notebook(tmp_path):
    """Fixture to create a temporary notebook file."""
    return tmp_path / "test_notebook.ipynb"


def test_create_notebook(temp_notebook):
    """Test notebook creation."""
    cells = [markdown_cell("# Test Notebook"), code_cell("print('Hello, World!')")]

    create_notebook(cells, temp_notebook)

    assert temp_notebook.exists()
    with open(temp_notebook, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    assert "cells" in notebook
    assert len(notebook["cells"]) == 2
    assert notebook["nbformat"] == 4
    assert "metadata" in notebook
    assert "kernelspec" in notebook["metadata"]


def test_markdown_cell():
    """Test markdown cell creation."""
    source = "# Test\n\nThis is a test"
    cell = markdown_cell(source)

    assert cell["cell_type"] == "markdown"
    assert cell["metadata"] == {}
    assert isinstance(cell["source"], list)
    assert len(cell["source"]) == 3
    assert cell["source"][0] == "# Test"


def test_markdown_cell_with_empty_string():
    """Test markdown cell creation with empty string."""
    cell = markdown_cell("")
    assert cell["cell_type"] == "markdown"
    assert cell["source"] == [""]


def test_markdown_cell_with_single_line():
    """Test markdown cell creation with single line."""
    cell = markdown_cell("Single line")
    assert cell["cell_type"] == "markdown"
    assert cell["source"] == ["Single line"]


def test_code_cell():
    """Test code cell creation."""
    source = "x = 42\nprint(x)"
    cell = code_cell(source)

    assert cell["cell_type"] == "code"
    assert cell["metadata"] == {}
    assert isinstance(cell["source"], list)
    assert len(cell["source"]) == 2
    assert cell["source"][0] == "x = 42"
    assert cell["execution_count"] is None
    assert cell["outputs"] == []


def test_code_cell_with_empty_string():
    """Test code cell creation with empty string."""
    cell = code_cell("")
    assert cell["cell_type"] == "code"
    assert cell["source"] == [""]
    assert cell["execution_count"] is None
    assert cell["outputs"] == []


def test_code_cell_with_single_line():
    """Test code cell creation with single line."""
    cell = code_cell("print('test')")
    assert cell["cell_type"] == "code"
    assert cell["source"] == ["print('test')"]
    assert cell["execution_count"] is None
    assert cell["outputs"] == []


def test_create_notebook_with_empty_cells(temp_notebook):
    """Test notebook creation with empty cells list."""
    cells = []
    create_notebook(cells, temp_notebook)

    assert temp_notebook.exists()
    with open(temp_notebook, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    assert "cells" in notebook
    assert len(notebook["cells"]) == 0


def test_create_notebook_metadata(temp_notebook):
    """Test notebook metadata structure."""
    cells = [markdown_cell("# Test")]
    create_notebook(cells, temp_notebook)

    with open(temp_notebook, "r", encoding="utf-8") as f:
        notebook = json.load(f)

    metadata = notebook["metadata"]
    assert "kernelspec" in metadata
    assert metadata["kernelspec"]["language"] == "python"
    assert metadata["kernelspec"]["name"] == "python3"
    assert "language_info" in metadata
    assert metadata["language_info"]["name"] == "python"
    assert metadata["language_info"]["version"].startswith("3")


def test_create_notebook_file_creation(temp_notebook):
    """Test notebook file creation with parent directories."""
    nested_path = temp_notebook.parent / "nested" / "test.ipynb"
    cells = [markdown_cell("# Test")]
    create_notebook(cells, nested_path)

    assert nested_path.exists()
    with open(nested_path, "r", encoding="utf-8") as f:
        notebook = json.load(f)
    assert "cells" in notebook
