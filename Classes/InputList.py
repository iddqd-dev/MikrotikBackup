from datetime import datetime as time
from timeit import default_timer as timer
splitter = "#########################################################"


class InputList:
    def __init__(self):
        self.host_count = 0
        self.bad_host_count = 0
        self.current_line_count = 0

    def hosts_counter(self, io):
        now = time.now()
        print(splitter)
        print(str(now.strftime("%d-%m-%Y %H:%M:%S")) + '\nCounting host in file:', io.input_file)
        for _ in io.read_data_from_file(flag='r'):
            self.host_count += 1
        return self.host_count

    def handling_list(self, output_list, host, io):

        print('Found', self.hosts_counter(io), 'hosts in list of file', io.input_file)
        for line in io.read_data_from_file(flag='r'):
            self.current_line_count += 1
            print('\n' + splitter)
            check_result = host.check_host_data(line)
            if check_result:
                host.extract_host_data_from_line(line)
                host.check_firmware_version()
                host.folder_generation()
                start_time = timer()
                connection = host.connect_to_host()
                if connection:
                    print("Backup time:", round((timer() - start_time), 2))
                    prepare_data = output_list.prepare_data_to_write(line, host)
                    io.write_data_to_file(prepare_data, output_list, flag='a')
                else:
                    self.bad_host_count += 1
                    io.write_data_to_file("Connection error " + host.ip + ". See mikrotikBackup.log \n"
                                                       + splitter + "\n", output_list, flag='a')
            else:
                self.bad_host_count += 1
