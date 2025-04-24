"""Unit tests for validation functions."""
from unittest.mock import patch

from utils.validate_pipeline import (
    main,
    validate_data_availability,
    validate_model_dependencies,
    validate_project_structure,
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


def test_validate_model_dependencies_missing_requirements():
    """Test validate_model_dependencies cuando requirements.txt no existe."""
    with patch("pathlib.Path.exists", return_value=False):
        assert validate_model_dependencies() is False


def test_validate_project_structure_missing_directory():
    """Test validate_project_structure cuando falta un directorio requerido."""
    with patch("pathlib.Path.exists", side_effect=lambda: False):
        assert validate_project_structure() is False


def test_validate_model_dependencies_missing_package():
    """Test validate_model_dependencies cuando falta un paquete requerido."""
    with patch(
        "utils.validate_pipeline._parse_requirements",
        return_value=["nonexistent_package"],
    ):
        with patch("importlib.import_module", side_effect=ImportError):
            assert validate_model_dependencies() is False


def test_main_validation_check_failed():
    """Test para cubrir el bloque else cuando un check falla."""
    with patch(
        "utils.validate_pipeline.validate_project_structure", return_value=False
    ):
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(
                1
            )  # Verifica que el script termina con error


def test_main_validation_check_exception():
    """Test para cubrir el bloque except cuando un check lanza una excepción."""
    with patch(
        "utils.validate_pipeline.validate_project_structure",
        side_effect=Exception("Test error"),
    ):
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(
                1
            )  # Verifica que el script termina con error
