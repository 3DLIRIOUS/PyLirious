"""Module to create (write) a Python 2 script to be run by MeshMixer"""

import os
import sys
#import inspect
import subprocess
import time

from meshlabxml.util import delete_all
from meshlabxml import handle_error


def write_mmpyfunc(return_vars=None, script=None, function=None, **kwargs):
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
        script_file.write(
            '\n%s = mmlirious.%s(remote, ' %
            (return_vars, function))
    else:
        script_file.write('\nmmlirious.%s(remote, ' % (function))
    script_file.close()

    filename_args = ['file_in', 'file_out']
    str_args = []

    script_file = open(script, 'a')
    if kwargs is not None:
        first = True
        for key, value in kwargs.items():
            if not first:
                script_file.write(', ')
            # Need to quote strings
            if key in filename_args:
                # Use raw literal strings; needed for Windows paths.
                script_file.write('%s=r"%s"' % (key, value))
            elif key in str_args:
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


def begin(script='TEMP3D_mix_default.py'):
    script_file = open(script, 'w')
    script_file.write('\n'.join([
        '#! python 2.7',
        '""" MeshMixer Python 2.7 script created by write_mmpy"""\n',
        'from __future__ import print_function',
        'from __future__ import division',
        'import os',
        'import sys',
        #'import inspect',
        '',
        'from pylirious import mmlirious',
        '\n']))
    script_file.write('remote = mmlirious.begin()\n')
    script_file.close()
    return None


def end(script='TEMP3D_mix_default.py'):
    script_file = open(script, 'a')
    script_file.write('\nmmlirious.end(remote)\n')
    script_file.close()
    return None


def open_mix(return_vars=None, script='TEMP3D_mix_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'open_mix'
    write_mmpyfunc(return_vars=return_vars, script=script,
                   function=function, **kwargs)
    return return_vars


def import_mesh(return_vars=None, script='TEMP3D_mix_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'import_mesh'
    write_mmpyfunc(return_vars=return_vars, script=script,
                   function=function, **kwargs)
    return return_vars


def export_mesh(return_vars=None, script='TEMP3D_mix_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'export_mesh'
    write_mmpyfunc(return_vars=return_vars, script=script,
                   function=function, **kwargs)
    return return_vars


def hollow(return_vars=None, script='TEMP3D_mix_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'hollow'
    write_mmpyfunc(return_vars=return_vars, script=script,
                   function=function, **kwargs)
    return return_vars


def make_solid(return_vars=None, script='TEMP3D_mix_default.py', **kwargs):
    """ Run the same function in mmlirious and return return_vars"""
    function = 'make_solid'
    write_mmpyfunc(return_vars=return_vars, script=script,
                   function=function, **kwargs)
    return return_vars


def command(cmd=None, script='TEMP3D_mix_default.py'):
    """ Write the command verbatim to the script file"""
    script_file = open(script, 'a')
    script_file.write(cmd)
    script_file.close()


def run(script='TEMP3D_mix_default.py', log=None):
    """Run MeshMixer in a subprocess and execute script.

    """
    python27 = 'C:\\Python27\\pythonw.exe'
    cmd = '"%s" "%s"' % (python27, script)

    if log is not None:
        log_file = open(log, 'a')
        log_file.write('cmd = %s\n' % cmd)
        log_file.write('***START OF MESHMIXER STDOUT & STDERR***\n')
        log_file.close()
        log_file = open(log, 'a+')
    else:
        log_file = None
        print('meshmixer cmd = %s' % cmd)
        print('***START OF MESHMIXER STDOUT & STDERR***')
    while True:
        if log is not None:
            # Find position in log_file before launching MeshMixer
            start_pos = log_file.tell()
        # Launch MeshMixer
        # TODO: experiment with passing current directory to meshmixer
        mm_proc = subprocess.Popen(['meshmixer'], stdout=log_file,
                                   stderr=log_file, universal_newlines=True)

        if False:
        #if log is not None:
            # Read log_file to see when MeshMixer has finished opening and is
            # ready to process script
            mm_ready = False
            while not mm_ready:
                # Go to the start of MeshMixer's output
                log_file.seek(start_pos)
                for line in log_file:
                    # print(line)
                    # Looks like gaManager needs an internet connection. Use a different line.
                    # if '[gaManager] success!' in line:
                    
                    # MeshMixer 3.0:
                    #if '[Setting up global event filter]' in line:
                    # MeshMixer 3.2:
                    if 'GraphicsViewScene3D::Initialize drawFboId:' in line:
                        mm_ready = True
                # log_file.seek(0,2) # Go to the end of the file
                time.sleep(0.1)
        else:
            # Use a fixed delay if there is no log. May not be enough if your
            # computer is slow.
            time.sleep(5)

        # Run mm python script
        return_code = subprocess.call(cmd, shell=True, stdout=log_file,
                                      stderr=log_file, universal_newlines=True)
        # return_code = 1 # for testing
        mm_proc.terminate()
        if log is not None:
            log_file.close()
        if (return_code == 0) or handle_error(program_name='MeshMixer', cmd=cmd, log=log):
            break
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('***END OF MESHMIXER STDOUT & STDERR***\n')
        log_file.write('MeshMixer return code = %s\n\n' % return_code)
        log_file.close()
    return return_code
