#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2012, 2015-2016 IOPixel SAS
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__version__ = '1.0.0'

"""
Create Private Ethereum Blockchain
 by ellis2323 & regispietra
 https://github.com/regispietra/CreatePrivateEthereum

This script pilots geth to provide easy functions:

* ./pgeth.py init
   this function create the blockchain with an account

* ./pgeth.py start
   this function starts geth daemon and mining. When it has started, you could use your Ethereun Wallet to see
   contracts and tokens.

* ./pgeth.py stop
    this functions stops geth

* ./pgeth.py destroy
   A function to delete quickly your private blockchain.

"""


import sys
import argparse
import subprocess
import json
import os
import shutil
import logging
import platform
import re

# const in python
PIDFILE = "/tmp/geth.pid"

# alloc with 1000 ethers
GENESIS = u"""{
"bordel": "fds",
  "nonce": "0xdeadbeefdeadbeef",
  "timestamp": "0x0",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "extraData": "0x00",
  "gasLimit": "0x8000000",
  "difficulty": "0x400",
  "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "coinbase": "0x0000000000000000000000000000000000000000",
  "alloc": {
      "0x$ADDRESS$": { "balance": "1000000000000000000000" }
  }
}"""

def load_config_keys(key):
    """ doc """
    try:
        file = open("pgeth_config.json", "r")
        txt = file.read()
        file.close()
        d = json.loads(txt)
    except:
        logging.error("invalid config file")
        logging.error("please use and modify the pgeth_config.json (https://github.com/regispietra/CreatePrivateEthereum)")
        sys.exit(-1)
    if d.has_key(key):
        return d[key]
    return None

def getDataDir():
    """Load datadir key and expand it"""
    datadir = load_config_keys("datadir")
    datadir = os.path.expanduser(datadir)
    return datadir

def getIpcDir():
    """Create default ipc path"""
    pl = platform.system()
    ipcdir = "~/.ethereum/geth.ipc"
    if pl == "Darwin":
        ipcdir = "~/Library/Ethereum/geth.ipc"
    elif pl == "Windows":
        ipcdir = "~/AppData/Roaming/Ethereum/geth.ipc"
    elif pl == "Linux":
        ipcdir = "~/.ethereum/geth.ipc"
    else:
        logging.error('Platform unknown %s. Contact devs at iopixel dot com', platform)
        sys.exit(-1)
    ipcdir = os.path.expanduser(ipcdir)
    return ipcdir

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
        logging.error("invalid geth path in config file")
        sys.exit(-1)
    stdpaths = [ "/usr/bin/geth", "/usr/local/bin/geth", "/opt/local/bin/geth" ]
    for p in stdpaths:
        if checkExe(p):
            return p
    logging.error("no geth found in classic path. Use the geth param in the config file")
    sys.exit(0)

def test(args):
    getAddress()

def destroyPrivateBlochain():
    """Destroy your private blockchain"""
    datadir = getDataDir()
    if not checkDir(datadir):
        logging.error("nothing to destroy. There is no %s directory" % datadir)
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
        logging.error("We do not destroy %s directory because there is something not standard in it.\nRemove the directory after checks" % datadir)
        sys.exit(-1)

def getAddress():
    """Get the address of the account 0"""
    datadir = getDataDir()
    geth = checkGethCommand()
    options = [ "--datadir", datadir ]
    cmdListAccounts = [ geth ] + options + ["account", "list"]
    logging.debug("cmd: " + str(cmdListAccounts))
    res = subprocess.check_output(cmdListAccounts)
    accountQty = len(res.split('\n')) - 1
    if accountQty == 0:
        return None
    line = res.split('\n')[0]
    regexp = re.search(u"{([0-9abcdefABCDEF]+)}", line)
    if regexp == None:
        logging.error("No address found in keystore")
        sys.exit(-1)
    result = regexp.group(1)
    logging.debug('adress found: 0x' + result)
    return result


def initAccount():
    """List accounts. Create a default one if there is none"""
    datadir = getDataDir()
    geth = checkGethCommand()
    options = [ "--datadir", datadir ]
    cmdListAccounts = [ geth ] + options + ["account", "list"]
    logging.debug("cmd: " + str(cmdListAccounts))
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
    logging.debug("cmd: " + str(cmdCreateAccount))
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
    options = [ "--datadir", datadir, "--networkid", "100" ]
    # create the json genesis
    address = getAddress()
    txt = GENESIS.replace("$ADDRESS$", address)
    f = open("genesis.json", "w")
    f.write(txt)
    f.close()
    # launch the blockchain with the CustomGenesis.json file
    cmdInit = [ geth ] + options + [ "init", "genesis.json"]
    logging.debug("cmd: " + str(cmdInit))
    subprocess.call(cmdInit) 

def checkIfGethIsRunningByGrep():
    """Check if there is a geth running"""
    try:
        cmd = "ps ax | grep 'geth ' | grep -v \"grep\""
        logging.debug(cmd)
        res = subprocess.check_output(cmd, shell=True)
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
        logging.error("geth must already be running (If not remove the %s file)" % PIDFILE)        
        sys.exit(1)
    # start geth with mining
    datadir = load_config_keys("datadir")
    geth = checkGethCommand()
    options = [ "--datadir", datadir, "--networkid", "100", "--nodiscover", "--nat", "none", "--mine", "--minerthreads", "1", "--ipcpath", getIpcDir() ]
    cmdStart = [ geth ] + options
    logging.debug("cmd: " + str(cmdStart))
    logfile = open("geth.logs", "w")
    process = subprocess.Popen(cmdStart, stdout=logfile, stderr=logfile)
    # write the the pid file
    pidfile = open(PIDFILE, "w")
    pidfile.write(str(process.pid))
    pidfile.close()
    logging.info("geth starting")

def stop(args):
    # check if there is a PID File
    if not checkIfGethIsRunning():
        logging.error("geth not running (because there is no %s file)" % PIDFILE)        
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
    logging.info("geth stopping")

    

def destroy(args):
    destroyPrivateBlochain()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S')

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