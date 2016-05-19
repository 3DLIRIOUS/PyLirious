"""Pylirious module"""

#!/usr/bin/python3
# pylirious.py

#Builtin modules
import os
import sys
import inspect
import subprocess
import unicodedata
import string

#Local modules
import meshlabxml as mlx

def parse_filename(fbasename, runlogname = None):
    """ Parse filename, spltting it up into the filename
    prefix, file extension, and reading "Scale" and "Up"
    metadata. """
    fpref_full = os.path.splitext(fbasename)[0].strip()
    fext = os.path.splitext(fbasename)[1][1:].strip().lower()
    try:
        metadata = fbasename.rsplit('(')[-1].rsplit(').')[-2]
        fprefix = fpref_full.rsplit('(',1)[0]
        mScale = metadata[:-1]
        mUp = metadata[-1]
    except IndexError:
        metadata = None
        fprefix = fpref_full
        mScale = None
        mUp = None
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Parsed filename:\n')
        RUNLOG.write('fbasename = %s\n' % fbasename)
        RUNLOG.write('fpref_full = %s\n' % fpref_full)
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('metadata = %s\n' % metadata)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()
    return fprefix, mScale, mUp, fext

def check_metadata(fbasename, runlogname = None):
    fprefix, mScale, mUp, fext = parse_filename(fbasename)
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Metadata values at start of check_metadata:\n')
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()

    # Check mScale
    mScaleDefault = '1' # this needs to be a string
    while True:
        if mlx.is_number(mScale):
            if mScale == 0:
                print ('Scale can\'t be zero!')
            else :
                break
        else :
            print ('Error: scale factor is not a valid number!\n')
        print ('Enter the current scale of the mesh.\n',
               'Valid values:\n',
               '  * Positive value greater than one, e.g. \"2\" means the ' +
               'mesh is twice its original size.\n',
               '  * Negative value for an inverse scale factor, (e.g. ' +
               '\"-10\" means 1/10th scale)\n',
               '  * Decimal value with period separator, (e.g. \"0.1\" ' +
               'for 1/10th scale)\n')
        mScale = input('Hit enter to accept the default' +
                        ' (\"%s\"): ' % mScaleDefault)
        if mScale == "":
            mScale = mScaleDefault

    # Check mUp, valid values are Y or Z
    if fext == 'stl':
        mUpDefault = 'Z'
    else:
        mUpDefault = 'Y'
    while True:
        if mUp == 'Y':
            break
        elif mUp == 'Z':
            break
        print('Enter the mesh \"up\" axis. Valid values are Y or Z.\n')
        mUp = input('Hit enter to accept the default' +
                        ' (\"%s\"): ' % mUpDefault)
        if mUp == "":
            mUp = mUpDefault

    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Metadata values at end of check_metadata:\n')
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()
    return fprefix, mScale, mUp, fext

def slugify(fprefix):
    fprefix = fprefix.replace(' ','_')
    # Notes: Shapeways doesn't like ampersands in mesh names or commas in texture names
    # Very strict: only letters, numbers, dashes & underscores. Still allow periods for now.
    #validFilenameChars = '-_.() %s%s\n' % (string.ascii_letters, string.digits)
    validFilenameChars = '-_.%s%s\n' % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', fprefix) #.encode('ascii', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)

def render_scad():
    ...

def run_admesh():
    ...

def swapYZ(fin, runlogname=None):
    fprefix, mScale, mUp, fext = check_metadata(fin)
    if mUp == 'Y': # Y to Z; rotate 90d about X
        mUp = 'Z'
        angle = 90
    else : # Z to Y; roate -90 about X
        mUp = 'Y'
        angle = -90

    fout = fprefix + '(' + mScale + mUp + ').' + fext
    mlLog = 'MLTEMP_swapYZ_mlx_lf.txt'
    sf = 'MLTEMP_swapYZ.mlx'

    mlx.begin(sf, i=fin)
    mlx.rotate(sf, 'x', angle)
    mlx.end(sf)

    mlRC = mlx.run(log=mlLog, i=fin, o=fout,
                          s=sf, runlogname=runlogname)
    return mlRC, fout

def blend( moduleFunction=None, runlogname=None, modulePath=None, cmd=None):
    """Run a function inside a Blender Python module and pass it parameters.
    
    Args:
        moduleFunction (str): the module, function and parameters you want to  run.
            example: 'bpylirious.boolean(source, operation, target, output)'
        modulePath (str): full path to the module. If omitted it will use the
            path of this module.
        runlogname (str): filename of the runlog file (optional)
        cmd (str): a full command to run with blender. This will override 
            moduleFunction and modulePath.

    Returns:
        return_code (int): the blender return code
    """
    if cmd is None:
        cmd = 'blender --background --factory-startup --python'
        if moduleFunction is None:
            print('Error: you must provide a python function')
            sys.exit(1)
        else:
            # Parse moduleFunction
            module = moduleFunction.split('.')[0]
            if modulePath is None:
                # Assume module is in the same directory as this module
                this_modulepath = os.path.dirname(os.path.realpath(inspect.getsourcefile(lambda:0)))
                moduleFull = os.path.join(this_modulepath, module + '.py')
            else:
                moduleFull = os.path.join(modulePath, module + '.py')
            function = '.'.join(moduleFunction.split('.')[1:]).split('(')[0]
            parameters = moduleFunction.split('(')[1].rsplit(')')[0].replace(', ', ' ')
            cmd += ' %s -- -f %s -p %s' % (moduleFull, function, parameters)
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        if parameters is not None:
            RUNLOG.write('\nBlender Python module and function:\n')
            RUNLOG.write('%s.%s(%s)\n' % (module, function, parameters.replace(' ', ', ')))
        RUNLOG.write('cmd = %s\n' % cmd)
        RUNLOG.write('***START OF BLENDER STDOUT & STDERR***\n')
        RUNLOG.close()
        RUNLOG = open(runlogname, 'a')
    else:
        RUNLOG = None
        print('blender cmd = %s' % cmd)
        print('***START OF BLENDER STDOUT & STDERR***')
    #subprocess.Popen( meshlabserver,
    #return_code = subprocess.call( [meshlabserver, '-i' + i])
    while True:
        return_code = subprocess.call( cmd, shell=True, stdout=RUNLOG,
                                   stderr=RUNLOG, universal_newlines=True)
        if return_code == 0:
            break
        else:
            print('Houston, we have a problem.')
            print('Blender did not finish sucessfully. Review the runlog file and the input file(s) to see what went wrong.')
            print('Blender command: "%s"' % cmd)
            print('runlog: "%s"' % runlogname)
            print('\nWhere do we go from here?')
            print(' r  - retry running Blender (probably after you\'ve fixed any problems with the input files)')
            print(' c  - continue on with the script (probably after you\'ve manually re-run and generated the deisred output file(s)')
            print(' x  - exit, keeping the MLTEMP file and runlog')
            print(' xd - exit, deleting the MLTEMP files and runlog')
            while True:
                choice = input('Select r, c, x, or xd: ')
                if choice not in ('r', 'c', 'x', 'xd'):
                    print('Please enter a valid option.')
                else:
                    break
            if choice == 'x':
                print('Exiting ...')
                sys.exit(1)
            elif choice == 'xd':
                print('Deleting MLTEMP* and runlog files and exiting ...')
                delete_all('MLTEMP*')
                if runlogname is not None:
                    os.remove(runlogname)
                sys.exit(1)
            elif choice == 'c':
                print('Continuing on ...')
                break
            elif choice == 'r':
                print('Retrying blender cmd ...')
    if runlogname is not None:
        RUNLOG.write('***END OF BLENDER STDOUT & STDERR***\n')
        RUNLOG.write('blender return code = %s\n\n' % return_code)
        RUNLOG.close()
    return return_code


