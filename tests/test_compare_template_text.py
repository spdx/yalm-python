import unittest

from yalm.compare_normalized_files import compare_normalized_files
from yalm.normalize_template_text import NormalizeTemplate
from yalm import normalizer


class TestTemplateText(unittest.TestCase):
    def test_omitable_text(self):
        a = "<<beginOptional>>Hello I am a Test.<<endOptional>>"
        b = "Hello I am a Test."
        stringtemplate = normalizer.normalize_template(a)
        stringtext = normalizer.normalize_template(b)
        test = NormalizeTemplate(stringtext, stringtemplate)
        test.remove_repeating_chars()
        test.remove_omitable_text()
        test.remove_repeating_chars()
        normalized_text = test.get_normalized_text()
        normalized_template = test.get_normalized_template()
        self.assertTrue(compare_normalized_files(normalized_template, normalized_text))

    def test_replaceable_text(self):
        a = " <<var;name=\"copyright\";original=\"Hello This is a test.\";match=\".{0,20}\">> Test"
        b = " Hello This  Test"
        stringtemplate = normalizer.normalize_template(a)
        stringtext = normalizer.normalize_template(b)
        test = NormalizeTemplate(stringtext, stringtemplate)
        test.remove_repeating_chars()
        test.remove_replaceable_text()
        test.remove_repeating_chars()
        normalized_text = test.get_normalized_text()
        normalized_template = test.get_normalized_template()
        self.assertTrue(compare_normalized_files(normalized_template, normalized_text))


if __name__ == '__main__':
    unittest.main()
