#!/usr/bin/env python

import sys
import argparse
import OpenSSL
import socket

def verify_callback(connection, x509, err_num, err_depth, ret_code):
    if err_num == 0:
        if err_depth != 0:
            print var_args
            if var_args["crlfile"] and not var_args["pinnedcertificate"]:
                if x509.get_serial_number() in serial_list:
                    sys.stderr.write("Certificate serial number is in CRL!\n")
                    return False
            return True
        else:
            if var_args["pinnedcertificate"]:
                cert_file = open(var_args['pinnedcertificate'], "rb").read()
                certificate = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_file)
                if certificate.digest("sha256") != x509.digest("sha256"):
                    sys.stderr.write("Certificate does not match pinned certificate!\n")
                    return False
            return True
    return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tlsv1.0", action="store_true")
    parser.add_argument("--tlsv1.1", action="store_true")
    parser.add_argument("--tlsv1.2", action="store_true")
    parser.add_argument("--sslv3", action="store_true")
    parser.add_argument("-3",action="store_true")
    parser.add_argument("--ciphers")
    parser.add_argument("--pinnedcertificate")
    parser.add_argument("--crlfile")
    parser.add_argument("url")
    args = parser.parse_args()
    global var_args
    var_args = vars(args)

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
    context.set_verify(OpenSSL.SSL.VERIFY_PEER | OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify_callback)
    # Check for cipher list and handle appropriately
    if var_args["ciphers"]:
        try:
            context.set_cipher_list(var_args["ciphers"])
        except:
            context = OpenSSL.SSL.Context(method)
    if var_args["crlfile"]:
        crl_file = open(var_args["crlfile"], "rb").read()
        crl = OpenSSL.crypto.load_crl(OpenSSL.crypto.FILETYPE_PEM, crl_file)
        global serial_list
        serial_list = [x.get_serial() for x in crl.get_revoked()]

    connection = OpenSSL.SSL.Connection(context, socket.socket())
    connection.connect((var_args["url"], 443)) # default 443
    try:
        connection.do_handshake()
    except:
        sys.exit(-1)
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