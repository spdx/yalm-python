import sys

output1 = sys.argv[1]
output1 = str(output1)

output2 = sys.argv[2]
output2 = str(output2)

output1 = open(output1, mode= 'rt', encoding= 'utf-8')
s1 = output1.read()

output2 = open(output2, mode= 'rt', encoding= 'utf-8')
s2 = output2.read()

if(s1==s2):
    print("Yes")
else:
    print("No")
