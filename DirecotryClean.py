#! /usr/bin/python
"""This script is used for  """


import os
import logging

logger = logging.getLogger()

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


#output files
FILES_TO_MOVE=''



def init_logging(logger):
    """Init the log system"""
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

def prepare():
	"""Prepare everything before work"""
	
	FILES_TO_MOVE=os.open(os.path.basename(__file__) + '.to_move'，os.O_RDWR)

def main ():
    """This the input of this tool script """

	#root = '/home/peterqi/tmp'
    root = '/home/steven/mount/peter/160401'
	
    #stack,a list, to store the temporary direcotries
    directory_stack = [root, ]
    #This stack will have M*N elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers


    init_logging(logger)
	
	


    logger.info('Start the tool !')



	prepare()


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
