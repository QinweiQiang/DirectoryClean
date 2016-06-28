#! /usr/bin/python
"""This script is used for  """


import os
import logging
import shutil


#size unit MB
FILE_SIZE_BOUNDARY = 100
# check if dir end without /
#DESTINATION_DIR = '/home/steven/tmp/peter/1231/'
HOME = '/home/peterqi/'


DESTINATION_DIR = HOME + 'DirectoryClean_test' 
SOURCE_DIR = HOME + 'DirectoryClean_test'
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
    %(levelname)7s \
    %(filename)s:%(lineno)4d \
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

def try_move(src, dst):
    """If the src and dst are on same device/partion, move it directly
    If not, copy the file, if successful, delete the source file"""
 
    logging.debug('Moving file ' + src)
 
    destinate_file_name = dst + '/' + os.path.basename(src)
    if os.path.exists (destinate_file_name):
        logging.warn('Same file exists on target directory: '+ src)
        return 1
 
    try:
        shutil.move (src, destinate_file_name)
        return 0

    except IOError, msg:
        logging.warn('Error when move file ' + src + ' error' + msg)
        return 1
    # #check if source and destination are on same device
    # if (os.stat(src).st_dev == os.stat(dst).st_dev):
    #     logging.debug('Same device, move directly!')
    #     shutil.move (src, destinate_file_name)
    # else:
    #     logging.debug('Different device, copy then delete')
    #     shutil.copy(src, dst)     
 
    #     logging.debug('delete the source file')   
    #     os.remove(src)
 
class DirecotryClean:
    """ This is the main class for this tool"""
    

    source_dir = ''
    dest_dir = ''
    list_for_video = []
    list_for_remove = []
    list_for_torrent = []
    list_for_unclassify = []





    def __init__ (self):
        """ nothing need to do here"""



    def classify_files(self, file_name):
        """Prepare process the file
           Check the file name and file size, etc.
           Put the
           """
        #logging.debug('Start to classify files')
    
        file_size = os.path.getsize(file_name)
    
        #get suffix of file
        suffix = os.path.splitext(file_name)[1]
    
        #if file is suffix with '.torrent'
        if suffix == '.torrent':
            self.list_for_torrent.append([file_name, file_size])
            logging.debug('File is torrent file')
            return 0
    
    
    
        #if file is suffix with FILE_FORMATE_LIST
        if (suffix in FILE_FORMATE_LIST) or \
        (suffix.lower() in FILE_FORMATE_LIST):
            self.list_for_video.append([file_name, file_size])
            logging.info('Video file:' + file_name)
            return 0
    
        #if file size less than FILE_SIZE_BOUNDARY, to remove list
        if (file_size < FILE_SIZE_BOUNDARY*1024*1024):
            self.list_for_remove.append(file_name)
            logging.info('File size less than %s MB, remove it', 
                    FILE_SIZE_BOUNDARY)
            return 0
    
        #if else, put it in unclassify list
        self.list_for_unclassify.append([file_name, file_size])
        return 1
    
    
    
    
    
    def precheck(self):
        """ Check before everything"""
        if not os.path.isdir(self.source_dir):
            logging.warn('Source direcotry '+ self.source_dir + ' is invalid')
            return 1

        if not os.path.isdir(self.dest_dir):
            logging.warn('Destination directory '+ self.dest_dir + 
                         ' is invalid')
            return 1

        return 0



    
    def get_file_lists(self):
        """Loop over all the directories/sub-directories to find all files
           Store absolute file name to different temporary files according
           to different file format
           """
        
        directories = [self.source_dir]
        while len(directories)!= 0:
    
            current_dir = directories.pop()
            os.chdir(current_dir)
            os.stat(self.source_dir).st_dev

            for elem in os.listdir(current_dir):
                if os.path.isfile(elem):
                    #logging.debug( elem + ' is file')
                    self.classify_files(os.path.abspath(elem))

                elif os.path.isdir(elem):
                    #logging.debug( elem + ' is directory')
                    directories.append(os.path.abspath(elem))
                else:
                    logging.warn(elem + ' is either file or directory')
    

    


    def move_files(self):
        """ Move the files"""

        #delete/move the file when classify it is a little 'rude'
        #store their absolute names into files first
    
        dir_video = self.dest_dir + '/video'
        if not os.path.exists(dir_video):
            os.makedirs(dir_video)
    
        while len(self.list_for_video) != 0:
            try:
                elem = self.list_for_video.pop()
                try_move(elem[0], dir_video)
            except Exception, msg:
                logging.warn('Error when move file' + 
                             msg)
                logging.warn('Continuing')
                continue

           
   
def main ():
    """This the input of this tool script """

    init_logging()
    

    directory1 = DirecotryClean()
    directory1.source_dir = SOURCE_DIR
    directory1.dest_dir = DESTINATION_DIR

    instance_list = []
    instance_list.append(directory1)
    #sedond instance
    #third instance





    for instance in instance_list:
        if (1 == instance.precheck()):
            logging.warn('Invalid init data, skip')
            instance_list.remove(instance)
            continue



        instance.get_file_lists()



    logging.info('Start to move the files')

    for instance in instance_list:
        instance.move_files()







if __name__ == '__main__':
    main ()
# need to remember the source device and destination devide, in tunple? 
# or global variable

