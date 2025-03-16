"""Integration tests for the complete pipeline."""

import pytest
from utils.validate_pipeline import main

def test_complete_pipeline():
    """Test the complete validation pipeline."""
    try:
        main()
        assert True
    except SystemExit as e:
        assert e.code == 0  # Expecting successful exit 