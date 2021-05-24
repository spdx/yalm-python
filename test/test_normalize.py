import unittest
import os
from pathlib import Path

from normalize_license_text import normalizer
from configuration.config import PACKAGE_PATH
from compare_template_text.normalize_template_text import NormalizeTemplate
from compare_template_text.compare_normalized_files import compare_normalized_files

input_text = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD.txt"))
input_text = input_text.replace('\\', os.sep)

input_text2 = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD2.txt"))
input_text2 = input_text.replace('\\', os.sep)

input_text_unmatch = str(Path(PACKAGE_PATH + "\\test\\data\\OBSD3.txt"))
input_text_unmatch = input_text.replace('\\', os.sep)


class TestNormalizeTexts(unittest.TestCase):
    def test_normalize_match(self):
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            normalized_text_string = normalizer.normalize_text(input_text_string)

        with open(input_text2, 'r') as input_file:
            input_text_string2 = input_file.read()
            input_file.close()
            normalized_text_string2 = normalizer.normalize_text(input_text_string2)

        self.assertEqual(True, normalized_text_string2 == normalized_text_string)

    def test_normalize_unmatch(self):
        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            normalized_text_string = normalizer.normalize_text(input_text_string)

        with open(input_text_unmatch, 'r') as input_file:
            input_text_string2 = input_file.read()
            input_file.close()
            normalized_text_string2 = normalizer.normalize_text(input_text_string2)

        self.assertEqual(True, normalized_text_string2 == normalized_text_string)


if __name__ == '__main__':
    unittest.main()
