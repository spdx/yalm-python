#!/bin/bash

python normalize.py $1 output.py
python normalize.py $2 output2.py
 
python3 compare_normalized_files.py output.py output2.py

