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

input_license_text = str(sys.argv[1])

input_license_template = str(sys.argv[2])

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
    