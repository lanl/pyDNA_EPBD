# cd docs, then run this script: bash create_docs.sh

# pip install sphinx
# pip install sphinx-book-theme
# pip install sphinxcontrib-bibtex
# pip install sphinx-automodapi

# sphinx-quickstart

# > Separate source and build directories (y/n) [n]: y
# > Project name: pyDNA-EPBD
# > Author name(s): AK
# > Project release []: 
# > Project language [en]:

# Bullet points
# * **bold** text :)
# * *italic* text!
# * Code style: ``cool_variable=42``

make clean
rm -rf ./source/modules

# a module directory must have __init__.py in the directory
sphinx-apidoc -o ./source/modules ../

make html