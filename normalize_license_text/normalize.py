import os
import re
import sys
import argparse

from normalize_class import NormalizeText
from compare_normalized_files import CompareNormalizedFiles

text_parser = argparse.ArgumentParser(description='Match the Licese Texts')

text_parser.add_argument('License_Text1',
                       metavar='text',
                       type=str,
                       help='the path to text A')

text_parser.add_argument('License_Text2',
                       metavar='template',
                       type=str,
                       help='the path to template')

args = text_parser.parse_args()
input_license_file1 = args.License_Text1
input_license_file2 = args.License_Text2

if not os.path.exists(input_license_file1):
    print('The path for License Text specified does not exist')
    sys.exit()

if not os.path.exists(input_license_file2):
    print('The path for License Text specified does not exist')
    sys.exit()


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

if(normalized_string1==normalized_string2):
    print("The Two License Texts match")
    
else:
    print("The Two License Texts do not match.")
