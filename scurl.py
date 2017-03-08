#!/usr/bin/env python

import sys
import argparse

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

if __name__ == '__main__':
    main()