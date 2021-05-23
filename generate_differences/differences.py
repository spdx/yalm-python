import re
import difflib
from pprint import pprint


class DifferenceGenerator:
    """
    This Class generates the potential differences which are more than
    a length of 10 between the input text and the original input license
    text/template.
    """
    def __init__(self, constant_license, license_to_match):
        self.constant_license = constant_license
        self.license_to_match = license_to_match
        copy_license = license_to_match
        self.copy_license = copy_license
        self.copy_license = self.generate_difference(copy_license)

    def generate_difference(self, copy_license):

        matches = difflib.SequenceMatcher(None, self.constant_license, self.license_to_match).get_matching_blocks()
        print("Following text produces a mismatch with the original template/text")

        for match in matches:
            x = self.license_to_match[match.b:match.b + match.size]
            if (match.size > 10):
                copy_license = copy_license.replace(x, '')

        copy_license = copy_license.replace('`', ' ')
        return copy_license

    def pretty_print_differences(self):
        return self.copy_license
