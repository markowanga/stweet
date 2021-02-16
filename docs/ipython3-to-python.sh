#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

sed -i -- 's/.. code:: ipython3/.. code:: python/g' "$DIR"/rst/*
rm -rf "$DIR"/rst/*--