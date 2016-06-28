#! /usr/bin/python
"""This script is used for ....."""
import os
import logging
import shutil

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


def is_same_file (src, dst):
    """Compare two files, to see if there are same"""

    #md5 sum is better
    if os.path.exists (dst):
        return 1

    if os.path.exists (src):
        return 0


def try_move(src, dst):
    """If the src and dst are on same device/partion, move it directly
    If not, copy the file, if successful, delete the source file"""

    logging.debug('Moving file ' + src)

    destinate_file_name = dst + '/' + os.path.basename(src)


    if (1 == is_same_file(src, destinate_file_name)):
        logging.warn('Same file exists on target directory: '+ src)
        return 1

    shutil.move (src, destinate_file_name)
    return 0


def move_files(file_list, dst_dir):
    """ Move the files"""

    #delete/move the file when classify it is a little 'rude'
    #store their absolute names into files first
    logging.debug ('Move files to ' +dst_dir)
    no_move = False
    while len(file_list) != 0:
        elem = file_list.pop()

        if (no_move == True):
            logging.warn('File not move:' + elem)
            continue

        try:
            try_move(elem, dst_dir)
        except Exception:
            logging.warn('Error when move file ' +elem )
            no_move = True


class DirecotryClean:
    """ This is the main class for this tool"""


    def __init__ (self, src, dst):
        """ nothing need to do here"""
        self.source_dir = src
        self.dest_dir = dst
        self.dir_video = self.dest_dir + '/video'
        self.dir_torrent = self.dest_dir + '/torrent'
        self.list_for_video = []
        self.list_for_remove = []
        self.list_for_torrent = []
        self.list_for_unclassify = []


    def classify_files(self, file_name):
        """Classify files according their name format, suffix etc."""

        #get suffix of file
        suffix = os.path.splitext(file_name)[1]

        #if file is suffix with '.torrent'
        if suffix == '.torrent':
            self.list_for_torrent.append(file_name)
            logging.debug('File is torrent file')
            return 0



        #if file is suffix with FILE_FORMATE_LIST
        if (suffix in FILE_FORMATE_LIST) or \
        (suffix.lower() in FILE_FORMATE_LIST):
            self.list_for_video.append(file_name)
            logging.info('Video file:' + file_name)
            return 0

        file_size = os.path.getsize(file_name)
        #if file size less than FILE_SIZE_BOUNDARY, to remove list
        if (file_size < FILE_SIZE_BOUNDARY*1024*1024):
            self.list_for_remove.append(file_name)
            logging.info('File size less than %s MB, remove it',
                    FILE_SIZE_BOUNDARY)
            return 0

        #if else, put it in unclassify list
        self.list_for_unclassify.append(file_name)
        return 0


    def precheck(self):
        """ Check before everything"""
        if not os.path.isdir(self.source_dir):
            logging.warn('Source direcotry '+ self.source_dir + ' is invalid')
            return 1

        if not os.path.isdir(self.dest_dir):
            logging.warn('Destination directory '+ self.dest_dir +
                         ' is invalid')
            return 1

        try:

            if not os.path.exists(self.dir_video):
                os.makedirs(self.dir_video)
            if not os.path.exists(self.dir_torrent):
                os.makedirs(self.dir_torrent)
        except Exception:
            logging.warn('Create destination directory failed')
            return 1

        return 0




    def get_file_lists(self):
        """Loop over all the directories/sub-directories to find all files.
           Store absolute file name to different list according to different 
           file format """

        directories = [self.source_dir]
        while len(directories)!= 0:

            current_dir = directories.pop()
            os.chdir(current_dir)
            os.stat(self.source_dir).st_dev

            for elem in os.listdir(current_dir):
                if os.path.isfile(elem):
                    self.classify_files(os.path.abspath(elem))

                elif os.path.isdir(elem):
                    directories.append(os.path.abspath(elem))
                else:
                    logging.warn(elem + ' is either file or directory')



    def move_all_types_files(self):
        """Move all kinds of files, video, torrent, etc."""
        move_files(self.list_for_video, self.dir_video)
        move_files(self.list_for_torrent, self.dir_torrent)


def main ():
    """This the input of this tool script """

    init_logging()

    directory1 = DirecotryClean('/home/peterqi/DirectoryClean_test',
                                '/home/peterqi/DirectoryClean_test')

    directory2 = DirecotryClean('/home/peterqi/DirectoryClean_test11',
                                '/home/peterqi/DirectoryClean_test11')


    instance_list = []
    instance_list.append(directory1)
    instance_list.append(directory2)

    for instance in instance_list:
        if (1 == instance.precheck()):
            logging.warn('Precheck failed for %s, skip',
                         directory1.source_dir)
            instance_list.remove(instance)
            continue
        instance.get_file_lists()

    for instance in instance_list:
        print instance
        instance.move_all_types_files()



if __name__ == '__main__':
    main ()
