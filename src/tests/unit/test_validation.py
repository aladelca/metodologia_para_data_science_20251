"""Unit tests for validation functions."""

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

def test_project_directories(project_root, data_dir, models_dir):
    """Test that project directories exist and are accessible."""
    assert project_root.exists()
    assert data_dir.exists()
    assert models_dir.exists()
    assert (data_dir / "raw").exists()
    assert (data_dir / "processed").exists()
    assert (data_dir / "interim").exists() 