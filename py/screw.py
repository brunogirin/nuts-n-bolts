#!/usr/bin/env python
'''
Created on 22 Dec 2012

@author: bruno
'''

import sys
import argparse
import json
import math

def sample(points, maxdx=0.1, scale_to=2*math.pi):
    xratio = scale_to / (points[-1]['x'] - points[0]['x'])
    fp = [{'x': p['x'] * xratio, 'y': p['y']} for p in points]
    prev = None
    for p in fp:
        if prev is not None:
            dx = p['x'] - prev['x']
            dy = p['y'] - prev['y']
            if math.fabs(dx) > maxdx:
                ndx = math.fabs(math.ceil(dx/maxdx))
                ddx = dx / ndx
                x = prev['x'] + ddx
                while math.fabs(p['x']-x) >= math.fabs(ddx/2):
                    y = prev['y']+dy*(x-prev['x'])/dx
                    yield {'x': x, 'y': y}
                    x = x + ddx
        yield p
        prev = p

def process_spec(key, spec, dataout, precision=5):
        dataout.write('\nmodule {0}(height, slices=100) {{\n'.format(key))
        if 'alias' in spec:
            dataout.write('    {0}(height, slices);\n'.format(spec['alias']))
        else:
            pitch = spec['pitch']
            r = spec['radius']
            if 'dx' in spec:
                maxdx = spec['dx']
            else:
                maxdx = 0.1
            poly = [{
                     'x': (r+p['y'])*math.cos(p['x']),
                     'y': (r+p['y'])*math.sin(p['x'])
                     } for p in sample(spec['profile'], maxdx)]
            dataout.write('    screw(height, {0}, [{1}], slices);\n'.format(
                                pitch,
                                ','.join(['[{0:.{2}f},{1:.{2}f}]'.format(q['x'], q['y'], precision) for q in poly])
                                )
                          )
        dataout.write('}\n')

def init_specs(dataout, include='', license=''):
    if license != '':
        licfile = open(license, 'r')
        dataout.write(licfile.read())
        dataout.write('\n')
    if include != '' and include[-1:] != '/':
        include = "{0}/".format(include)
    dataout.write("use <{0}screw.scad>;\n".format(include))

def process_specs(specs, dataout, include='', license=''):
    init_specs(dataout, include, license)
    for k, v in specs.iteritems():
        process_spec(k, v, dataout)
    dataout.close()

def process(datain, dataout, include='', license=''):
    specs = json.load(datain)
    process_specs(specs, dataout, include, license)
    datain.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Produce OpenSCAD modules to
                                     generate screws as per a specification in
                                     JSON format''')
    parser.add_argument('-i', '--include', default='',
                        help='''Specify the include directory where screw.scad
                        can be found.''')
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
    process(datain, dataout, args.include, args.license)
    
