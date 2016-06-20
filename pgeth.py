#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import argparse
import subprocess
import json
import os
import shutil
import logging

# const in python
PIDFILE = "/tmp/geth.pid"

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

def checkExe(path):
    """Check the path exists and it is a file"""
    if not os.path.exists(path):
        return False
    if not os.path.isfile(path) and os.access(path, os.X_OK):
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
        if checkExe(geth):
            return geth
        sys.stderr.write("invalid geth path in config file\n")
        sys.exit(-1)
    stdpaths = [ "/usr/bin/geth", "/usr/local/bin/geth", "/opt/local/bin/geth" ]
    for p in stdpaths:
        if checkExe(p):
            return p
    sys.stderr.write("no geth found in classic path. Use the geth param in the config file\n")
    sys.exit(0)

def test(args):
    checkIfGethIsRunning()

def destroyPrivateBlochain():
    """Destroy your private blockchain"""
    datadir = getDataDir()
    if not checkDir(datadir):
        sys.stderr.write("nothing to destroy. There is no %s directory\n" % datadir)
        sys.exit(-1)
    chaindata = os.path.os.path.join(datadir, "chaindata")
    keystore = os.path.os.path.join(datadir, "keystore")
    dapp = os.path.os.path.join(datadir, "dapp")
    nodekey = os.path.os.path.join(datadir, "nodekey")
    dsstore = os.path.os.path.join(datadir, ".DS_Store")
    ipcfile = os.path.os.path.join(datadir, "geth.ipc")
    if checkDir(chaindata):
        shutil.rmtree(chaindata)
    if checkDir(keystore):
        shutil.rmtree(keystore)
    if checkDir(dapp):
        shutil.rmtree(dapp)
    if checkDir(dsstore):
        shutil.rmtree(dsstore)
    if checkFile(nodekey):
        os.remove(nodekey)
    if checkFile(ipcfile):
        os.remove(ipcfile)
    try:
        os.rmdir(datadir)
    except:
        sys.stderr.write("We do not destroy %s directory because there is something not standard in it.\nRemove the directory after checks" % datadir)
        sys.exit(-1)

def initAccount():
    """List accounts. Create a default one if there is none"""
    datadir = getDataDir()
    geth = checkGethCommand()
    options = [ "--datadir", datadir ]
    cmdListAccounts = [ geth ] + options + ["account", "list"]
    print "cmd: " + str(cmdListAccounts)
    res = subprocess.check_output(cmdListAccounts)
    accountQty = len(res.split('\n')) - 1
    # check account qty
    if accountQty > 0:
        return
    # create mypassword.txt
    f = open("mypassword.txt", "w")
    f.write(load_config_keys("password"))
    f.close()
    # create an account
    cmdCreateAccount = [ geth ] + options + [ "--password", "mypassword.txt", "account", "new" ]
    print "cmd: " + str(cmdCreateAccount)
    subprocess.call(cmdCreateAccount)
    ## geth --networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none --datadir=~/myblockchain/node1 account new

def init(args):
    """init command"""
    # account management
    initAccount()
    # init needed if there is no chaindata dir
    datadir = getDataDir()
    if checkDir(os.path.join(datadir, 'chaindata')):
        return
    geth = checkGethCommand()
    options = [ "--datadir", datadir ]
    # launch the blockchain with the CustomGenesis.json file
    cmdInit = [ geth ] + options + [ "init", "pgeth_config.json"]
    print "cmd: " + str(cmdInit)
    subprocess.call(cmdInit) 

def checkIfGethIsRunningByGrep():
    """Check if there is a geth running"""
    try:
        res = subprocess.check_output("ps ax | grep 'geth ' | grep -v \"grep\"", shell=True)
        processQty = len(res.split('\n')) - 1
        return True
    except subprocess.CalledProcessError:
        return False

def checkIfGethIsRunning():
    """Check if there is a geth running"""
    if checkFile(PIDFILE):
        return True
    return False


def start(args):
    """ doc """
    # check if there is a PID File
    if checkIfGethIsRunning():
        sys.stderr.write("geth must already be running (If not remove the %s file)\n" % PIDFILE)        
        sys.exit(1)
    # start geth with mining
    datadir = load_config_keys("datadir")
    geth = checkGethCommand()
    options = [ "--datadir", datadir, "--dev", "--networkid", "100", "--nodiscover", "--nat", "none", "--mine", "--minerthreads", "1" ]
    cmdStart = [ geth ] + options
    print "cmd: " + str(cmdStart)
    logfile = open("geth.logs", "w")
    process = subprocess.Popen(cmdStart, stdout=logfile, stderr=logfile)
    # write the the pid file
    pidfile = open(PIDFILE, "w")
    pidfile.write(str(process.pid))
    pidfile.close()
    print "geth starting"

def stop(args):
    # check if there is a PID File
    if not checkIfGethIsRunning():
        sys.stderr.write("geth not running (because there is no %s file)\n" % PIDFILE)        
        sys.exit(1)
    # read the pid file
    pidfile = open(PIDFILE, "r")
    text = pidfile.read()
    pidfile.close()
    try:
        pid = int(text)
    except e:
        sys.stderr.write("Invalid %s file)\n" % PIDFILE)
    try:
        os.kill(pid, 1)
    finally:
        os.remove(PIDFILE)
    print "geth stopping"

    

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