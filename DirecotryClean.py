#! /usr/bin/python
"""This script is used for  """


import os
import logging
import shutil

#size unit MB
FILE_SIZE_BOUNDARY = 100
# check if dir end without /
DESTINATION_DIR = '/home/steven/tmp/peter/1231/'
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
    logging.getLogger().setLevel(logging.DEBUG)



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
#    DESTINATION_DIR = '/home/peterqi/DirectoryClean_test'
    if not os.path.isdir(DESTINATION_DIR):
        logging.error('Destination directory '+ DESTINATION_DIR +' is invalid')

def move_files(directories):
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
        #logging.debug('Enter directory:'+current_dir)

        for elem in os.listdir(current_dir):
            if os.path.isfile(elem):
                #logging.debug( elem + ' is file')
                classify_files(os.path.abspath(elem), list_for_video, \
                        list_for_torrent, \
                        list_for_remove, \
                        list_for_unclassify)
            elif os.path.isdir(elem):
                #logging.debug( elem + ' is directory')
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
    destination = os.statvfs(DESTINATION_DIR)
    free_size = destination.f_bavail*destination.f_bsize
    logging.info("Destination directory %s has %s free space", DESTINATION_DIR,
            free_size)
    free_size = free_size-150*1024*1024

    dir_video = DESTINATION_DIR + '/video.peter'
    if not os.path.exists(dir_video):
        os.makedirs(dir_video)

    while len(list_for_video) != 0:
        elem = list_for_video.pop()
        if (elem[1] < free_size):

            try_move(elem[0], dir_video)

        else:
            logging.error('No enough space on' +DESTINATION_DIR)
            #store rest of elem into file


def try_move(src, dst):
    """If the src and dst are on same device/partion, move it directly
    If not, copy the file, if successful, delete the source file"""

    logging.debug('Start to move file: ' + src)

    destinate_file_name = dst + '/' + os.path.basename(src)
    if os.path.exists (destinate_file_name):
            logging.warn('Same file exist on target directory: '+ src)
            return

    #check if source and destination are on same device
    if (os.stat(src).st_dev == os.stat(dst).st_dev):
        logging.debug('Same device, move directly!')
        shutil.move (src, destinate_file_name)
    else:
        logging.debug('Different device, copy then delete')
        shutil.copy(src, dst)     

        logging.debug('delete the source file')   
        os.remove(src)
def main ():
    """This the input of this tool script """


    #stack,a list, to store the init and temporary direcotries
    directory_stack = ['/home/steven/tmp/peter/1231/' ]
                      #'/home/peterqi/tmp', \
                      #'/home/steven/mount/peter/160401'

    #This stack will have M*(N-1) elemments at most
    #M is the level of the directory
    #N is the avarage sub-directory numbers

    prepare(directory_stack)

    move_files(directory_stack)






if __name__ == '__main__':
    main ()
