import os
import re
from abc import abstractmethod, ABCMeta

from configuration.config import PACKAGE_PATH
from generate_differences.differences import DifferenceGenerator

class Normalizer(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, s: str) -> str:
        pass


class SequentialNormalizer(Normalizer):
    def __init__(self, normalizers: list[Normalizer]):
        self.normalizers = normalizers

    def __call__(self, s: str) -> str:
        for normalizer in self.normalizers:
            s = normalizer(s)
        return s


class LowercaseNormalizer(Normalizer):
    """
    Converts the string into lowercase.
    """

    def __call__(self, s: str) -> str:
        return s.lower()


class EquivalentWordsNormalizer(Normalizer):
    """
    Checks each word against the equivalent words
    list to avoid mismatch of equivalent words.
    """

    equivalent_words_file = str(PACKAGE_PATH + "\\resources\\equivalentwords.txt")
    equivalent_words_file = equivalent_words_file.replace('\\', os.sep)

    def __call__(self, s: str) -> str:
        with open(self.equivalent_words_file, "r") as equivalentfile:
            for word in equivalentfile.readlines():
                wordtoreplace, wordreplaced = word.split(',')
                wordtoreplace = str(wordtoreplace)
                wordreplaced = str(wordreplaced)[:-1]
                s = s.replace(wordreplaced, wordtoreplace)
        return s


class CopyrightSymbolNormalizer(Normalizer):
    """
    Removes the copyright symbol and the possibilities 
    of mismatch due to it.
    """

    def __call__(self, s: str) -> str:
        s = s.replace("copyright", '')
        s = s.replace('(c)', '')
        return s


class BulletsNumberingNormalizer(Normalizer):
    """
    The most important and error prone function is the handling
    of the bullets and numbering cases. The case has just 1 error
    prone possibility and requirement that the numbering should
    carry a space after it or else it gets matched with the
    version. (1. ) will match while (1.) will not.
    """

    def __call__(self, s: str) -> str:
        regex_to_substitute = [r'([0-9]+\.){2,}', r'[0-9]+\.[\D]', r'^[a-z]\.',
                                r'[a-z]\)', r'[0-9]\)', r'^[A-Z]\.', '^[mdclxvi]+\.']
        for x in regex_to_substitute:
            s = re.sub(x, '', s)
        return s


class PunctuationNormalizer(Normalizer):
    """
    Replaces the common punctuations with ` to avoid errors.
    """
    def __call__(self, s: str) -> str:
        punctuations = ['/', '\'', '\"', '`']
        s = s.replace('_', '-')
        s = s.replace('--', '-')

        for x in punctuations:
            s = s.replace(x, '`')

        s = re.sub(r'\.(?=[a-z])', '.`', s)
        s = re.sub(r'\,(?=[a-z])', ',`', s)
        s = re.sub(r'\-(?=[a-z])', '-`', s)
        s = s + '`'
        s = '`' + s
        return s

class LicenseTitleNormalizer(Normalizer):
    def __call__(self, s: str) -> str:
        s = s.replace('end of terms and conditions', '')
        return s


class WhiteSpaceNormalizer(Normalizer):
    """
    All the Whitespace and the tabs are removed. At the end of
    this function the input file just becomes a single long
    string which is easier to match.
    """
    def __call__(self, s: str) -> str:
        s = re.sub(r'\s+', '`', s)
        s = re.sub(r'\`+', '`', s)
        return s


normalize_text = SequentialNormalizer([
    LowercaseNormalizer(),
    EquivalentWordsNormalizer(),
    CopyrightSymbolNormalizer(),
    BulletsNumberingNormalizer(),
    PunctuationNormalizer(),
    LicenseTitleNormalizer(),
    WhiteSpaceNormalizer(),
])

normalize_template = SequentialNormalizer([
    LowercaseNormalizer(),
    EquivalentWordsNormalizer(),
    PunctuationNormalizer(),
    WhiteSpaceNormalizer(),
])
