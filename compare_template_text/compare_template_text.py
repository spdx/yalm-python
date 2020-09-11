import re
import os
import sys
import argparse

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.normalize_class import NormalizeText
from normalize_license_text.compare_normalized_files import CompareNormalizedFiles
from normalize_template_text import NormalizeTemplate

""" This file is the main execution file for comparing License Texts and Templates. It takes into the
files as arguments and passes them along the Normalizing Text class before passing into Normalizing 
Template class. """

template_parser = argparse.ArgumentParser(description='The Template and the Text to match')
template_parser.add_argument('Text',
                       metavar='text',
                       type=str,
                       help='the path to text')

template_parser.add_argument('Template',
                       metavar='template',
                       type=str,
                       help='the path to template')

args = template_parser.parse_args()
input_license_template = args.Template
input_license_text = args.Text

if not os.path.exists(input_license_text):
    print('The path for License Text specified does not exist')
    sys.exit()

if not os.path.exists(input_license_template):
    print('The path for License Template specified does not exist')
    sys.exit()

try:
    with open(input_license_text,'r') as inputfile:
        input_text_string = inputfile.read()
        inputfile.close()
        x = NormalizeText(input_text_string)
        normalized_text_string = x.returnfinalstring_for_template()

except IOError:
    print("There is no file named ",input_license_text)
    
try:
    with open(input_license_template,'r') as inputfile:
        input_template_string = inputfile.read()
        inputfile.close()
        y = NormalizeText(input_template_string)
        normalized_template_string = y.returnfinalstring_for_template()

except IOError:
    print("There is no File named ", input_license_template)
    
a = NormalizeTemplate(normalized_text_string,normalized_template_string)
a.normalize_template()
normalized_text = a.return_normalized_text()
normalized_template = a.return_normalized_template()

if(CompareNormalizedFiles(normalized_template,normalized_text)==True):
    print("The Text and the Template Match.")
    
else:
    print("The Text and the Template do not Match.")
    