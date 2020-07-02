from config import *
import re
import sys

InputLicenseFile = sys.argv[1]
InputLicenseFile = str(InputLicenseFile)

OutputNormalizedFile = sys.argv[2]
OutputNormalizedFile = str(OutputNormalizedFile)

class NormalizeText:
    def lowercase(self):
        inputfile = open(InputLicenseFile, mode= 'rt', encoding= 'utf-8')
        
        outputfile = open(OutputNormalizedFile,"w")
        for line in inputfile:
            if(str(line).isalpha):
                outputfile.write(str(line).lower())
            else:
                outputfile.write(str(line))
        print("Converted  to LowerCase")
        
    def equivalentwords(self):
        inputfile = open(OutputNormalizedFile,mode = 'r', encoding = 'utf-8')
        data = inputfile.read()
        equivalentfile = open("equivalentwords.txt","r")
        for word in equivalentfile.readlines():
            splitwords = word.split(',')
            wordtoreplace = splitwords[0]
            wordreplaced = splitwords[1]
            data = data.replace(str(wordtoreplace),str(wordreplaced))
        
        inputfile.close()
        fin  = open(OutputNormalizedFile,"wt")
        fin.write(data)
        fin.close()
        print("Replaced Equivalent words")    
        
    def copyrightsymbol(self):
        inputfile = open(OutputNormalizedFile,mode = "r", encoding = 'utf-8')
        data = inputfile.read()
        data = data.replace("copyright","")
        data = data.replace('(c)',"")
        inputfile.close()
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
        print("Copyright symbol")
        
    def punctuation(self):
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
        print("Punctuations")
        
    def bullets_numbering(self):
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.readlines()
        for i in range(len(data)):
            data[i] = re.sub(r'^[0-9]+\.','',data[i])
            data[i] = re.sub(r'^[a-z]\.','',data[i])
            data[i] = re.sub(r'^[A-Z]\.','',data[i])
            data[i] = re.sub(r'^[mdclxvi]+\.','',data[i])

        inputfile.close()
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.writelines(data)
        outputfile.close()
        print("Bullets and Numbering successful")
        
    def license_title(self):
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.read()
        data = re.sub(r'END OF TERMS AND CONDITIONS*','',data)
        inputfile.close()
        
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
        print("Remove License Text at the end of File")
        
    def remove_whitespace(self):
        inputfile = open(OutputNormalizedFile,mode = "r",encoding = 'utf-8')
        data = inputfile.read()
        data  = re.sub(r'\t',' ',data)
        data  = re.sub(r'\r',' ',data)
        data = re.sub(r'\n',' ',data)
        data  = re.sub(r'\r','',data)
        data = data.replace(" ","")
        outputfile = open(OutputNormalizedFile,"wt")
        outputfile.write(data)
        outputfile.close()
        
p = NormalizeText()
p.lowercase()
p.equivalentwords()
p.copyrightsymbol()
p.punctuation()
p.bullets_numbering()
p.license_title()
p.remove_whitespace()
