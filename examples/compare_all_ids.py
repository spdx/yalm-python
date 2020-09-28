#!/usr/bin/env python

# Parses License Texts passed into them and compare them against all the License ids. 

import os
import sys
import argparse

from configuration.config import PACKAGE_PATH

from normalize_license_text.normalize_class import NormalizeText
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import CompareNormalizedFiles

Text_Directory = PACKAGE_PATH + "/match_against_all_templates/input_text_files/"
directory = PACKAGE_PATH + '/data/templates/'

if __name__ == '__main__':
    a = "Any Sample Text passed into Module"
    
    object_a = NormalizeText(a)
    normalized_text_string = object_a.returnfinalstring_for_template()
    
    for filename in os.scandir(directory):
        file_name = str(filename.path)
        file_name = file_name.replace(str(directory), '')
        print(file_name)

        try:
            with open(filename.path, 'r') as input_file:
                input_template_file = input_file.read()
                input_file.close()
                object_normalization = NormalizeText(input_template_file)
                input_template_file = object_normalization.returnfinalstring_for_template()

                y = NormalizeTemplate(
                    normalized_text_string, input_template_file
                    )
                y.normalize_template()
                normalized_template_string = y.return_normalized_template()
                normalized_text_string = y.return_normalized_text()
        except BaseException:
            continue

        if(CompareNormalizedFiles(
            normalized_template_string, normalized_text_string
        )):

            print("The Text and the Template- " + file_name + " Match.")

