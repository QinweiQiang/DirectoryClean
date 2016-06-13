#! /usr/bin/python
"""This script is used for  """

# This tool is used for
import os 

def main ():
    """This the input of this tool script """
    print "Start the program at date"

#    root = '/home/peterqi/'
#   root = '/home/peterqi/DirectoryClean'
    root = '/home/peterqi/tmp'





    directory_stack = [root, ]
    #This stack will have M*N elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers

    while len(directory_stack)!= 0:
        current_dir = directory_stack.pop()
        os.chdir(current_dir)
        print 'Enter directory'
        print current_dir
        for elem in os.listdir(current_dir):
            print elem
            if os.path.isfile(elem):
                print 'This is file'
            elif os.path.isdir(elem):
                print 'This is direcotry'
                directory_stack.append(os.path.abspath(elem))
            else:
                print 'This is error'
        


if __name__ == '__main__':
    main ()
