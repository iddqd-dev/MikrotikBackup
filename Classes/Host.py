import socket
import sys
import ftplib
from ipaddress import IPv4Address as ip_addr
from Classes import Config as cfg
from Classes import Scripts as sc

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
        self.stdout_ = None
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
            print('Wrong data in line:', line)
            return False

    def extract_host_data_from_line(self, data):
        self.user = data[0]
        self.password = data[1]
        self.ip = data[2]
        self.port = data[3]
        return True

    def ssh_connection(self, script):
        try:
            cfg.ssh.connect(hostname=self.ip, username=self.user, password=self.password, port=self.port, timeout=5,
                            look_for_keys=False)
            print('Connected to host', self.ip, '\nAccess time to host:', self.access_time(), 'seconds')
            stdin_, stdout_, stderr_ = cfg.ssh.exec_command(script)
            stdout_.channel.recv_exit_status()
            self.stdout_ = stdout_
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
            print(err)
            return False
        finally:
            cfg.ssh.close()

    def check_firmware_version(self):
        lines = []
        try:
            self.ssh_connection(sc.get_info)
            for line in self.stdout_.read().splitlines():
                lines.append(line)
            try:
                cfg.mikrotik_name = str(lines[0])[2:-1]
                cfg.mikrotik_arch = str(lines[1])[2:-1]
                cfg.mikrotik_fw = str(lines[2])[2:-1]
                if "bad', b'command', b'name', b'routerboard'," in cfg.mikrotik_fw:
                    cfg.mikrotik_fw = "noRouterboardVersion"
            except Exception as e:
                cfg.mikrotik_fw = "'wrongData'"
                print(e)
            print(cfg.mikrotik_fw, cfg.mikrotik_arch, cfg.mikrotik_name)
        except socket.timeout:
            print("sorry")
        return True

    def folder_generation(self):
        ftp = ftplib.FTP(cfg.ftp_addr, cfg.ftp_user, cfg.ftp_password)
        try:
            ip_addr(self.ip)
            try:
                ftp.cwd(cfg.mikrotik_name)
            except ftplib.error_perm as err:
                if "550" in str(err):
                    ftp.mkd(cfg.mikrotik_name)
                    print("Directory was not found and was created.")
        except ValueError:
            print(self.ip + " is not valid ip address")
            return False
        return True

    def connect_to_host(self):
        try:
            self.ssh_connection(sc.backup_script)
            self.lines = self.stdout_.readlines()
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
            print(err)
            return False
        finally:
            cfg.ssh.close()

    def check_host(self, line):
        if self.extract_host_data_from_line(line):
            print("Trying to connect to %s" % self.ip)
            self.connect_to_host()
            return True
        else:
            print("Error")
            return False
