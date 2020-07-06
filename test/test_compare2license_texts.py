import unittest
import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

from normalize_license_text.NormalizeClass import NormalizeText 

normalized_output1 = 'data/Data_LicenseText/normalized_output1.py'
normalized_output2 = 'data/Data_LicenseText/normalized_output2.py'


def ReturnLicenseTextMatch(self,InputLicenseFile1,InputLicenseFile2):
    x = NormalizeText()
        
    x.lowercase(InputLicenseFile1,'data/Data_LicenseText/normalized_output1.py')
    x.lowercase(InputLicenseFile2,'data/Data_LicenseText/normalized_output2.py')
        
    x.equivalentwords('data/Data_LicenseText/normalized_output1.py')
    x.equivalentwords('data/Data_LicenseText/normalized_output2.py')
        
    x.copyrightsymbol('data/Data_LicenseText/normalized_output1.py')
    x.copyrightsymbol('data/Data_LicenseText/normalized_output2.py')

    x.bullets_numbering('data/Data_LicenseText/normalized_output1.py')
    x.bullets_numbering('data/Data_LicenseText/normalized_output2.py')
        
    x.punctuation('data/Data_LicenseText/normalized_output1.py')
    x.punctuation('data/Data_LicenseText/normalized_output2.py')
                
    x.license_title('data/Data_LicenseText/normalized_output1.py')
    x.license_title('data/Data_LicenseText/normalized_output2.py')
        
    x.remove_whitespace('data/Data_LicenseText/normalized_output1.py')
    x.remove_whitespace('data/Data_LicenseText/normalized_output2.py')
        
    normalized_output1 = open('data/Data_LicenseText/normalized_output1.py', mode= 'rt', encoding= 'utf-8')
    s1 = normalized_output1.read()

    normalized_output2 = open('data/Data_LicenseText/normalized_output2.py', mode= 'rt', encoding= 'utf-8')
    s2 = normalized_output2.read()
        
    if(s1==s2):
        return True
    else:
        return False
    
    normalized_output1.close()
    normalized_output2.close()

        
class TestTwoLicenseTexts(unittest.TestCase):
        
    def test_license_text(self):
        FiledirA = currpath+"/data/Data_LicenseText/"
        FiledirB = currpath+"/data/Data_LicenseText/"
        self.assertTrue(ReturnLicenseTextMatch(self,FiledirA+"Adobe-2006.txt",FiledirB+"Adobe-2006_2.txt"))
        self.assertTrue(ReturnLicenseTextMatch(self,FiledirA+"sleepycat.txt",FiledirB+"sleepycat_2.txt"))
        self.assertTrue(ReturnLicenseTextMatch(self,FiledirA+"CERN-OHL.txt",FiledirB+"CERN-OHL_2.txt"))
        
if __name__ == '__main__':
    unittest.main()
