#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import subprocess

def init(args):
    """doc3S"""
    subprocess.call(["geth", "--networkid 100 --identity node1 --verbosity 3 --nodiscover --nat none init"])
    print args

def start(args):
    """ doc """
    print args

def stop(args):
    """ doc """
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