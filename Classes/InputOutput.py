from ipaddress import IPv4Address as ip_addr


class InputOutput:
    def __init__(self, input_f, output_f, input_list, output_list, host):
        self.output_file = output_f
        self.input_file = input_f
        self.output_list = output_list
        self.input_list = input_list
        self.host = host

    def read_data_from_file(self, flag):
        try:
            with open(self.input_file, flag) as file:
                for line in file:
                    yield line.strip().split(' ')
        except IOError:
            print("can't read from file, IO error")
            exit(1)

    def write_data_to_file(self, line, output_list, flag):
        try:
            with open(self.output_file, flag) as file:
                file.write(line)
                try:
                    ip_addr(self.host.ip)
                    output_list.count_of_good_hosts += 1
                except ValueError:
                    pass
            return True
        except IOError:
            print("Can't write to output file, IO error")
            exit(1)
