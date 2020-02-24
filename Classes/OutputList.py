import datetime
from Classes import Host

host = Host.Host()
splitter = "#########################################################"


class OutputList:
    def __init__(self):
        self.count_of_good_hosts = 0

    @staticmethod
    def write_data(io, data):
        io.write_data_to_file(data, flag='a')

    @staticmethod
    def prepare_data_to_write(line, host):
        now = datetime.datetime.now()
        new_line = "Mikrotik " + line[2] + " " + str(now.strftime("%d-%m-%Y %H:%M:%S")) + '\n\n'
        for line in host.lines:
            if not line.isspace():
                new_line += line.replace('\n', '')
        new_line += splitter + " \n"
        return new_line
