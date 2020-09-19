import re
import os
import sys

from configuration.config import PACKAGE_PATH

from generate_differences.differences import Generate_Differences

equivalent_words_file = PACKAGE_PATH + "/resources/equivalentwords.txt"


class NormalizeText:
    """
    This is the main class responsible for Normalization of License Texts. 
    It takes into account the case of the text, punctuations, copyright
    symbols and whitespaces. The Class mainly takes as input argument a
    string and normalizes into an output normalized_string.
    """

    def __init__(self, inputstring):
        self.inputstring = inputstring

    def returnfinalstring(self):
        """
        Return the Final normalized string.
        This function is used in comparing 2 License Texts.
        """

        normalized_string = ''
        normalized_string = self.lowercase()
        normalized_string = self.equivalentwords(normalized_string)
        normalized_string = self.copyrightsymbol(normalized_string)
        normalized_string = self.bullets_numbering(normalized_string)
        normalized_string = self.punctuation(normalized_string)
        normalized_string = self.license_title(normalized_string)
        normalized_string = self.remove_whitespace(normalized_string)
        return normalized_string

    def returnfinalstring_for_template(self):
        """
        Returns the Final Normalized String for Template Format.
        This Function is used in comparing Template and Text.
        """

        normalized_string_for_template = ''
        normalized_string_for_template = self.lowercase()
        normalized_string_for_template = self.equivalentwords(
            normalized_string_for_template)
        normalized_string_for_template = self.punctuation(
            normalized_string_for_template)
        normalized_string_for_template = self.remove_whitespace(
            normalized_string_for_template)
        return normalized_string_for_template

    def lowercase(self):
        """
        Converts The strign into Lowercase.
        """

        normalized_string = self.inputstring.lower()
        return normalized_string

    def equivalentwords(self, normalized_string):
        """
        Checks each word against the equivalent words
        list to avoid mismatch of equivalent words.
        """

        try:
            equivalentfile = open(equivalent_words_file, "r")
            for word in equivalentfile.readlines():
                splitwords = word.split(',')
                wordtoreplace = splitwords[0]
                wordreplaced = splitwords[1]
                wordtoreplace = str(wordtoreplace)
                wordreplaced = str(wordreplaced)[:-1]
                normalized_string = re.sub(
                    wordreplaced, wordtoreplace, normalized_string)
            equivalentfile.close()
            return normalized_string
        except IOError:
            print("There was some problem with the function.")

    def copyrightsymbol(self, normalized_string):
        """
        Removes the copyright symbol and the possibilities 
        of mismatch due to it.
        """

        try:
            normalized_string = normalized_string.replace("copyright", '')
            normalized_string = normalized_string.replace('(c)', '')
            return normalized_string
        except IOError:
            print("This function could not run properly.")

    def bullets_numbering(self, normalized_string):
        """
        The most important and error prone function is the handling
        of the bullets and numbering cases. The case has just 1 error 
        prone possibility and requirement that the numbering should 
        carry a space after it or else it gets matched with the
        version. (1. ) will match while (1.) will not.
        """

        try:
            regex_to_substitute = [
                r'([0-9]+\.){2,}',
                r'[0-9]+\.[\D]',
                r'^[a-z]\.',
                r'[a-z]\)',
                r'[0-9]\)',
                r'^[A-Z]\.',
                '^[mdclxvi]+\.']

            for x in regex_to_substitute:
                normalized_string = re.sub(x, '', normalized_string)

            return normalized_string
        except IOError:
            print("This function could not run properly.")

    def punctuation(self, normalized_string):
        """
        This Function replaces the common punctuations with ` to 
        avoid errors.
        """

        punctuations = ['/', '\'', '\"', '`']
        normalized_string = normalized_string.replace('_', '-')
        normalized_string = normalized_string.replace('--', '-')

        try:
            for x in punctuations:
                normalized_string = normalized_string.replace(x, '`')

            normalized_string = re.sub(r'\.(?=[a-z])', '.`', normalized_string)
            normalized_string = re.sub(r'\,(?=[a-z])', ',`', normalized_string)
            normalized_string = re.sub(r'\-(?=[a-z])', '-`', normalized_string)
            normalized_string = normalized_string + '`'
            normalized_string = '`' + normalized_string
            return normalized_string
        except IOError:
            print("This function could not run properly.")

    def license_title(self, normalized_string):

        normalized_string = re.sub(
            r'end of terms and conditions`', '', normalized_string)
        return normalized_string

    def remove_whitespace(self, normalized_string):
        """
        All the Whitespace and the tabs are removed. At the end of
        this function the input file just becomes a single long
        string which is easier to match.
        """

        try:
            normalized_string = re.sub(r'\s+', '`', normalized_string)
            normalized_string = re.sub(r'\`+', '`', normalized_string)
            return normalized_string
        except IOError:
            print("This function could not run properly.")
