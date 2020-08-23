import sys
import re

"""This file finally checks and matches the normalized files passed onto it 
from the normalize.py file resulting from the output of NormalizeText class' return function.
It returns the output of the result. """

def CompareNormalizedFiles(a,b):
    if re.match(a,b):
        return True
    else:
        return False
