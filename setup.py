"""Setup para el proyecto."""
from setuptools import find_packages, setup

setup(
    name="metodologia_data_science",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas",
        "requests",
    ],
)
