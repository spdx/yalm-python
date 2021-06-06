import unittest
import os
from pathlib import Path

from yalm import normalizer
from yalm.config import PACKAGE_PATH
from yalm.normalize_template_text import NormalizeTemplate
from yalm.compare_normalized_files import compare_normalized_files

input_text = str(Path(PACKAGE_PATH + "\\tests\\data\\OBSD.txt"))
input_text = input_text.replace('\\', os.sep)

input_text_mismatch = str(Path(PACKAGE_PATH + "\\tests\\data\\OBSD3.txt"))
input_text_mismatch = input_text_mismatch.replace('\\', os.sep)

input_template = str(Path(PACKAGE_PATH + "\\tests\\data\\OBSD_template.txt"))
input_template = input_template.replace('\\', os.sep)


class TestAllTexts(unittest.TestCase):
    def test_template_match(self):

        with open(input_text, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            normalized_text_string = normalizer.normalize_template(input_text_string)

        with open(input_template, 'r') as input_file:
            input_template_file = input_file.read()
            input_file.close()
            input_template_file = normalizer.normalize_template(input_template_file)

            y = NormalizeTemplate(normalized_text_string, input_template_file)
            y.normalize_template()
            normalized_template_string = y.get_normalized_template()
            normalized_text_string = y.get_normalized_text()

        self.assertEqual(True, compare_normalized_files(normalized_template_string, normalized_text_string))

    def test_template_mismatch(self):

        with open(input_text_mismatch, 'r') as inputfile:
            input_text_string = inputfile.read()
            inputfile.close()
            normalized_text_string = normalizer.normalize_template(input_text_string)

        with open(input_template, 'r') as input_file:
            input_template_file = input_file.read()
            input_file.close()
            input_template_file = normalizer.normalize_template(input_template_file)

            y = NormalizeTemplate(normalized_text_string, input_template_file)
            y.normalize_template()
            normalized_template_string = y.get_normalized_template()
            normalized_text_string = y.get_normalized_text()

        self.assertEqual(False, compare_normalized_files(normalized_template_string, normalized_text_string))


if __name__ == '__main__':
    unittest.main()
