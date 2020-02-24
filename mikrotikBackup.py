#!/usr/bin/python
import sys
import datetime
import argparse
from Classes import InputOutput, InputList, Host, OutputList
splitter = "#########################################################"


def cmd_arg_parser():
    now = datetime.datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', default='mikrotik_list.txt')
    parser.add_argument('-o', '--output_file', default='' + str(now.strftime("%d-%m-%Y")) + '_logs.txt')
    return parser


def main():
    parser = cmd_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    input_f = namespace.input_file
    output_f = namespace.output_file
    output_list = OutputList.OutputList()
    input_list = InputList.InputList()
    host = Host.Host()
    io = InputOutput.InputOutput(input_f, output_f, input_list, output_list, host)
    input_list.handling_list(output_list, host, io)
    print('Failed:', input_list.bad_host_count, 'hosts.', 'Passed backups:', output_list.count_of_good_hosts, '\n' + splitter + '\n')


if __name__ == "__main__":
    main()
