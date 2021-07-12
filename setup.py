from setuptools import setup

setup(
    packages = ["ater", "arba", "citi"],
    python_requires = ">=3.6",
    install_requires=["openpyxl>=3", "pyfiglet"],
    scripts = ["scripts/ater","scripts/scanntech-operaciones", "scripts/arba", "scripts/citi"]
)
