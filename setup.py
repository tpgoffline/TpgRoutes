import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="tpgroutes",
    version="1.0.2",
    description="Routes algorithm for Geneva Public Transportations, in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tpgoffline/TpgRoutes",
    author="Rémy Da Costa Faro",
    author_email="remy@tpgoffline.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["tpgroutes"],
    install_requires=["sqlalchemy"],
    entry_points={"console_scripts": ["tpgroutes=tpgroutes.__main__:main"]},
)
