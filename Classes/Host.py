import socket
import sys
import ftplib
from ipaddress import IPv4Address as ip_addr

try:
    import paramiko
except ImportError:
    print("""
#########################################################
paramiko module not found. Please install it.
pip install paramiko
or
apt-get install python-paramiko
#########################################################""")
    sys.exit(1)
from timeit import default_timer as timer


class Host:
    def __init__(self):
        self.mikrotik_arch = ""
        self.mikrotik_fw = ""
        self.mikrotik_name = ""
        self.lines = None
        self.user = None
        self.password = None
        self.ip = None
        self.port = None
        self.start_time = timer()
        self.host_access_time = 0
        self.err = None

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

    def check_mikrotik_name(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.user, password=self.password, port=self.port, timeout=5,
                        look_for_keys=False)
            print('Connected to host', self.ip, '\nAccess time to host:', self.access_time(), 'seconds')
            stdin_, stdout_, stderr_ = ssh.exec_command(":put [/system identity get name];")
            stdout_.channel.recv_exit_status()
            self.mikrotik_name = str(stdout_.readlines())[2:-6]
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to", self.ip)
            print('Check username and password.')
            return False
        except ConnectionError:
            print("Could not connect to %s" % self.ip)
            return False
        except socket.timeout as err:
            print(err)
            return False
        except Exception as err:
            self.err = err
            return False
        finally:
            ssh.close()
        return True

    def check_firmware_version(self):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.user, password=self.password, port=self.port, timeout=5,
                        look_for_keys=False)
            print('Connected to host', self.ip, '\nAccess time to host:', self.access_time(), 'seconds')
            stdin_, stdout_, stderr_ = ssh.exec_command(":put [system routerboard get current-firmware ]; :put [/system resource get architecture-name]")
            stdout_.channel.recv_exit_status()
            #s = stdout_.read().splitlines()
            s = [line.split() for line in stdout_.read().splitlines()]
            self.mikrotik_fw = str(s[0])[2:-1]
            self.mikrotik_arch = str(s[1])[2:-1]
            print(self.mikrotik_fw, self.mikrotik_arch)
            # self.mikrotik_fw = str(stdout_.readlines())[2:-6]
            # print(self.mikrotik_fw)
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to", self.ip)
            print('Check username and password.')
            return False
        except ConnectionError:
            print("Could not connect to %s" % self.ip)
            return False
        except socket.timeout as err:
            print(err)
            return False
        except Exception as err:
            self.err = err
            return False
        finally:
            ssh.close()
        return True

    def folder_generation(self):
        ftp = ftplib.FTP("192.168.1.12", "mikrotik", "mikrotik")
        try:
            ip_addr(self.ip)
            try:
                ftp.cwd(self.mikrotik_name)
            except ftplib.all_errors as err:
                ftp.mkd(self.mikrotik_name)
                print(err)
        except ValueError:
            print(self.ip + " is not valid ip address")
            return False
        return True

    def connect_to_host(self):
        ftp = "192.168.1.12"
        user = "mikrotik"
        password = "mikrotik"
        distance = str(self.mikrotik_name)
        backup_script = ':local time [/system clock get time];' \
                        ':local thisdate [/system clock get date]; ' \
                        ':local datetimestring ([:pick $thisdate 0 3] ."-" . [:pick $thisdate 4 6] ."-" . [:pick $thisdate 7 11]);' \
                        ':local backupfilename ([/system identity get name]."_'+ self.mikrotik_fw + "_" + self.mikrotik_arch +'_".$datetimestring."_".$time); ' \
                        '/system backup save name="$backupfilename";' \
                        ':delay 5s;' \
                        ' /export compact file="$backupfilename";' \
                        \
                        '/tool fetch address="' + ftp + '" src-path="$backupfilename.backup" user=' \
                        + user + ' password=' + password + ' port=21 upload=yes mode=ftp dst-path="' \
                        + distance + '/$backupfilename.backup";' \
                        \
                        ':delay 1;' \
                        \
                        '/tool fetch address="' + ftp + '" src-path="$backupfilename.rsc" user=' \
                        + user + ' password=' + password + ' port=21 upload=yes mode=ftp dst-path="' \
                        + distance + '/$backupfilename.rsc";' \
                        \
                        ':delay 1;' \
                        '/file remove "$backupfilename.backup";' \
                        '/file remove "$backupfilename.rsc";' \
                        ':log'' info "Finished Backup Script.";'
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.ip, username=self.user, password=self.password, port=self.port, timeout=5,
                        look_for_keys=False)
            print('Connected to host', self.ip, '\nAccess time to host:', self.access_time(), 'seconds')
            stdin_, stdout_, stderr_ = ssh.exec_command(backup_script)
            stdout_.channel.recv_exit_status()
            self.lines = stdout_.readlines()
            return True
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to", self.ip)
            print('Check username and password.')
            return False
        except ConnectionError:
            print("Could not connect to %s" % self.ip)
            return False
        except socket.timeout as err:
            print(err)
            return False
        except Exception as err:
            self.err = err
            return False
        finally:
            ssh.close()
        return True

    def check_host(self, line):
        if self.extract_host_data_from_line(line):
            print("Trying to connect to %s" % self.ip)
            self.connect_to_host()
            return True
        else:
            print("Error")
            return False
