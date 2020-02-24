#!/usr/bin/python
import sys
import datetime
import argparse
from timeit import default_timer as timer
from Classes import InputOutput, InputList, Host, OutputList

splitter = "#########################################################"
start_time = timer()


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
    print(splitter)
    print("Failed:", input_list.bad_host_count, "backup's.", 'Completed:', output_list.count_of_good_hosts, "backups's.")
    print(splitter)
    full = timer() - start_time
    print("Full backup in", round(full, 2), "second's.")
    print(splitter)


if __name__ == "__main__":
    main()
