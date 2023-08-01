"""
2021. Triad National Security, LLC. All rights reserved.
This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos
National Laboratory (LANL), which is operated by Triad National Security, LLC for the U.S.
Department of Energy/National Nuclear Security Administration. All rights in the program are
reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear
Security Administration. The Government is granted for itself and others acting on its behalf a
nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare
derivative works, distribute copies to the public, perform publicly and display publicly,
and to permit others to do so.
"""
from setuptools import setup, find_packages
from glob import glob

__version__ = "1.0.0"

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
