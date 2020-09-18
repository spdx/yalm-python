import sys
import re

"""This function matches the normalized text with the normalized template regex using 
the match function. """

def CompareNormalizedFiles(normalized_template,normalized_text):
    if re.match(normalized_template,normalized_text):
        return True
    else:
        return False
