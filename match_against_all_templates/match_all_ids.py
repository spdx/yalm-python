import os
import sys
import argparse

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.normalize_class import NormalizeText
from compare_template_text.normalize_template_text import NormalizeTemplate
from normalize_license_text.compare_normalized_files import CompareNormalizedFiles

all_template_parser = argparse.ArgumentParser(description='All Templates and the Text to match')

all_template_parser.add_argument('License_Text',
                       metavar='text',
                       type=str,
                       help='the path to text')

args = all_template_parser.parse_args()
input_license_text = args.License_Text

directory = '../data_templates/'

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
    file_name = str(filename.path)
    file_name = file_name.replace('../data_templates','')
    # print(file_name)
    
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
        print("The Text and the Template- "+ file_name + " Match.")
