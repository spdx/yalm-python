import re
import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.normalize_class import NormalizeText
from normalize_license_text.compare_normalized_files import CompareNormalizedFiles
from normalize_template_text import NormalizeTemplate

""" This file is the main execution file for comparing License Texts and Templates. It takes into the
files as arguments and passes them along the Normalizing Text class before passing into Normalizing 
Template class. """

InputLicenseText = sys.argv[1]
InputLicenseText = str(InputLicenseText)

InputLicenseTemplate = sys.argv[2]
InputLicenseTemplate = str(InputLicenseTemplate)

try:
    with open(InputLicenseText,'r') as inputfile:
        input_text_string = inputfile.read()
        inputfile.close()
        x = NormalizeText(input_text_string)
        normalized_text_string = x.returnfinalstring()

except IOError:
    print("There is no file named ",InputLicenseText)
    
try:
    with open(InputLicenseTemplate,'r') as inputfile:
        input_template_string = inputfile.read()
        inputfile.close()
        y = NormalizeText(input_template_string)
        normalized_template_string = y.returnfinalstring()

except IOError:
    print("There is no File named ", normalized_template_string)
    
a = NormalizeTemplate(normalized_text_string,normalized_template_string)
normalized_text = a.return_normalized_text()
normalized_template = a.return_normalized_template()

if(CompareNormalizedFiles(normalized_text,normalized_template)==True):
    print("The Text and the Template Match.")
    
else:
    print("The Text and the Template do not Match.")
