import re
import sys

from normalize_class import NormalizeText
from compare_normalized_files import CompareNormalizedFiles

input_license_file1 = str(sys.argv[1])

input_license_file2 = str(sys.argv[2])

""" This file executes the main functions of the NormalizeClass. """

try:
    with open(input_license_file1,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        x = NormalizeText(inputstring)
        normalized_string1 = x.returnfinalstring()
        print(normalized_string1)

except IOError:
    print("There is no file named ",InputLicenseFile)
    
try:
    with open(input_license_file2,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        y = NormalizeText(inputstring)
        normalized_string2 = y.returnfinalstring()
        print(normalized_string2)

except IOError:
    print("There is no File named ", input_license_file2)

if(CompareNormalizedFiles(normalized_string1,normalized_string2)==True):
    print("The Two License Texts match")
    
else:
    print("The Two License Texts do not match.")
