import os
import re
import sys
import argparse
from pprint import pprint

from normalize_class import NormalizeText
from generate_differences.differences import Generate_Differences

from configuration.config import PACKAGE_PATH
Text_Directory = PACKAGE_PATH + "/normalize_license_text/input_text_files/"


""" This file executes the main functions of the NormalizeClass. """

def main():
    with open(input_license_file1,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        x = NormalizeText(inputstring)
        normalized_string1 = x.returnfinalstring()

    with open(input_license_file2,'r') as inputfile:
        inputstring = inputfile.read()
        inputfile.close()
        y = NormalizeText(inputstring)
        normalized_string2 = y.returnfinalstring()

    if(normalized_string1==normalized_string2):
        print("The Two License Texts match")
    
    else:
        print("The Two License Texts do not match.")
        compare_object = Generate_Differences(normalized_string1,normalized_string2)
        differences = compare_object.pretty_print_differences()
        pprint(differences)


if __name__ == "__main__":
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

    input_license_file1 = Text_Directory + str(args.License_Text1)
    input_license_file2 = Text_Directory + str(args.License_Text2)


    if not os.path.exists(input_license_file1):
        print(f'The path for License Text {input_license_file1} specified does not exist')
        sys.exit()

    if not os.path.exists(input_license_file2):
        print(f'The path for License Text {input_license_file2} specified does not exist')
        sys.exit()

    main()
