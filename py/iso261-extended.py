#!/usr/bin/env python
'''
Created on 26 Dec 2012

@author: bruno
'''

import sys
import argparse
import csv
import re

import iso261


def load_csv(datain):
    data = []
    ipattern = re.compile('[0-9]+')
    fpattern = re.compile('[0-9]+\.[0-9]+')
    reader = csv.reader(datain)
    last_dia = 0
    current_entry = {}
    for row in reader:
        if fpattern.match(row[0]):
            dia = float(row[0])
        elif ipattern.match(row[0]):
            dia = int(row[0])
        else:
            continue
        if dia != last_dia:
            current_entry = {
                'D': dia
            }
            current_entry['P'] = []
            if row[1] == row[2]:
                current_entry['extended'] = True
            data.append(current_entry)
            last_dia = dia
        current_entry['P'].append(float(row[3]))
    return data


def process(datain, dataout, produce_json=False, precision=5, license=''):
    data = load_csv(datain)
    iso261.process_data(data, dataout, produce_json, precision, license)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Produce OpenSCAD modules to
                                     generate screws that follow an extension
                                     of the ISO 261 standard''')
    parser.add_argument('-j', '--json', action='store_true',
                        help="Produce JSON output rather than OpenSCAD")
    parser.add_argument('-d', '--decimals', type=int, default=5,
                        help='''Number of decimals to use in OpenSCAD output,
                        ignored if JSON output is specified''')
    parser.add_argument('-l', '--license', default='',
                        help='''Specify the license header to user, if any.''')
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    args = parser.parse_args()
    if args.input is None or args.input == '-':
        datain = sys.stdin
    else:
        datain = open(args.input, 'r')
    if args.output is None:
        dataout = sys.stdout
    else:
        dataout = open(args.output, 'w')
    process(datain, dataout, args.json, args.decimals, args.license)
