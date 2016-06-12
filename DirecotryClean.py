#! /usr/bin/python
"""This script is used for  """

# This tool is used for
import os 

class DirecotryClean(object):
    """This class  """
    direcotry = ''
    def __init__ (self, directory):
        """init the class """
        self.directory = directory

    def set_direcotry (self, directory):
        """Update the directory """
        self.directory = directory

    def get_children (self):
        """get the file/directory list in this directory"""
        return os.listdir(self.directory)


    def clean_up(self):
        """This is the working function for this class"""
        for child in self.get_children :    
            print child




def main ():
    """This the input of this tool script """
    print "Start the program at date"

#    root = DirecotryClean()








if __name__ == '__main__':
    main ()
