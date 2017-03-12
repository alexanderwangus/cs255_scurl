#!/usr/bin/env python

import sys
import argparse
import OpenSSL
import socket


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tlsv1.0", action="store_true")
    parser.add_argument("--tlsv1.1", action="store_true")
    parser.add_argument("--tlsv1.2", action="store_true")
    parser.add_argument("--sslv3", action="store_true")
    parser.add_argument("-3",action="store_true")
    parser.add_argument("--ciphers")
    parser.add_argument("--pinnedcertificate")
    parser.add_argument("url")
    args = parser.parse_args()
    var_args = vars(args)

    print var_args

    method = ""
    if var_args["tlsv1.0"]:
        method = OpenSSL.SSL.TLSv1_METHOD
    elif var_args["tlsv1.1"]:
        method = OpenSSL.SSL.TLSv1_1_METHOD
    elif var_args["tlsv1.2"]:
        method = OpenSSL.SSL.TLSv1_2_METHOD
    elif var_args["sslv3"]:
        method = OpenSSL.SSL.SSLv23_METHOD #SSLV3 might be deprecated in newest OpenSSL, switch back and test on corn
    elif var_args["3"]:
        method = OpenSSL.SSL.SSLv23_METHOD
    else:
        method = OpenSSL.SSL.TLSv1_2_METHOD

    # Create socket and context, and setup connection
    context = OpenSSL.SSL.Context(method) # method defined by command line options
    # Check for cipher list and handle appropriately
    if var_args["ciphers"]:
        try:
            context.set_cipher_list(var_args["ciphers"])
        except:
            context = OpenSSL.SSL.Context(method)

    connection = OpenSSL.SSL.Connection(context, socket.socket())
    connection.connect((var_args["url"], 443)) # default 443
    connection.do_handshake()
    connection.send("GET / HTTP/1.0\r\n" + var_args["url"] + "\r\nUser-Agent: CryptoGods\r\n\r\n")
    data = ""
    while True:
        try:
            new_data = connection.recv(8192)
            data += new_data
        except OpenSSL.SSL.Error:
            break

    connection.shutdown()
    connection.close()
    print data


    # Verify cert chain
    # connection.get_client_ca_list()


if __name__ == '__main__':
    main()