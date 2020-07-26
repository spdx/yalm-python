import unittest
import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.compare_normalized_files import CompareNormalizedFiles
from compare_template_text.normalize_template_text import NormalizeTemplate
from normalize_license_text.normalize_class import NormalizeText

class TestTemplateText(unittest.TestCase):
    def test_omitable_text(self):
        a = "<<beginOptional>>Hello I am a Test.<<endOptional>>"
        b = "Hello I am a Test."
        x = NormalizeText(a)
        stringtemplate = x.returnfinalstring()
        y = NormalizeText(b)
        stringtext = y.returnfinalstring()
        test = NormalizeTemplate(stringtext, stringtemplate)
        test.remove_omitable_text()
        test.remove_repeating_chars()
        normalized_text = test.return_normalized_text()
        normalized_template = test.return_normalized_template()
        self.assertTrue(CompareNormalizedFiles(normalized_text,normalized_template))
        
    def test_bulletted_text(self):
        a = "<<var;name=\"bullet\";original=\"1\";match=\".{0,20}\">> Definitions." 
        b = " Definitions."
        x = NormalizeText(a)
        stringtemplate = x.returnfinalstring()
        y = NormalizeText(b)
        stringtext = y.returnfinalstring()
        test = NormalizeTemplate(stringtext, stringtemplate)
        test.remove_bulletted_text()
        test.remove_repeating_chars()
        normalized_text = test.return_normalized_text()
        normalized_template = test.return_normalized_template()
        self.assertTrue(CompareNormalizedFiles(normalized_text,normalized_template))

if __name__ == '__main__':
    unittest.main()

        
