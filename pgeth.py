#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import argparse
import subprocess
import json
import os

def load_config_keys(key):
    """ doc """
    file = open("pgeth_config.json", "r")
    txt = file.read()
    file.close()
    d = json.loads(txt)
    return d[key]

def initAccount():
    """List accounts. Create a default one if there is none"""
    datadir = load_config_keys("datadir")
    str_geth = "geth"
    str_options = " --datadir=" + datadir + " "
    cmdListAccounts = str_geth + str_options + " account list"
    print "cmd: " + cmdListAccounts
    res = subprocess.check_output(cmdListAccounts, shell=True)
    accountQty = len(res.split('\n')) - 1
    # check account qty
    if accountQty > 0:
        return
    # create an account
    cmdCreateAccount = str_geth + str_options + " --password mypassword.txt account new"
    print "cmd: " + cmdCreateAccount
    subprocess.call(cmdCreateAccount, shell=True)
    ## geth --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none --datadir=~/myblockchain/node1 account new

def init(args):
    """doc3S"""
    # account new
    initAccount()
    datadir = load_config_keys("datadir")
    str_options = " --verbosity 3 --datadir=" + datadir + " "
    # launch the blockchain with the CustomGenesis.json file
    cmdInit = "geth" + str_options + " init" + " pgeth_config.json"
    print "cmd: " + cmd
    subprocess.call(cmd, shell = True) 

def start(args):
    """ doc """
    datadir = load_config_keys("datadir")
    str_datadir = " --datadir=" + datadir + " "
    str_options =  " --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none "
    str_args = "geth " + str_datadir + str_options + "account new"
    cmd = "geth" + str_options + str_datadir + " --mine" + " --ipcpath ~/Library/Ethereum/geth.ipc"
    print cmd
    subprocess.call(cmd, shell = True)

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