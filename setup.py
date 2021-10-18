from setuptools import setup

setup(
    name="scanntech-operaciones",
    packages = ["ater", "arba", "citi","padron"],
    python_requires = ">=3.6",
    install_requires=["openpyxl>=3", "pyfiglet", "sqlalchemy"],
    scripts = ["scripts/ater","scripts/scanntech-operaciones", "scripts/arba", "scripts/citi", "scripts/padron"]
)
