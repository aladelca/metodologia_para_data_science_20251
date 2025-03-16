"""Unit tests for notebook content generation functions."""

import pytest
from utils.generate_notebooks import (
    generate_basic_concepts,
    generate_control_structures,
    generate_functions,
    generate_classes,
    generate_error_handling,
    generate_code_standards
)

def test_generate_basic_concepts():
    """Test basic concepts notebook generation."""
    cells = generate_basic_concepts()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_generate_control_structures():
    """Test control structures notebook generation."""
    cells = generate_control_structures()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_generate_functions():
    """Test functions notebook generation."""
    cells = generate_functions()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_generate_classes():
    """Test classes notebook generation."""
    cells = generate_classes()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_generate_error_handling():
    """Test error handling notebook generation."""
    cells = generate_error_handling()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_generate_code_standards():
    """Test code standards notebook generation."""
    cells = generate_code_standards()
    assert isinstance(cells, list)
    assert len(cells) > 0
    for cell in cells:
        assert isinstance(cell, dict)
        assert 'cell_type' in cell
        assert cell['cell_type'] in ['markdown', 'code']
        assert 'source' in cell
        assert isinstance(cell['source'], list)

def test_cell_content_structure():
    """Test the structure of cells in all notebooks."""
    test_functions = [
        generate_basic_concepts,
        generate_control_structures,
        generate_functions,
        generate_classes,
        generate_error_handling,
        generate_code_standards
    ]
    
    for generate_func in test_functions:
        cells = generate_func()
        for cell in cells:
            if cell['cell_type'] == 'code':
                assert 'execution_count' in cell
                assert 'outputs' in cell
            assert 'metadata' in cell
            assert isinstance(cell['metadata'], dict) 