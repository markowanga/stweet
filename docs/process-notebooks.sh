#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

rm -rf "$DIR"/rst
rm -f "$DIR"/notebooks/*.csv "$DIR"/notebooks/*.jl
jupyter nbconvert --to rst --execute "$DIR"/notebooks/*.ipynb
jupyter nbconvert --clear-output --inplace "$DIR"/notebooks/*.ipynb
rm -f "$DIR"/notebooks/*.csv "$DIR"/notebooks/*.jl
