"""Module to create (write) a Python script to be run by Blender"""

import os
import sys
import subprocess

from meshlabxml.util import delete_all


def write_bpyfunc(return_vars=None, script=None, function=None, **kwargs):
    # Determine calling function automatically:
    #   inspect.currentframe().f_code.co_name
    #   function = inspect.stack()[0][3]
    #   Faster just to hardcode name
    """print('In write_mmpyfunc')
    print('script = %s' % script)
    print('return_vars = %s' % return_vars)
    print('function = %s' % function)
    print('kwargs = %s' % kwargs)"""

    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('\n%s = bpylirious.%s(' % (return_vars, function))
    else:
        script_file.write('\nbpylirious.%s(' % (function))
    script_file.close()

    str_args = ['file_in', 'file_out', 'axis', 'operation']

    script_file = open(script, 'a')
    if kwargs is not None:
        first = True
        for key, value in kwargs.items():
            if not first:
                script_file.write(', ')
            # Need to quote strings
            if key in str_args:
                script_file.write('%s="%s"' % (key, value))
            else:
                script_file.write('%s=%s' % (key, value))
            first = False
    script_file.close()

    # Write closing parentheses
    script_file = open(script, 'a')
    script_file.write(')\n')
    script_file.close()
    return return_vars


def begin(script='TEMP3D_blender_default.py'):
    script_file = open(script, 'w')
    script_file.write('\n'.join([
        '""" Blender Python script created by pylirious.writebpy"""\n',
        #'import bpy',
        #'import bmesh',
        #'from mathutils import Vector',
        #'import os',
        #'import sys',
        #'import inspect',
        #'import math',
        'from pylirious import bpylirious',
        #'import meshlabxml as mlx',
        '\n']))
    script_file.write('bpylirious.begin()\n')
    script_file.close()
    return None


def import_mesh(return_vars=None,
                script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'import_mesh'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def export_mesh(return_vars=None,
                script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'export_mesh'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def rotate(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'rotate'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def translate(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'translate'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def join(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'join'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def plane_cut(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'plane_cut'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def extrude_bottom(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'extrude_bottom'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def extrude_plane(return_vars=None,
                  script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'extrude_plane'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def boolean(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'boolean'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def command(cmd=None, script='TEMP3D_blender_default.py'):
    """ Write the command verbatim to the script file"""
    script_file = open(script, 'a')
    script_file.write(cmd)
    script_file.close()


def run(script='TEMP3D_blender_default.py', log=None):
    """Run Blender in a subprocess and execute script.

    """
    cmd = 'blender --background --factory-startup --python %s' % script
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('cmd = %s\n' % cmd)
        log_file.write('***START OF BLENDER STDOUT & STDERR***\n')
        log_file.close()
        log_file = open(log, 'a')
    else:
        log_file = None
        print('blender cmd = %s' % cmd)
        print('***START OF BLENDER STDOUT & STDERR***')
    while True:
        return_code = subprocess.call(cmd, shell=True, stdout=log_file,
                                      stderr=log_file, universal_newlines=True)
        if log is not None:
            log_file.close()
        if return_code == 0:
            break
        else:
            print('Houston, we have a problem.')
            print('Blender did not finish sucessfully. Review the log',
                  'file and the input file(s) to see what went wrong.')
            print('Blender command: "%s"' % cmd)
            print('log: "%s"' % log)
            print('\nWhere do we go from here?')
            print(' r  - retry running Blender (probably after',
                  'you\'ve fixed any problems with the input files)')
            print(' c  - continue on with the script (probably after',
                  'you\'ve manually re-run and generated the desired',
                  'output file(s)')
            print(' x  - exit, keeping the TEMP3D file and log')
            print(' xd - exit, deleting the TEMP3D files and log')
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
                print('Deleting TEMP3D* and log files and exiting ...')
                delete_all('TEMP3D*')
                if log is not None:
                    os.remove(log)
                sys.exit(1)
            elif choice == 'c':
                print('Continuing on ...')
                break
            elif choice == 'r':
                print('Retrying blender cmd ...')
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('***END OF BLENDER STDOUT & STDERR***\n')
        log_file.write('blender return code = %s\n\n' % return_code)
        log_file.close()
    return return_code
