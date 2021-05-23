# Parses License Texts passed into them and compare them against all the License ids.

import os
from pathlib import Path

from configuration.config import PACKAGE_PATH

from normalize_license_text.normalize_class import NormalizeText
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import compare_normalized_files

Text_Directory = str(Path(PACKAGE_PATH + "\\match_against_all_templates\\input_text_files\\"))
Text_Directory = Text_Directory.replace('\\', os.sep)

directory = str(Path(PACKAGE_PATH + '\\data\\templates\\'))
directory = directory.replace('\\', os.sep)

if __name__ == '__main__':
    a = "Any Sample Text passed into Module"

    object_a = NormalizeText(a)
    normalized_text_string = object_a.get_final_string_for_template()

    for filename in os.scandir(directory):
        file_name = str(filename.path)
        file_name = file_name.replace(str(directory), '')
        print(file_name)

        try:
            with open(filename.path, 'r') as input_file:
                input_template_file = input_file.read()
                input_file.close()
                object_normalization = NormalizeText(input_template_file)
                input_template_file = object_normalization.get_final_string_for_template()

                y = NormalizeTemplate(normalized_text_string, input_template_file)
                y.normalize_template()
                normalized_template_string = y.get_normalized_template()
                normalized_text_string = y.get_normalized_text()
        except BaseException:
            continue

        if (compare_normalized_files(normalized_template_string, normalized_text_string)):

            print("The Text matches with the Template- " + file_name)
