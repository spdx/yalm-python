import unittest
import os
from pathlib import Path, PureWindowsPath

from yalm import normalizer
from yalm.config import PACKAGE_PATH
from yalm.normalize_template_text import NormalizeTemplate
from yalm.compare_normalized_files import compare_normalized_files

input_text = Path(PACKAGE_PATH + "/tests/data/test_all_ids.txt")
directory = Path(PACKAGE_PATH + "/data/templates/")


class TestAllTexts(unittest.TestCase):
    def test_main_script(self):
        list_of_matches = []
        matches_list = ["AAL.template.txt"]

        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            normalized_text_string = normalizer.normalize_template(input_text_string)

        for filename in os.scandir(directory):
            file_name = str(filename.path)
            file_name = file_name.replace(str(directory), '')
            file_name = file_name.replace('\\', '')
            file_name = file_name.replace('/', '')
            print(file_name)

            try:
                with open(filename.path, 'r') as input_file:
                    input_template_file = input_file.read()
                    input_file.close()
                    input_template_file = normalizer.normalize_template(input_template_file)

                    y = NormalizeTemplate(normalized_text_string, input_template_file)
                    y.normalize_template()
                    normalized_template_string = y.get_normalized_template()
                    normalized_text_string = y.get_normalized_text()
            except BaseException:
                continue

            if (compare_normalized_files(normalized_template_string, normalized_text_string)):
                list_of_matches.append(file_name)
                print("The Text matches with the Template- " + file_name)

        self.assertCountEqual(list_of_matches, matches_list)


if __name__ == '__main__':
    unittest.main()
