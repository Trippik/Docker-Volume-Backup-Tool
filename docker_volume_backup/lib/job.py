class Job:
    def __init__(self):
        self.filename = self.generate_file_name()


    def generate_file_name(self):
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = filename + ".tar.gz"
        return(filename)

    def create_backup_tar(self):
        with tarfile.open(self.filename, "w:gz") as tar:
            tar.add(vol_directory, arcname=os.path.basename(vol_directory))

    def save_file_ftp(self):
        session = ftplib.FTP(os.environ["STORAGE-SERVER"],os.environ['USERNAME'],os.environ['PASSWORD'])
        file = open(self.filename,'rb')
        session.storbinary('STOR ' + self.filename, file)
        file.close()
        session.quit()

    def save_file_sftp(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            dir_list= sftp.listdir()
            logging.error(dir_list)
            remoteFilePath = "/" + self.filename
            sftp.put(self.filename, remoteFilePath)


    def remove_old_files_ftp(self):
        logging.error("Automated deletion of backups is not yet supported using FTP")

    def remove_old_files_sftp(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=os.environ["STORAGE-SERVER"], username=os.environ['USERNAME'], password=os.environ['PASSWORD'], port=int(os.environ['PORT']), cnopts=cnopts) as sftp:
            max_no = int(os.environ["NUMBER-OF-BACKUPS"])
            dir_list= sftp.listdir()
            number_of_backups = len(dir_list)
            no_to_delete = number_of_backups - max_no
            count = 0 
            for file in dir_list:
                if(count < no_to_delete):
                    remoteFilePath = "/" + file
                    sftp.remove(remoteFilePath)
                count = count + 1

    def run(self):
        self.create_backup_tar()
        if mode == 'FTP':
            self.save_file_ftp()
            self.remove_old_files_ftp()
        elif mode == 'SFTP':
            self.save_file_sftp()
            self.remove_old_files_sftp()
        os.remove(self.filename)