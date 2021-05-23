import unittest

from normalize_license_text.normalize_class import NormalizeText


class TestTwoLicenseTexts(unittest.TestCase):
    def test_lowercase(self):
        a = "This Is A Text"
        b = "this is a text"
        x = NormalizeText(a)
        test1 = x.get_final_string()
        y = NormalizeText(b)
        test2 = y.get_final_string()
        self.assertEqual(test1, test2)

    def test_equivalent(self):
        a = "I study analogue while "
        b = "I study analog whilst "
        x = NormalizeText(a)
        test1 = x.get_final_string()
        y = NormalizeText(b)
        test2 = y.get_final_string()
        self.assertEqual(test1, test2)

    def test_copyrightsymbol(self):
        c = "copyright"
        d = "(c)"
        x = NormalizeText(c)
        test1 = x.get_final_string()
        y = NormalizeText(d)
        test2 = y.get_final_string()
        self.assertEqual(test1, test2)

    def test_bullets(self):
        a = "A. Hello. version 2.3"
        b = "B. Hello. version 2.4"
        x = NormalizeText(a)
        test1 = x.get_final_string()
        y = NormalizeText(b)
        test2 = y.get_final_string()
        self.assertEqual(test1 == test2, False)

    def test_punctuation(self):
        a = "a-b{} (ON)"
        b = "a*b** *ON*"
        x = NormalizeText(a)
        test1 = x.get_final_string()
        y = NormalizeText(b)
        test2 = y.get_final_string()
        self.assertTrue(test1, test2)

    def test_whitespace(self):
        a = "Hello     This is SPDX."
        b = "Hello`This`is`SPDX."
        x = NormalizeText(a)
        test1 = x.get_final_string()
        y = NormalizeText(b)
        test2 = y.get_final_string()
        self.assertTrue(test1, test2)


if __name__ == '__main__':
    unittest.main()
