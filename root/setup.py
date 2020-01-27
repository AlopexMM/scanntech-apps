from distutils.core import setup

setup(
    # Nombre de la aplicacion:
    name="scanntech-apps",

    # Versión nro:
    version="1.0",

    # Autor de la aplicacion
    author="Mario Mori",
    author_email="mariomori00@gmail.com",

    # Packages
    packages=["reportes"],

    # Incluir archivos adicionales dentro de package
    include_package_data=True,

    # Detalles
    url="http://pypi.python.org/pypi/scanntech-apps-1.0/",

    #
    # License="LICENSE.txt"
    description="Aplicativo para resolver reportes de Scanntech",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "astroid == 2.3.3",
        "isort == 4.3.21,"
        "lazy-object-proxy == 1.4.3",
        "mccabe == 0.6.1",
        "numpy == 1.18.1",
        "pandas == 0.25.3",
        "pkg-resources == 0.0.0",
        "pycodestyle == 2.5.0",
        "python-dateutil == 2.8.1"
        "pytz == 2019.3",
        "six == 1.14.0",
        "wrapt == 1.11.2",
        "xlrd == 1.2.0",
    ],
)
