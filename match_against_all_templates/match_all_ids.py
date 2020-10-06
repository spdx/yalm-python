#!/usr/bin/env python

import os
import argparse
from pathlib import Path

from configuration.config import PACKAGE_PATH

from normalize_license_text.normalize_class import NormalizeText
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import CompareNormalizedFiles

Text_Directory = Path(PACKAGE_PATH)


def main():
    """
    This function on executing runs through all the License Templates
    and returns the matched IDs.
    """

    with open(input_license_text, 'r') as inputfile:
        input_text_string = inputfile.read()
        inputfile.close()
        x = NormalizeText(input_text_string)
        normalized_text_string = x.returnfinalstring_for_template()

    for filename in os.scandir(directory):
        file_name = str(filename.path)
        file_name = file_name.replace(str(directory), '')

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

            print("The Text matches with the Template- " + file_name)


if __name__ == "__main__":

    all_template_parser = argparse.ArgumentParser(
        description='All Templates and the Text to match'
    )

    all_template_parser.add_argument('License_Text',
                                     metavar='text',
                                     type=str,
                                     help='the path to text')

    args = all_template_parser.parse_args()

    input_license_text = str(args.License_Text)

    directory = str(Path(PACKAGE_PATH + '\\data\\templates\\'))
    directory = directory.replace('\\',os.sep)

    if not os.path.exists(input_license_text):
        print(
            f'The path for License Text {input_license_text} specified does not exist')
        sys.exit()

    main()
