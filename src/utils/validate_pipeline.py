"""Pipeline validation script.

This script runs a complete validation of the data processing and modeling pipeline.
It will be expanded as we develop the project.
"""

import sys
from pathlib import Path

def validate_project_structure():
    """Validate that all required directories and files exist."""
    required_dirs = [
        "data/raw",
        "data/processed",
        "data/interim",
        "notebooks",
        "models",
        "utils",
        "visualization"
    ]
    
    src_dir = Path(__file__).parent.parent
    
    for dir_path in required_dirs:
        if not (src_dir / dir_path).exists():
            print(f"Error: Required directory {dir_path} does not exist")
            return False
    return True

def validate_data_availability():
    """Check if required data files are available."""
    # This will be implemented when we define our data requirements
    return True

def _parse_requirements(requirements_path):
    """Parse requirements.txt file and extract package names."""
    packages = []
    # Mapping de nombres de paquetes a nombres de módulos
    package_to_module = {
        'beautifulsoup4': 'bs4',
        'scikit-learn': 'sklearn',
        'pandas-datareader': 'pandas_datareader',
        'python-dotenv': 'dotenv'
    }
    
    # Paquetes a ignorar (herramientas de desarrollo)
    ignore_packages = {
        'pre-commit', 'black', 'flake8', 'isort', 'mypy',
        'pytest', 'pytest-cov', 'types-PyYAML', 'types-requests',
        'types-setuptools', 'types-python-dateutil', 'pandas-stubs'
    }
    
    with open(requirements_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines, comments and version specifiers
            if not line or line.startswith('#') or line.startswith('-'):
                continue
            # Extract package name without version
            package = line.split('>=')[0].split('<=')[0].split('==')[0].strip()
            # Skip development tools and type stubs
            if package not in ignore_packages and not package.startswith('types-') and not package.endswith('-stubs'):
                # Use the module name if it exists in the mapping, otherwise use the package name
                module_name = package_to_module.get(package, package)
                packages.append(module_name)
    return packages

def validate_model_dependencies():
    """Validate that all required dependencies are available."""
    src_dir = Path(__file__).parent.parent.parent
    requirements_path = src_dir / "requirements.txt"
    
    if not requirements_path.exists():
        print("Error: requirements.txt not found")
        return False
        
    required_packages = _parse_requirements(requirements_path)
    import importlib
    
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"Error: Required package {package} is not installed")
            return False
    return True

def main():
    """Run all validation checks."""
    checks = [
        ("Project Structure", validate_project_structure),
        ("Data Availability", validate_data_availability),
        ("Model Dependencies", validate_model_dependencies)
    ]
    
    all_passed = True
    
    print("Running validation pipeline...")
    print("-" * 50)
    
    for check_name, check_func in checks:
        print(f"\nRunning {check_name} check...")
        try:
            if check_func():
                print(f"✅ {check_name} check passed")
            else:
                print(f"❌ {check_name} check failed")
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {str(e)}")
            all_passed = False
    
    print("\n" + "-" * 50)
    if all_passed:
        print("✅ All validation checks passed!")
        sys.exit(0)
    else:
        print("❌ Some validation checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 