import re
import sys

"""This class normalizes the template by implementing the Omitable and Replaceable text 
normalizations. """

class NormalizeTemplate:
    
    def __init__(self,text_string,template_string):
        self.text_string = text_string
        self.template_string = template_string
                
    def normalize_template(self):
        self.remove_bulletted_text()
        self.remove_replaceable_text()
        self.remove_omitable_text()
    
    def return_normalized_template(self):
        
        """ Returns the Normalized template after normalization techniques. """
        print(self.template_string)
        return self.template_string
    
    def return_normalized_text(self):
        """ Returns the normalized text after normalization techniques. """
        
        print(self.text_string)
        return self.text_string
    
    def remove_omitable_text(self):
        """ Removes text from the template and the text that is optional. So, the text 
        which is optional and present matches and gets replaced by '' while the text that doesn't match will 
        remain as it is thus giving an unmatch. """
         
        lists = re.findall('(?<=\<\<beginoptional\>\>).*?(?=\<\<endoptional\>\>)',
                           self.template_string)
        # print(lists)
        for x in lists:
            if(x.startswith('*')):
                x = x[1:]

            if(x.endswith('*')):
                x = x[:-1]

            self.text_string = self.text_string.replace(x,'')
            self.template_string = self.template_string.replace(x,'')
            self.template_string = self.template_string.replace('<<beginoptional>>','')
            self.template_string = self.template_string.replace('<<endoptional>>','')
            self.remove_repeating_chars()
        return
    
    def remove_bulletted_text(self):
        """ The bulletted text is found in between the <var tags>. This method removes all the 
        text containing var tags from the template. """ 
        
        self.template_string = re.sub('(?<=\<\<var;name\=\*bullet\*).*?(?=\>\>)','',
                                   self.template_string)
        self.template_string = re.sub('\<\<var;name=\*bullet.*?\>\>','',self.template_string)
        self.remove_repeating_chars()
        return
    
    def remove_replaceable_text(self):
        """The Replaceable Text is found between the <<var copyright tags. This method removes all
        the text between the original fields from the template and the text. """
        
        lists = re.findall('(?<=\<\<var;name=\*;original=).*?(?=;match=.*?\>\>)',
                           self.template_string)
        print(lists)
        for x in lists:
            if(x.startswith('*')):
                x = x[1:]

            if(x.endswith('*')):
                x = x[:-1]

            self.text_string = self.text_string.replace(x,'')
            self.template_string = self.template_string.replace(x,'')
            self.template_string = re.sub('\<\<var;name=.*?;original.*?;match.*?\>\>','',self.template_string)
            self.remove_repeating_chars()
        return
        
    def remove_repeating_chars(self):
        self.template_string = re.sub(r'\*+','*',self.template_string)
        self.text_string = re.sub(r'\*+','*',self.text_string)
        return 













