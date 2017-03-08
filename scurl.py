#!/usr/bin/env python

import sys
import argparse
import OpenSSL
import socket

def t1():
    print "in t1"

def t2():
    print "in t2"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tlsv1.0", action="store_true")
    parser.add_argument("--tlsv1.1", action="store_true")
    parser.add_argument("--tlsv1.2", action="store_true")
    parser.add_argument("--sslv3", action="store_true")
    parser.add_argument("-3",action="store_true")
    args = parser.parse_args()
    var_args = vars(args)

    if var_args["tlsv1.0"]:
        t1()
    else:
        t2()

    # Create socket and context, and setup connection
    context = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD) # method defined by command line options
    connection = OpenSSL.SSL.Connection(context, socket.socket())
    connection.connect(("www.google.com", 443)) # defualt 443
    connection.do_handshake()

    # Verify cert chain
    # connection.get_client_ca_list()


if __name__ == '__main__':
    main()