import re
import sys

from normalize_class import NormalizeText
from compare_normalized_files import CompareNormalizedFiles

InputLicenseFile1 = sys.argv[1]
InputLicenseFile1 = str(InputLicenseFile1)

InputLicenseFile2 = sys.argv[2]
InputLicenseFile2 = str(InputLicenseFile2)

""" This file executes the main functions of the NormalizeClass. """

try:
    with open(InputLicenseFile1,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        x = NormalizeText(inputstring)
        normalized_string1 = x.returnfinalstring()
        # print(normalized_string1)

except IOError:
    print("There is no file named ",InputLicenseFile)
    
try:
    with open(InputLicenseFile2,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        y = NormalizeText(inputstring)
        normalized_string2 = y.returnfinalstring()

except IOError:
    print("There is no File named ", InputLicenseFile2)

if(CompareNormalizedFiles(normalized_string1,normalized_string2)==True):
    print("The Two License Texts match")
    
else:
    print("The Two License Texts do not match.")
