from setuptools import setup

setup(
    packages = ["ater", "arba"],
    python_requires = ">=3.6",
    install_requires=["openpyxl>=3"],
    scripts = ["scripts/ater","scripts/scanntech-operaciones", "scripts/arba"]
)
