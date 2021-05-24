import unittest

from normalize_license_text import normalizer


class TestTwoLicenseTexts(unittest.TestCase):
    def test_lowercase(self):
        a = "This Is A Text"
        b = "this is a text"
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertEqual(test1, test2)

    def test_equivalent(self):
        a = "I study analogue while "
        b = "I study analog whilst "
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertEqual(test1, test2)

    def test_copyrightsymbol(self):
        a = "copyright"
        b = "(c)"
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertEqual(test1, test2)

    def test_bullets(self):
        a = "A. Hello. version 2.3"
        b = "B. Hello. version 2.4"
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertEqual(test1 == test2, False)

    def test_punctuation(self):
        a = "a-b{} (ON)"
        b = "a*b** *ON*"
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertTrue(test1, test2)

    def test_whitespace(self):
        a = "Hello     This is SPDX."
        b = "Hello`This`is`SPDX."
        test1 = normalizer.normalize_text(a)
        test2 = normalizer.normalize_text(b)
        self.assertTrue(test1, test2)


if __name__ == '__main__':
    unittest.main()
