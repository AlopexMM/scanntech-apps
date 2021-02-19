from setuptools import setup, find_packages

setup(
    name="scanntech-operaciones",
    version="0.1.0",
    packages=find_packages(include=["scanntech-operaciones", "scanntech-operaciones.*"],
    install_requires = ["openpyxl"]
    setup_requires=["pytest-runner", "flake8"],
    test_require=["pytest"]
)
