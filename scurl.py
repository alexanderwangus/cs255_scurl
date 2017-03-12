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
    connection.send("GET / HTTP/1.0\r\nHost: www.google.com\r\nUser-Agent: CryptoGods\r\n\r\n")
    data = ""
    while True:
        try:
            new_data = connection.recv(8192)
            data += new_data
        except OpenSSL.SSL.Error:
            break
    print data
    connection.shutdown()
    connection.close()
    print data


    # Verify cert chain
    # connection.get_client_ca_list()


if __name__ == '__main__':
    main()