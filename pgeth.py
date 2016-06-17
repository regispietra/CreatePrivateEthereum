#!/usr/bin/env python
# -*- coding: utf-8 -*-

## geth --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none --datadir=~/myblockchain/node1 account new

import sys
import argparse
import subprocess
import json
import os
from subprocess import Popen, PIPE, STDOUT

def load_config_keys(key):
    """ doc """
    file = open("pgeth_config.json", "r")
    txt = file.read()
    file.close()
    d = json.loads(txt)
    return d[key]

def init(args):
    """doc3S"""
    # account new + launch
    datadir = load_config_keys("datadir")
    str_datadir = " --datadir=" + datadir + " "
    str_options =  " --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none "
    str_args = "geth " + str_datadir + str_options 
    # create account using mypassword.txt
    subprocess.call("geth --password mypassword.txt account new", shell=True)
    # launch the blockchain with the CustomGenesis.json file
    subprocess.call("geth" + str_options + str_args + " init" + " pgeth_config.json", shell = True) 

def start(args):
    """ doc """
    datadir = load_config_keys("datadir")
    str_datadir = " --datadir=" + datadir + " "
    str_options =  " --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none "
    str_args = "geth " + str_datadir + str_options + "account new"
    subprocess.call("geth" + str_options + str_datadir + " mine" + " --ipcpath ~/Library/Ethereum/geth.ipc", shell = True)
    print args

def stop(args):
    
    print args

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = 'to be completed')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    init_parser = subparsers.add_parser('init')
    init_parser.set_defaults(func = init)

    start_parser = subparsers.add_parser('start')
    start_parser.set_defaults(func = start)

    stop_parser = subparsers.add_parser('stop')
    stop_parser.set_defaults(func = stop)

    args = parser.parse_args()
    args.func(args)  # call the default function