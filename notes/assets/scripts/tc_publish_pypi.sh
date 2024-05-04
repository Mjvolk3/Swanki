#!/bin/bash
cd /Users/michaelvolk/Documents/projects/swanki
rm -rf ./dist
eval "$(conda shell.bash hook)"
conda activate swanki
python -m build
twine upload dist/*