import socket, paramiko
from timeit import default_timer as timer


class Host:
    def __init__(self):
        self.lines = None
        self.user = None
        self.password = None
        self.ip = None
        self.port = None
        self.start_time = timer()
        self.host_access_time = 0

    def access_time(self):
        self.host_access_time = timer() - self.start_time
        return round(self.host_access_time, 2)

    @staticmethod
    def check_host_data(line):
        print('Checking data of host', line[2])
        if len(line) == 4:
            return True
        else:
            print('no valid data in line')
            return False

    def extract_host_data_from_line(self, data):
        self.user = data[0]
        self.password = data[1]
        self.ip = data[2]
        self.port = data[3]
        return True

    def connect_to_host(self):
        ftp = "your-ftp-address"
        backup_script = ':global thisdate [/system clock get date]; ' \
                        ':global datetimestring ([:pick $thisdate 0 3] ."-" . [:pick $thisdate 4 6] ."-" . [:pick $thisdate 7 11]);' \
                        ':global backupfilename ([/system identity get name]."_".$datetimestring); ' \
                        '/system backup save name="$backupfilename";' \
                        ':delay 5s;' \
                        ' /export compact file="$backupfilename";' \
                        '/tool fetch address="' + ftp + '" src-path="$backupfilename.backup" user="mikrotik" password="mikrotik" port=21 upload=yes mode=ftp dst-path="$backupfilename.backup";' \
                                                        ':delay 1;' \
                                                        '/tool fetch address="' + ftp + '" src-path="$backupfilename.rsc" user="mikrotik" password="mikrotik" port=21 upload=yes mode=ftp dst-path="$backupfilename.rsc";' \
                                                                                        ':delay 1;' \
                                                                                        '/file remove "$backupfilename.backup";' \
                                                                                        '/file remove "$backupfilename.rsc";' \
                                                                                        ':log'' info "Finished Backup Script…!!!!";'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.user, password=self.password, port=self.port, timeout=5,
                        look_for_keys=False)
            print('Connected to host', self.ip, 'Access time to host:', self.access_time(), 'seconds')
            stdin_, stdout_, stderr_ = ssh.exec_command(backup_script)
            stdout_.channel.recv_exit_status()
            self.lines = stdout_.readlines()
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to", self.ip)
            print('Host marked as bad.')
            return False
        except ConnectionError:
            print("Could not connect to %s" % self.ip)
            return False
        except socket.timeout:
            print('Timed out!')

    def check_host(self, line):
        if self.extract_host_data_from_line(line):
            print("Trying to connect to %s" % self.ip)
            self.connect_to_host()
            return True
        else:
            return False
