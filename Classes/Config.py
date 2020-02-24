import sys

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

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ftp_addr = "192.168.1.1"
ftp_user = "mikrotik"
ftp_password = "mikrotik"
mikrotik_arch = ""
mikrotik_fw = ""
mikrotik_name = ""
