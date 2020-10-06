import unittest
import os
from pathlib import Path

from normalize_license_text.normalize_class import NormalizeText
from configuration.config import PACKAGE_PATH
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import CompareNormalizedFiles

input_text = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD.txt"))
input_text = input_text.replace('\\',os.sep)

input_text_mismatch = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD3.txt"))
input_text_mismatch = input_text_mismatch.replace('\\',os.sep)

input_template = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD_template.txt"))
input_template = input_template.replace('\\',os.sep)

class TestAllTexts(unittest.TestCase):
    def test_template_match(self):
        
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            x = NormalizeText(input_text_string)
            normalized_text_string = x.returnfinalstring_for_template()

        with open(input_template, 'r') as input_file:
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

        self.assertEqual(True,CompareNormalizedFiles(normalized_template_string, normalized_text_string))
        
    def test_template_mismatch(self):
        
        with open(input_text_mismatch, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            x = NormalizeText(input_text_string)
            normalized_text_string = x.returnfinalstring_for_template()

        with open(input_template, 'r') as input_file:
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

        self.assertEqual(False,CompareNormalizedFiles(normalized_template_string, normalized_text_string))
        

if __name__ == '__main__':
    unittest.main()
