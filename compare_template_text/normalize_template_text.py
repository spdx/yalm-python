import re
import sys

"""This class normalizes the template by implementing the Omitable and Replaceable text 
normalizations. """

class NormalizeTemplate:
    
    def __init__(self,text_string,template_string):
        self.text_string = text_string
        self.template_string = template_string
        self.remove_replaceable_text()
        self.remove_omitable_text()
        self.remove_repeating_chars()
    
    def return_normalized_template(self):
        # print(self.template_string)
        return self.template_string
    
    def return_normalized_text(self):
        # print(self.text_string)
        return self.text_string
    
    def remove_omitable_text(self):
        lists = re.findall('(?<=\<\<beginoptional\>\>).*?(?=\<\<endoptional\>\>)',
                           self.template_string)
        print(lists)
        for x in lists:
            if(x.startswith('*')):
                x = x[1:]

            if(x.endswith('*')):
                x = x[:-1]

            self.text_string = self.text_string.replace(x,'')
            self.template_string = self.template_string.replace(x,'')
        return
    
    def remove_replaceable_text(self):
        self.template_string = re.sub('(?<=\<\<var;).*?(?=\>\>)','',
                                   self.template_string)
        return
        
    def remove_repeating_chars(self):
        self.template_string = self.template_string.replace('<<beginoptional>>','')
        self.template_string = self.template_string.replace('<<endoptional>>','')
        self.template_string = re.sub('\<\<var;','',self.template_string)
        self.template_string = re.sub('\>\>','',self.template_string)
        self.template_string = re.sub(r'\*+','*',self.template_string)
        self.text_string = re.sub(r'\*+','*',self.text_string)
        return 
