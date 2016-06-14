#! /usr/bin/python
"""This script is used for  """


import os
import logging


#size unit MB
FILE_SIZE_BOUNDARY = 100

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


    logging.getLogger().addHandler(log_handler)
    logging.getLogger().addHandler(log_handler_stdout)
    logging.getLogger().setLevel(logging.INFO)
#    logging.getLogger().setLevel(logging.DEBUG)



def classify_files(file_name, list_video, list_torrent, list_remove, \
        list_unclassify):
    """Prepare process the file
       Check the file name and file size, etc.
       Put the
       """
    logging.debug('classify_files') 

    file_size = os.path.getsize(file_name)

    #get suffix of file
    suffix = os.path.splitext(file_name)[1]

    #if file is suffix with '.torrent'
    if suffix == '.torrent':
        list_torrent.append([file_name, file_size])
        logging.debug('File is torrent file')
        return



    #if file is suffix with FILE_FORMATE_LIST
    if (suffix in FILE_FORMATE_LIST) or \
    (suffix.lower() in FILE_FORMATE_LIST):
        list_video.append([file_name, file_size])
        logging.info('Video file:' + file_name)
        return
   
    #if file size less than FILE_SIZE_BOUNDARY, to remove list
    if (file_size < FILE_SIZE_BOUNDARY*1024*1024):
        list_remove.append(file_name)
        logging.info('File size less than %s MB, remove it', FILE_SIZE_BOUNDARY)
        return
       
    #if else, put it in unclassify list
    list_unclassify.append([file_name, file_size])






def prepare(stack):
    """Prepare everything before real work"""
    
    init_logging()

    logging.info('Start the tool !')
    #check the directory_strack to see if all elements are 
    #valid directories
    for element in stack:
        if not os.path.isdir(element):
            stack.remove(element)
            logging.warn("Remove directory '"+ element +
                    "'as it is not an valid directory")

def find_files(directories):
    """Loop over all the directories/sub-directories to find all files
       Store absolute file name to different temporary files according
       to different file format
       """
    list_for_remove = []
    list_for_torrent = []
    list_for_video = []
    list_for_unclassify = []


    while len(directories)!= 0:

        current_dir = directories.pop()
        os.chdir(current_dir)
        logging.debug('Enter directory:'+current_dir)

        for elem in os.listdir(current_dir):
            if os.path.isfile(elem):
                logging.debug( elem + ' is file')
                classify_files(os.path.abspath(elem), list_for_video, \
                        list_for_torrent, \
                        list_for_remove, \
                        list_for_unclassify)
            elif os.path.isdir(elem):
                logging.debug( elem + ' is directory')
                directories.append(os.path.abspath(elem))
            else:
                logging.warn(elem + ' is either file or directory')
 
    print list_for_remove
    print '---------------------------------'
    print list_for_torrent
    print '---------------------------------'
    print list_for_video
    print '---------------------------------'
    print list_for_unclassify

    #delete/move the file when classify it is a little 'rude'
    #store their absolute names into files first




def main ():
    """This the input of this tool script """

	
    #stack,a list, to store the init and temporary direcotries
    directory_stack = ['/home/peterqi/DirectoryClean_test', \
                      #'/home/peterqi/tmp', \
                      '/home/steven/mount/peter/160401']
    #This stack will have M*(N-1) elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers
    
    prepare(directory_stack)
    find_files(directory_stack)
#    move_files()






if __name__ == '__main__':
    main ()
