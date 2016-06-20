#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import argparse
import subprocess
import json
import os
import shutil

def load_config_keys(key):
    """ doc """
    try:
        file = open("pgeth_config.json", "r")
        txt = file.read()
        file.close()
        d = json.loads(txt)
    except:
        sys.stderr.write("invalid config file\n")
        sys.exit(-1)
    if d.has_key(key):
        return d[key]
    return None

def getDataDir():
    """Load datadir key and expand it"""
    datadir = load_config_keys("datadir")
    datadir = os.path.expanduser(datadir)
    return datadir

def checkDir(path):
    """Check the path exists and it is a directory"""
    if not os.path.exists(path):
        return False
    if not os.path.isdir(path):
        return False
    return True

def checkFile(path):
    """Check the path exists and it is a file"""
    if not os.path.exists(path):
        return False
    if not os.path.isfile(path) and os.access(path, os.X_OK):
        return False
    return True

def checkGethCommand():
    """Search Geth command"""
    geth = load_config_keys("geth")
    if geth:
        if checkFile(geth):
            return geth
        sys.stderr.write("invalid geth path in config file\n")
        sys.exit(-1)
    stdpaths = [ "/usr/bin/geth", "/usr/local/bin/geth", "/opt/local/bin/geth" ]
    for p in stdpaths:
        if checkFile(p):
            return p
    sys.stderr.write("no geth found in classic path. Use the geth param in the config file\n")
    sys.exit(0)

def test(args):
    print checkGethCommand()

def destroyPrivateBlochain():
    """Destroy your private blockchain"""
    datadir = getDataDir()
    if not checkDir(datadir):
        sys.stderr.write("nothing to destroy. There is no %s directory\n" % datadir)
        sys.exit(-1)
    chaindata = os.path.os.path.join(datadir, "chaindata")
    keystore = os.path.os.path.join(datadir, "keystore")
    if checkDir(chaindata):
        shutil.rmtree(chaindata)
    if checkDir(keystore):
        shutil.rmtree(keystore)
    os.rmdir(datadir)

def initAccount():
    """List accounts. Create a default one if there is none"""
    datadir = getDataDir()
    str_geth = "/usr/local/bin/geth"
    str_options = " --datadir=" + datadir + " "
    cmdListAccounts = str_geth + str_options + " account list"
    print "cmd: " + cmdListAccounts
    res = subprocess.check_output([ "/usr/local/bin/geth", "--datadir", datadir, "account", "list"])
    print res
    sys.exit(1)
    accountQty = len(res.split('\n')) - 1
    # check account qty
    if accountQty > 0:
        return
    # create mypassword.txt
    f = open("mypassword.txt", "w")
    f.write(load_config_keys("password"))
    f.close()
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
    print "cmd: " + cmdInit
    subprocess.call(cmdInit, shell = True) 

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

def destroy(args):
    destroyPrivateBlochain()

def testpython(args):
    testpython()

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

    destroy_parser = subparsers.add_parser('destroy')
    destroy_parser.set_defaults(func = destroy)

    test_parser = subparsers.add_parser('test')
    test_parser.set_defaults(func = test)


    args = parser.parse_args()
    args.func(args)  # call the default function