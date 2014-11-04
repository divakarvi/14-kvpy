#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import os, sys

def lyx2lyx(fname_pfx):
    def handle_listing(ifile, ofile, line, stack):
        top = stack[-1]
        if top.startswith(r'\begin_layout Standard'):
            #print('fixing listings inset')
            #end existing Standard layout
            ofile.write(r'\end_layout' + '\n') 
            #insert new Standard layout
            ofile.write(r'\begin_layout Standard' + '\n') 
            ofile.write(r'\begin_inset listings' + '\n')
            while not line.startswith(r'\end_inset'):
                line = ifile.readline()
                ofile.write(line)
            #end inserted Standard layout 
            ofile.write(r'\end_layout' + '\n')
            #resume Standard layout
            ofile.write(r'\begin_layout Standard' + '\n') 
            return 'fixed'
        return ''

    ifile = fname_pfx + '.lyx'
    ofile = fname_pfx + '_tmp.lyx'
    print(ifile, ' ----> ', ofile)
    ifile = open(ifile, 'r')
    ofile = open(ofile, 'w')

    stack = []
    line = ifile.readline()
    while line != '':
        if line.startswith(r'\begin_layout'):
            stack.append(line)           
        if line.startswith(r'\end_layout'):
            top = stack.pop()
        if line.startswith(r'\begin_layout Exercise'):
            line = line.replace('Exercise', 'Description', 1)
            ofile.write(line)
            ofile.write('Exercise:  \n')
            line = ifile.readline()
            continue
        if line.startswith(r'\begin_layout Theorem'):
            line = line.replace('Theorem', 'Description', 1)
            ofile.write(line)
            ofile.write('Theorem:  \n')
            line = ifile.readline()
            continue
        if line.startswith(r'\begin_inset listings'):
            fix = handle_listing(ifile, ofile, line, stack)
            if(fix == 'fixed'):
                line = ifile.readline()
                continue

        ofile.write(line)
        line = ifile.readline()

    ifile.close()
    ofile.close()

def lyx2html(fname_pfx):
    ifile  = fname_pfx + '_tmp.lyx'
    ofile = fname_pfx + '.html'

    opt1 = '--nofooter'
    opt2 = '--numberfoot'
    opt3 = '--copyright'
    opt4 = '--css "lyx.css"'
    
    opts = opt1 + ' ' + opt2 + ' ' +  opt3 + ' ' + opt4
    cmd = 'elyxer ' + opts + ' ' + ifile + ' > ' + ofile
    print(cmd)
    os.system(cmd)

    cmd = 'rm ' + ifile
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    assert len(sys.argv) == 2
    fname_pfx = sys.argv[1]
    assert os.path.isfile(fname_pfx + '.lyx')
    assert not os.path.isfile(fname_pfx + '_tmp.lyx')
    assert not os.path.isdir(fname_pfx + '_tmp.lyx')

    lyx2lyx(fname_pfx)
    lyx2html(fname_pfx)

    yno = raw_input('copy to Dropbox? y/n: ')
    if yno == 'y':
        cmd = 'cp lecture.html lyx.css ~/Dropbox/Public/14-kvpy/'
        os.system(cmd)
        cmd = 'cp -r figs-python ~/Dropbox/Public/14-kvpy/'
        os.system(cmd)
