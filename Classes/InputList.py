class InputList:
    def __init__(self):
        self.host_count = 0
        self.bad_host_count = 0
        self.current_line_count = 0

    def hosts_counter(self, io):
        print('Counting host in file:', io.input_file)
        for line in io.read_data_from_file(flag='r'):
            self.host_count += 1
        return self.host_count

    def handling_list(self, output_list, host, io):
        splitter = "#########################################################"
        print('Found', self.hosts_counter(io), 'hosts in list of file', io.input_file)
        for line in io.read_data_from_file(flag='r'):
            self.current_line_count += 1
            print('\n' + splitter)
            check_result = host.check_host_data(line)
            if check_result:
                host.extract_host_data_from_line(line)
                host.check_firmware_version()
                host.folder_generation()
                connection = host.connect_to_host()
                if connection:
                    prepare_data = output_list.prepare_data_to_write(line, host)
                    write_line = io.write_data_to_file(prepare_data, output_list, flag='a')
                    if write_line:
                        print('recorded line#', output_list.count_of_good_hosts, 'of', self.host_count)
                else:
                    self.bad_host_count += 1
                    write_line = io.write_data_to_file("Connection error " + host.ip + ". See mikrotikBackup.log \n"
                                                       + splitter + "\n", output_list, flag='a')
            else:
                self.bad_host_count += 1
