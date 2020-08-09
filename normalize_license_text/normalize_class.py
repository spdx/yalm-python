import re
import os
import sys

""" This is the main class responsible for Normalization of License Texts. It takes into 
account the case of the text, punctuations, copyright symbols and whitespaces. The Class mainly
takes as input argument a string and normalizes into an output normalized_string. """ 

class NormalizeText:
    
    def __init__(self,inputstring):
        self.inputstring = inputstring
        
    def returnfinalstring(self):
        normalized_string = ''
        normalized_string = self.lowercase()
        normalized_string = self.equivalentwords(normalized_string)
        normalized_string = self.copyrightsymbol(normalized_string)
        normalized_string = self.bullets_numbering(normalized_string)
        normalized_string = self.punctuation(normalized_string)
        normalized_string = self.license_title(normalized_string)
        normalized_string = self.remove_whitespace(normalized_string)
        return normalized_string
        
    def lowercase(self):
        normalized_string = self.inputstring.lower()
        return normalized_string
        
    def equivalentwords(self,normalized_string):
        try:
            equivalentfile = open("equivalentwords.txt","r")
            for word in equivalentfile.readlines():
                splitwords = word.split(',')
                wordtoreplace = splitwords[0]
                wordreplaced = splitwords[1]
                wordtoreplace = str(wordtoreplace)
                wordreplaced = str(wordreplaced)[:-1]
                normalized_string = re.sub(wordreplaced,wordtoreplace,normalized_string)
            equivalentfile.close()
            return normalized_string
        except IOError:
            print("There was some problem with the function.")
        
        
    def copyrightsymbol(self,normalized_string):
        
        """ Removes the copyright symbol and the possibilities of mismatch due to it. """
        try:
            normalized_string = normalized_string.replace("copyright",'')
            normalized_string = normalized_string.replace('(c)','')
            return normalized_string
        except IOError:
            print("This function could not run properly.")
                    
    def bullets_numbering(self,normalized_string):
        
        """ The most important and error prone function is the handling of the bullets
        and numbering cases. The case has just 1 error prone possibility and requirement
        that the numbering should carry a space after it or else it gets matched with the 
        version. 
        (1. ) will match while (1.) will not.
        """
                            
        try:
            regex_to_substitute = ['([0-9]+\.){2,}','[0-9]+\.[\D]','^[a-z]\.','[a-z]\)','[0-9]\)',
                     '^[A-Z]\.','^[mdclxvi]+\.']
            
            for x in regex:
                normalized_string = re.sub(x,'',normalized_string)
                
            # normalized_string =   re.sub(r'([0-9]+\.){2,}','',normalized_string)
            # normalized_string = re.sub(r'[0-9]+\.[\D]','',normalized_string)
            # normalized_string = re.sub(r'^[a-z]\.','',normalized_string)
            # normalized_string = re.sub(r'[a-z]\)','',normalized_string)
            # normalized_string = re.sub(r'[0-9]\)','',normalized_string)
            # normalized_string = re.sub(r'^[A-Z]\.','',normalized_string)
            # normalized_string = re.sub(r'^[mdclxvi]+\.','',normalized_string)
            return normalized_string
        except IOError:
            print("This function could not run properly.")

    def punctuation(self,normalized_string):
        
        punctuations = ['-','/','*','#','\'','\"','{','}',')','(']
        try:
            for x in punctuations:
                normalized_string = normalized_string.replace(x,'*')
            return normalized_string
        except IOError:
            print("This function could not run properly.")
                
    def license_title(self,normalized_string):
        
        normalized_string = re.sub(r'end of terms and conditions*','',normalized_string)
        return normalized_string
        
    def remove_whitespace(self,normalized_string):
        
        """All the Whitespace and the tabs are removed. At the end of this function
        the input file just becomes a single long string which is easier to match. """
        
        try:
            normalized_string = re.sub(r'\s+','*',normalized_string)
            return normalized_string
        except IOError:
            print("This function could not run properly.")
