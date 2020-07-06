import re
import sys

""" This is the main class responsible for Normalization of License Texts. It takes into 
account the case of the text, punctuations, copyright symbols and whitespaces. The functions 
each open the input file and normalize it into the output file both given as arguments.""" 

class NormalizeText:
    def lowercase(self,InputLicenseFile,OutputNormalizedFile):
        inputfile = open(InputLicenseFile, mode= 'rt', encoding= 'utf-8')
        
        outputfile = open(OutputNormalizedFile,"w")
        for line in inputfile:
            if(str(line).isalpha):
                outputfile.write(str(line).lower())
            else:
                outputfile.write(str(line))
        inputfile.close()
        outputfile.close()
            
        
    def equivalentwords(self,OutputNormalizedFile):
        inputfile = open(OutputNormalizedFile,mode = 'r', encoding = 'utf-8')
        data = inputfile.read()
        equivalentfile = open("equivalentwords.txt","r")
        for word in equivalentfile.readlines():
            splitwords = word.split(',')
            wordtoreplace = splitwords[0]
            wordreplaced = splitwords[1]
            data = data.replace(str(wordtoreplace),str(wordreplaced))
        
        inputfile.close()
        equivalentfile.close()
        fin  = open(OutputNormalizedFile,"wt")
        fin.write(data)
        fin.close()
        
    def copyrightsymbol(self,OutputNormalizedFile):
        
        """ Removes the copyright symbol and the possibilities of mismatch due to it. """
        
        inputfile = open(OutputNormalizedFile,mode = "r", encoding = 'utf-8')
        data = inputfile.read()
        data = data.replace("copyright","")
        data = data.replace('(c)',"")
        inputfile.close()
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
                
    def bullets_numbering(self,OutputNormalizedFile):
        
        """ The most important and error prone function is the handling of the bullets
        and numbering cases. The case has just 1 error prone possibility and requirement
        that the numbering should carry a space after it or else it gets matched with the 
        version. """
        
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.readlines()
        for i in range(len(data)):
            data[i] = re.sub(r'([0-9]+\.){2,}','',data[i])
            data[i] = re.sub(r'[0-9]+\.[\D]','',data[i])
            data[i] = re.sub(r'^[a-z]\.','',data[i])
            data[i] = re.sub(r'[a-z]\)','',data[i])
            data[i] = re.sub(r'[0-9]\)','',data[i])
            data[i] = re.sub(r'^[A-Z]\.','',data[i])
            data[i] = re.sub(r'^[mdclxvi]+\.','',data[i])

        inputfile.close()
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.writelines(data)
        outputfile.close()

    def punctuation(self,OutputNormalizedFile):
        inputfile = open(OutputNormalizedFile,mode = "r", encoding = 'utf-8')
        data = inputfile.read()
        data = data.replace('-','')
        data = data.replace('/','')
        data = data.replace('*','')
        data = data.replace('#','')
        data = data.replace('\'','')
        data = data.replace('\"','')
        data = data.replace('{','')
        data = data.replace('}','')
        data = data.replace(')','')
        data = data.replace('(','')
        inputfile.close()
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
        
    def license_title(self,OutputNormalizedFile):
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.read()
        data = re.sub(r'END OF TERMS AND CONDITIONS*','',data)
        inputfile.close()
        
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
        
    def remove_whitespace(self,OutputNormalizedFile):
        
        """All the Whitespace and the tabs are removed. At the end of this function
        the input file just becomes a single long string which is easier to match. """
        
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.read()
        data  = re.sub(r'\t',' ',data)
        data  = re.sub(r'\r',' ',data)
        data = re.sub(r'\n',' ',data)
        data  = re.sub(r'\r','',data)
        data = data.replace(" ","")
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        inputfile.close()
        outputfile.close()
        