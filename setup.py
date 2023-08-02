"""TODO: Add copyright information.
"""

from setuptools import setup, find_packages
from pydna_epbd.version import __version__


# add readme
with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

# add dependencies
with open("requirements.txt", "r") as f:
    INSTALL_REQUIRES = f.read().strip().split("\n")

setup(
    name="pydna_epbd",
    version=__version__,
    author="Anowarul Kabir, Manish Bhattarai, Boian S. Alexandrov",
    author_email="akabir4@gmu.edu",
    description="pyDNA-EPBD: A Python-based Implementation of the Extended Peyrard-Bishop-Dauxois Model for DNA Breathing Dynamics Simulation",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    package_dir={"pydna_epbd": "pydna_epbd"},
    platforms=["Linux", "Mac", "Windows"],
    include_package_data=True,
    setup_requires=[
        "numpy",
        "joblib",
        "matplotlib",
        "pandas",
        "scikit-learn",
        "scipy",
        "seaborn",
    ],
    url="https://github.com/lanl/pyDNA_EPBD",
    packages=find_packages(),
    classifiers=[
        "Development Status :: Beta",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.9.0",
    license="License :: BSD3 License",
)
