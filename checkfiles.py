import os

class WriteLog(object):
    def write_log(self, file_log):
        try:
            with open('.logs', 'w') as line:
                line.write(file_log)
        finally:
            line.close()

class CheckingFilesStrategy(object):
    def __init__(self, write_log):
        self.write_log = write_log
        self.file_count = 0

    def check_permissions_on_files(self, full_path):
        if not os.access(full_path, os.R_OK):
            if os.path.isfile(full_path):
                os.chmod(full_path, 0644)
            if os.path.isdir(full_path):
                os.chmod(full_path, 0755)
            self.write_log.write_log(full_path)

    def check_owner_files(self, full_path, user, group):
        import grp, pwd
        if pwd.getpwuid(os.stat(full_path).st_uid)[0] in user:
            os.chown(full_path, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
        if grp.getgrgid(os.stat(full_path).st_gid)[0] in group:
            os.chown(full_path, pwd.getpwnam(user).pw_uid, grp.getgrnam(group).gr_gid)
        self.write_log.write_log(full_path)

    def find_file_last_modification(self, full_path):
        import time
        last_mod_dic = []
        last_mod_dic.append(time.ctime(os.path.getmtime(full_path)))
        if last_mod_dic[0] < time.ctime(os.path.getmtime(full_path)):
            last_modified = full_path
        return full_path, "last modified: %s" % time.ctime(os.path.getmtime(full_path))

    def check_size_folder(self, full_path):
        return os.path.getsize(full_path)

    def check_how_many_files(self, full_path):
        if full_path:
            self.file_count += 1
        return self.file_count

class CheckingFiles(object):
    def __init__(self, CheckingFilesStrategy):
        self.CheckingFilesStrategy = CheckingFilesStrategy

    def checkFiles(self, home):
        for path, dir, files in os.walk(home):
            for value_dir in dir:
                full_path = os.path.join(path, value_dir)
                self.CheckingFilesStrategy.check_permissions_on_files(full_path)
                self.CheckingFilesStrategy.check_owner_files(full_path, 'ivanov', 'ivanov')
                self.CheckingFilesStrategy.find_file_last_modification(full_path)
                self.CheckingFilesStrategy.check_size_folder(full_path)
            for value_files in files:
                full_path = os.path.join(path, value_files)
                self.CheckingFilesStrategy.check_permissions_on_files(full_path)
                self.CheckingFilesStrategy.check_owner_files(full_path, 'ivanov', 'ivanov')
                self.CheckingFilesStrategy.find_file_last_modification(full_path)
                self.CheckingFilesStrategy.check_size_folder(full_path)
                self.CheckingFilesStrategy.check_how_many_files(full_path)

        print self.CheckingFilesStrategy.file_count

if __name__ == '__main__':
    createWriteLog = WriteLog()
    createCheckingFilesStrategy = CheckingFilesStrategy(createWriteLog)
    createCheckingFiles = CheckingFiles(createCheckingFilesStrategy)
    createCheckingFiles.checkFiles(os.getcwd())
