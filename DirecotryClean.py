#! /usr/bin/python
"""This script is used for  """


import os 
import logging

def init_logging(logger):
    """Init the log system"""
    log_file = os.path.basename(__file__)+'.log'
    log_formater = logging.Formatter(
'%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s')

    #logging.FileHandler(filename, mode='a', encoding=None, delay=False)
    #mode=w, empty the log fie every beggining
    #mode=a, append the log file all the time
    #If delay is true, then file opening is deferred until the first 
    #call to emit(). By default, the file grows indefinitely.
    log_handler = logging.FileHandler(log_file, 'w', None, False)
    log_handler.setFormatter(log_formater)

    log_handler_stdout = logging.StreamHandler()
    log_handler_stdout.setFormatter(log_formater)

    
    logger.addHandler(log_handler)
    logger.addHandler(log_handler_stdout)
    logger.setLevel(logging.DEBUG)
    

def main ():
    """This the input of this tool script """

    logger = logging.getLogger()
    init_logging(logger)
    logger.info('Start the program at date')

    root = '/home/peterqi/tmp'

    #stack,a list, to store the temporary direcotries
    directory_stack = [root, ]
    #This stack will have M*N elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers




    while len(directory_stack)!= 0:

        current_dir = directory_stack.pop()
        os.chdir(current_dir)
        logger.debug('Enter directory:'+current_dir)

        for elem in os.listdir(current_dir):
            if os.path.isfile(elem):
                logger.debug( elem + ' is file')
            elif os.path.isdir(elem):
                logger.debug( elem + 'is directory')
                directory_stack.append(os.path.abspath(elem))
            else:
                logger.warn(elem + 'is either file or directory')
        


if __name__ == '__main__':
    main ()
