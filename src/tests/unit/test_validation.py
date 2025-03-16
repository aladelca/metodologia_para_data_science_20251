"""Unit tests for validation pipeline."""

import pytest
from utils.validate_pipeline import (
    validate_project_structure,
    validate_data_availability,
    validate_model_dependencies,
)

def test_validate_project_structure():
    """Test project structure validation."""
    assert validate_project_structure() is True

def test_validate_data_availability():
    """Test data availability validation."""
    assert validate_data_availability() is True

def test_validate_model_dependencies():
    """Test model dependencies validation."""
    assert validate_model_dependencies() is True 