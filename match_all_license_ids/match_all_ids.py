import os
import sys

currpath = str(os.getcwd())
sys.path.append(currpath+"/../")

directory = '../data_templates/'

"""This file on executing runs through all the License Templates and returns 
the matched IDs. """

for filename in os.scandir(directory):
    print(filename.path)
