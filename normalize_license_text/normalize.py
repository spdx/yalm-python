import re
import sys

from NormalizeClass import NormalizeText

InputLicenseFile = sys.argv[1]
InputLicenseFile = str(InputLicenseFile)

OutputNormalizedFile = sys.argv[2]
OutputNormalizedFile = str(OutputNormalizedFile)

""" This file executes the main functions of the NormalizeClass. """

x = NormalizeText()
x.lowercase(InputLicenseFile,OutputNormalizedFile)
x.equivalentwords(OutputNormalizedFile)
x.copyrightsymbol(OutputNormalizedFile)
x.bullets_numbering(OutputNormalizedFile)
x.punctuation(OutputNormalizedFile)
x.license_title(OutputNormalizedFile)
x.remove_whitespace(OutputNormalizedFile)
