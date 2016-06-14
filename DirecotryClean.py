#! /usr/bin/python
"""This script is used for  """


import os
import logging

logger = logging.getLogger('peter')

FILE_FORMATE_LIST = ('.iso', \
     '.webm',\
     '.mkv',\
     '.flv',\
     '.vob',\
     '.ogv',\
     '.ogg',\
     '.mng',\
     '.avi',\
     '.mov',\
     '.qt',\
     '.wmv',\
     '.yuv',\
     '.rm',\
     '.rmvb',\
     '.asf',\
     '.amv',\
     '.mp4',\
     '.m4p',\
     '.m4v',\
     '.mpg',\
     '.mp2',\
     '.mpeg',\
     '.mpe',\
     '.mpv',\
     '.m2v',\
     '.m4v',\
     '.svi',\
     '.3gp',\
     '.3g2',\
     '.mxf',\
     '.roq',\
     '.nsv',\
     '.f4v',\
     '.f4p',\
     '.f4a',\
     '.f4b'
     )


def init_logging():
    """Init the log system"""
    print "Init the logging"
    log_file = os.path.basename(__file__)+'.log'
    log_formater = logging.Formatter(
    '%(asctime)s \
    %(levelname)s \
    %(filename)s:%(lineno)d \
    %(message)s')

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
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)




def prepare_process_file(file_name):
    """Prepare process the file
       Check the file name and file size, etc.
       Put the
       """
    #need file bigger than 100MB
    #file_size_boundary = 100*1024*1024
    #FILE_FORMATE_LIST
    
    #if file size less than file_size_boundary,  to_remove list


    #get suffix of file
    suffix = os.path.splitext(file_name)[1]

    #if file is suffix with FILE_FORMATE_LIST, in to_move list
    if (suffix in FILE_FORMATE_LIST) or \
    (suffix.lower() in FILE_FORMATE_LIST):
        logger.info('Video file:' + file_name)

    #if else, put it in manually operation list





def prepare(stack):
    """Prepare everything before real work"""
    
    init_logging()

    #check the directory_strack to see if all elements are 
    #valid directories
    for element in stack:
        if not os.path.isdir(element):
            stack.remove(element)
            logger.warn("Remove directory '"+ element +
                    "'as it is not an valid directory")

def main ():
    """This the input of this tool script """

	
    #stack,a list, to store the init and temporary direcotries
    directory_stack = ['/home/peterqi/tmp', \
                       '/home/steven/mount/peter/160401']
    #This stack will have M*(N-1) elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers
    
    prepare(directory_stack)

    logger.info('Start the tool !')


    while len(directory_stack)!= 0:

        current_dir = directory_stack.pop()
        os.chdir(current_dir)
        logger.debug('Enter directory:'+current_dir)

        for elem in os.listdir(current_dir):
            if os.path.isfile(elem):
                logger.debug( elem + ' is file')
                prepare_process_file(os.path.abspath(elem))
            elif os.path.isdir(elem):
                logger.debug( elem + ' is directory')
                directory_stack.append(os.path.abspath(elem))
            else:
                logger.warn(elem + ' is either file or directory')



if __name__ == '__main__':
    main ()
