import unittest
import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.normalize_class import NormalizeText
from normalize_license_text.compare_normalized_files import CompareNormalizedFiles
        
class TestTwoLicenseTexts(unittest.TestCase):
    def test_lowercase(self):
        a = "This Is A Text"
        b = "this is a text"
        x = NormalizeText(a)
        test1 = x.lowercase()
        y = NormalizeText(b)
        test2 = y.lowercase()
        self.assertEqual(test1,test2)
        
    def test_equivalent(self):
        a = "I study analogue while "
        b = "I study analog whilst "
        x = NormalizeText(a)
        test1 = x.equivalentwords(a)
        y = NormalizeText(b)
        test2 = y.equivalentwords(b)
        self.assertEqual(test1,test2)
        
    def test_copyrightsymbol(self):
        c = "copyright"
        d = "(c)"
        x = NormalizeText(c)
        test1 = x.copyrightsymbol(c)
        y = NormalizeText(d)
        test2 = y.copyrightsymbol(d)
        self.assertEqual(test1,test2)
        
    def test_bullets(self):
        a = "A. Hello. version 2.3"
        b = "B. Hello. version 2.4"
        x = NormalizeText(a)
        test1 = x.bullets_numbering(a)
        y = NormalizeText(b)
        test2 = y.bullets_numbering(b)
        print(test1)
        print(test2)
        self.assertFalse(CompareNormalizedFiles(test1,test2))
        
    def test_punctuation(self):
        a = "a-b{} (ON)"
        b = "a*b** *ON*"
        x = NormalizeText(a)
        test1 = x.punctuation(a)
        y = NormalizeText(b)
        test2 = y.punctuation(b)
        self.assertTrue(CompareNormalizedFiles(test1,test2))
        
    def test_whitespace(self):
        a = "Hello     This is SPDX."
        b = "Hello*This*is*SPDX."
        x = NormalizeText(a)
        test1 = x.remove_whitespace(a)
        y = NormalizeText(b)
        test2 = y.remove_whitespace(b)
        print(test1)
        print(test2)
        self.assertTrue(CompareNormalizedFiles(test1,test2))

if __name__ == '__main__':
    unittest.main()
