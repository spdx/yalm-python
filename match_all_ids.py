import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.normalize_class import NormalizeText
from compare_template_text.normalize_template_text import NormalizeTemplate
from normalize_license_text.compare_normalized_files import CompareNormalizedFiles

input_license_text = str(sys.argv[1])

directory = 'data_templates/'

"""This file on executing runs through all the License Templates and returns 
the matched IDs. """

try:
    with open(input_license_text,'r') as inputfile:
        input_text_string = inputfile.read()
        inputfile.close()
        x = NormalizeText(input_text_string)
        normalized_text_string = x.returnfinalstring_for_template()

except IOError:
    print("There is no file named ",input_license_text)

for filename in os.scandir(directory):
    print(filename.path)
    try:
        with open(filename.path,'r') as input_file:
            input_template_file = input_file.read()
            input_file.close()
            object_normalization = NormalizeText(input_template_file)
            input_template_file = object_normalization.returnfinalstring_for_template()
            
            y = NormalizeTemplate(normalized_text_string, input_template_file)
            y.normalize_template()
            normalized_template_string = y.return_normalized_template()
    except:
        continue
        
    if(CompareNormalizedFiles(normalized_template_string,normalized_text_string)==True):
        print("The Text and the Template Match.")
    