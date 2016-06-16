#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

def init(args):
    print args

def start(args):
    print args

def stop(args):
    print args

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'to be completed')
    args = parser.parse_args()

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