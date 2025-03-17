"""Unit tests for notebook generation functions."""

from utils.generate_notebooks import (
    generate_basic_concepts,
    generate_classes,
    generate_code_standards,
    generate_control_structures,
    generate_error_handling,
    generate_functions,
)
from utils.notebook_generator import code_cell, markdown_cell


def test_generate_basic_concepts():
    """Test basic concepts notebook generation."""
    cells = generate_basic_concepts()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_generate_control_structures():
    """Test control structures notebook generation."""
    cells = generate_control_structures()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_generate_functions():
    """Test functions notebook generation."""
    cells = generate_functions()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_generate_classes():
    """Test classes notebook generation."""
    cells = generate_classes()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_generate_error_handling():
    """Test error handling notebook generation."""
    cells = generate_error_handling()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_generate_code_standards():
    """Test code standards notebook generation."""
    cells = generate_code_standards()
    assert isinstance(cells, list)
    assert len(cells) > 0
    assert all(isinstance(cell, dict) for cell in cells)
    assert all("cell_type" in cell for cell in cells)
    assert any(cell["cell_type"] == "markdown" for cell in cells)
    assert any(cell["cell_type"] == "code" for cell in cells)


def test_cell_content():
    """Test cell content structure."""
    # Test markdown cell
    md = markdown_cell("# Test\n\nThis is a test")
    assert md["cell_type"] == "markdown"
    assert isinstance(md["source"], list)
    assert len(md["source"]) > 0

    # Test code cell
    code = code_cell("print('Hello')\nx = 42")
    assert code["cell_type"] == "code"
    assert isinstance(code["source"], list)
    assert len(code["source"]) > 0
    assert code["execution_count"] is None
    assert "outputs" in code
