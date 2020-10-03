import unittest
import os

from normalize_license_text.normalize_class import NormalizeText
from configuration.config import PACKAGE_PATH
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import CompareNormalizedFiles

input_text = PACKAGE_PATH + "/test/data/OBSD.txt"
input_text2 = PACKAGE_PATH + "/test/data/OBSD2.txt"
input_text_unmatch = PACKAGE_PATH + "/test/data/OBSD3.txt"

directory = PACKAGE_PATH + "/data/templates/"


class TestNormalizeTexts(unittest.TestCase):
    def test_normalize_match(self):        
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            x = NormalizeText(input_text_string)
            normalized_text_string = x.returnfinalstring()

        with open(input_text2, 'r') as input_file:
            input_text_string2 = input_file.read()
            input_file.close()
            y = NormalizeText(input_text_string2)
            normalized_text_string2 = y.returnfinalstring()

        self.assertEqual(True, normalized_text_string2==normalized_text_string)
        
    def test_normalize_unmatch(self):
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            x = NormalizeText(input_text_string)
            normalized_text_string = x.returnfinalstring()

        with open(input_text_unmatch, 'r') as input_file:
            input_text_string2 = input_file.read()
            input_file.close()
            y = NormalizeText(input_text_string2)
            normalized_text_string2 = y.returnfinalstring()

        self.assertEqual(False, normalized_text_string2==normalized_text_string)


if __name__ == '__main__':
    unittest.main()
