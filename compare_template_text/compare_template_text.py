import re
import os
import argparse
from pprint import pprint

from configuration.config import PACKAGE_PATH

from normalize_license_text.normalize_class import NormalizeText
from compare_normalized_files import CompareNormalizedFiles
from normalize_template_text import NormalizeTemplate
from generate_differences.differences import Generate_Differences


def main():
    """
    This file is the main execution file for
    comparing License Texts and Templates. It
    takes into the files as arguments and passes
    them along the Normalizing Text class before
    passing into Normalizing Template class.
    """

    with open(input_license_text, 'r') as inputfile:
        input_text_string = inputfile.read()
        inputfile.close()
        x = NormalizeText(input_text_string)
        normalized_text_string = x.returnfinalstring_for_template()

    with open(input_license_template, 'r') as inputfile:
        input_template_string = inputfile.read()
        inputfile.close()
        y = NormalizeText(input_template_string)
        normalized_template_string = y.returnfinalstring_for_template()

    a = NormalizeTemplate(normalized_text_string, normalized_template_string)
    a.normalize_template()
    normalized_text = a.return_normalized_text()
    normalized_template = a.return_normalized_template()

    if (CompareNormalizedFiles(normalized_template, normalized_text)):
        print("The Text and the Template Match.")

    else:
        nl = "\n"
        print(f"The Text and the Template do not Match.{nl}" f"Following text produces a mismatch{nl}")
        compare_object = Generate_Differences(normalized_template, normalized_text)

        differences = compare_object.pretty_print_differences()
        pprint(differences)


if __name__ == "__main__":

    template_parser = argparse.ArgumentParser(description='The Template and the Text to match')

    template_parser.add_argument('Text', metavar='text', type=str, help='the path to text')

    template_parser.add_argument('Template', metavar='template', type=str, help='the path to template')

    args = template_parser.parse_args()

    input_license_template = str(args.Template)
    input_license_text = str(args.Text)

    if not os.path.exists(input_license_text):
        print(f'The path for License Text {input_license_text} specified does not exist')
        sys.exit()

    if not os.path.exists(input_license_template):
        print(f'The path for License Template {input_license_template} specified does not exist')
        sys.exit()

    main()
