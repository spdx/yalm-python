import unittest
import os

from normalize_license_text.normalize_class import NormalizeText
from configuration.config import PACKAGE_PATH
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import CompareNormalizedFiles

input_text = PACKAGE_PATH + "/test/data/test_all_ids.txt"
directory = PACKAGE_PATH + "/data/templates/"


class TestAllTexts(unittest.TestCase):
    def test_main_script(self):
        list_of_matches = []
        matches_list = ["AAL.template.txt"]
        
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            x = NormalizeText(input_text_string)
            normalized_text_string = x.returnfinalstring_for_template()

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

            if(CompareNormalizedFiles(normalized_template_string, normalized_text_string)):
                list_of_matches.append(file_name)
                print("The Text matches with the Template- " + file_name)
                
        self.assertCountEqual(list_of_matches,matches_list)


if __name__ == '__main__':
    unittest.main()
