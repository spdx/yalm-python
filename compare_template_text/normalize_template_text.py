import re

class NormalizeTemplate:
    """
    This class normalizes the template by implementing the Omitable and Replaceable text 
    normalizations.
    """

    def __init__(self,text_string,template_string):
        self.text_string = text_string
        self.template_string = template_string
        self.template_string = self.template_string.replace('\\','@')
        self.template_string  = re.escape(self.template_string)
                
    def normalize_template(self):
        self.remove_repeating_chars()
        self.remove_replaceable_text()
        self.remove_omitable_text()
    
    def return_normalized_template(self):
        """ 
        Returns the Normalized template after normalization techniques. 
        """
        return self.template_string
    
    def return_normalized_text(self):
        """
        Returns the normalized text after normalization techniques.
        """
        
        return self.text_string
    
    def remove_omitable_text(self):
        """ 
        Removes text from the template and the text that is optional. 
        So, the text which is optional and present matches and gets 
        replaced by '' while the text that doesn't match will remain as
        it is thus giving an unmatch.
        """
         
        lists = re.findall('`?<<beginoptional>>.*?<<endoptional>>`?',
                           self.template_string)
        
        for x in lists:
            """ 
            match_regex will find the text within the optional tags. 
            This has been done using lookup and lookbehind rule in regex
            to match only the text proceeding <<endOptional>> and succeeding
            <<beginoptional>>
            """
            
            match_regex = re.search('(?<=<<beginoptional>>).*?(?=<<endoptional>>)',
                                    x).group(0)
            if(match_regex.startswith('`')):
                match_regex = match_regex[1:]

            if(match_regex.endswith('`')):
                match_regex = match_regex[:-1]
            
            self.template_string = self.template_string.replace(
                x,'`?('+match_regex+')?`?')
            
        self.remove_repeating_chars()           
        return
        
    def remove_replaceable_text(self):
        """
        The Replaceable Text is found between the <<var copyright tags.
        This method removes all the text between the original fields 
        from the template and the text. 
        """
        
        lists = re.findall('`?<<var.*?>>`?', self.template_string)
        
        for x in lists:
            """ 
            match_regex contains the match pos in the template rule format.
            It will match the text only if its succeeding the match keyword and
            proceeding the ">>" end tags.
            """
             
            match_regex = re.search('(?<=match=\`).*?(?=\`>>)',x).group(0)
            if(match_regex.startswith('`')):
                match_regex = match_regex[1:]

            if(match_regex.endswith('`')):
                match_regex = match_regex[:-1]

            """ The '\' is required to be replaced because the match pos shouldn't
            contain any escaped characters. The only escaped characters present in 
            it are those which contain '\' in the match pos. These characters are
            replaced with '@' to identify them and are later converted back to '\'
            """
              
            match_regex = match_regex.replace('\\','')
            match_regex = match_regex.replace('`','')
            self.template_string = self.template_string.replace(
                x,'`'+match_regex+'`')
            self.remove_repeating_chars()
            
        escaped_chars_list = re.findall('@(?=\W)',self.template_string)
        for x in escaped_chars_list:
            self.template_string = self.template_string.replace(x,'\\')
        return
     
    def remove_repeating_chars(self):                
        """
        This function is necessary for unnecessary piling up the '`' and the
        '`?' generated in the omitable_text and the replaceable_text function.
        """

        self.template_string = re.sub(r'`+','`',self.template_string)
        self.template_string = re.sub(r'(`\?)+','`?',self.template_string)
        return 
