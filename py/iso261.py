#!/usr/bin/env python
'''
Created on 26 Dec 2012

@author: bruno
'''

import sys
import argparse
import json
import math

H_RATIO = math.cos(math.pi / 6)


def process(datain, dataout, produce_json=False, precision=5, license=''):
    data = json.load(datain)
    process_data(data, dataout, produce_json, precision, license)


def generate_specs(data):
    for s in data:
        dd = s['D']
        d = float(dd)
        r = d / 2
        pitches = s['P']
        extended = False
        if 'extended' in s:
            extended = s['extended']
        first = True
        for pp in pitches:
            p = float(pp)
            h = H_RATIO * p
            # Basic profile
            profile = [
                       {'x': -p/2,   'y': -5*h/8},
                       {'x': -3*p/8, 'y': -5*h/8},
                       {'x': -p/16,  'y':  0},
                       {'x':  p/16,  'y':  0},
                       {'x':  3*p/8, 'y': -5*h/8},
                       {'x':  p/2,   'y': -5*h/8}
                       ]
            name = 'M{0}x{1}'.format(
                                     str(dd).replace('.', '_'),
                                     str(pp).replace('.', '_')
                                     )
            os = {
                  'radius':  r,
                  'pitch':   p,
                  'profile': profile
                  }
            yield (name, os)
            # External profile with rounding below Dmin
            profile_ext = [
                           {'x': -p/2,        'y': -5*h/8-h/16},
                           {'x': -3*p/8-p/32, 'y': -5*h/8-h/32},
                           {'x': -3*p/8,      'y': -5*h/8},
                           {'x': -p/16,       'y':  0},
                           {'x':  p/16,       'y':  0},
                           {'x':  3*p/8,      'y': -5*h/8},
                           {'x':  3*p/8+p/32, 'y': -5*h/8-h/32},
                           {'x':  p/2,        'y': -5*h/8-h/16}
                           ]
            name_ext = '{0}_ext'.format(name)
            os_ext = {
                      'radius':  r,
                      'pitch':   p,
                      'profile': profile_ext
                      }
            yield (name_ext, os_ext)
            # Internal profile with rounding above Dmaj
            profile_int = [
                           {'x': -p/2,       'y': -5*h/8},
                           {'x': -3*p/8,     'y': -5*h/8},
                           {'x': -p/16,      'y':  0},
                           {'x': -p/16+p/64, 'y':  h/64},
                           {'x':  0,         'y':  h/32},
                           {'x':  p/16-p/64, 'y':  h/64},
                           {'x':  p/16,      'y':  0},
                           {'x':  3*p/8,     'y': -5*h/8},
                           {'x':  p/2,       'y': -5*h/8}
                           ]
            name_int = '{0}_int'.format(name)
            os_int = {
                      'radius':  r,
                      'pitch':   p,
                      'profile': profile_int
                      }
            yield (name_int, os_int)
            if first == True and extended == False:
                aname = 'M{0}'.format(str(dd).replace('.', '_'))
                yield (aname, {'alias': name})
                aname_ext = '{0}_ext'.format(aname)
                yield (aname_ext, {'alias': name_ext})
                aname_int = '{0}_int'.format(aname)
                yield (aname_int, {'alias': name_int})
                first = False


def process_data(data, dataout, produce_json=False, decimals=5, license=''):
    if produce_json == True:
        ospecs = {}
        for (k, s) in generate_specs(data):
            ospecs[k] = s
        json.dump(ospecs, dataout)
    else:
        import screw
        screw.init_specs(dataout, '', license)
        for (k, s) in generate_specs(data):
            screw.process_spec(k, s, dataout, decimals)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Produce OpenSCAD modules to
                                     generate screws that follow the ISO 261
                                     standard''')
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
