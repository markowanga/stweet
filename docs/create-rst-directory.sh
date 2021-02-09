#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

rm -rf "$DIR"/rst
mkdir "$DIR"/rst
cp "$DIR"/notebooks/*.rst "$DIR"/rst
rm -f "$DIR"/notebooks/*.rst