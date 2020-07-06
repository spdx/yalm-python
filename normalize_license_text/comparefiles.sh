#!/bin/bash

# This is the final script to be executed in the Command Line interface. 
# The user can take 2 files and pass along this function as arguments and
# the shell will print the output.

python normalize.py $1 output.py
python normalize.py $2 output2.py
 
python3 compare_normalized_files.py output.py output2.py

