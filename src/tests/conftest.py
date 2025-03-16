"""Shared pytest fixtures and configuration."""

import pytest
import os
import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = str(Path(__file__).parent.parent)
if src_path not in sys.path:
    sys.path.append(src_path)

@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory."""
    return Path(__file__).parent.parent

@pytest.fixture(scope="session")
def data_dir(project_root):
    """Return the data directory."""
    return project_root / "data"

@pytest.fixture(scope="session")
def models_dir(project_root):
    """Return the models directory."""
    return project_root / "models" 