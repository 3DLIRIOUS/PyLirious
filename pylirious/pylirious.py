#!/usr/bin/python3
"""Pylirious module

Miscellaneous functions to work with 3D models in Python 3.

"""

import os
import sys
import inspect
import subprocess
from datetime import datetime

import meshlabxml as mlx

from . import filename

"""
run_openscad() {
    #$1=input
    #$2=output

	#set -x
    local start_time
    local end_time
    local diff_time
    local return_code

    echo ; echo -n "Rendering OpenSCAD file & generating stl ... "
    start_time=$(date +%s.%N)
    openscad -o "$2" "$1"
    return_code=$?
    end_time=$(date +%s.%N)
    diff_time=$(bc <<< "$end_time - $start_time")
    diff_time=$(printf %.0f $diff_time) #round to integer milliseconds
    echo -n "finished in "; printf "%0dh:%0dm:%0ds" $(($diff_time/3600)) $(($diff_time%3600/60)) $(($diff_time%60)); echo ", return code: $return_code"

    if [ $return_code -ne 0 ]; then
        pause "Uh oh, looks like there's an error. Hit any key to keep going anyway ... "
    fi

    return $return_code
}

run_admesh() {
    #$1=input
    #$2=output - if blank run check only, otherwise output ascii stl

    local start_time
    local end_time
    local diff_time
    local return_code
    local O=""

    # set default log file if it is not already set
    if [ -z "$admesh_LF" ]; then
        admesh_LF="TEMP3DL_admeshlog.txt"
    fi

    # check for output file
    if [ -n "$2" ]; then
        O="-a $2"
    fi

	echo
	if [  "$verbosity" -ge 4  ]; then
		echo "*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*"
	fi
    echo -n "    Running ADMesh ... "
    start_time=$(date +%s.%N)
    admesh "$1" $O > "$admesh_LF"
    return_code=$?
    end_time=$(date +%s.%N)
    diff_time=$(bc <<< "$end_time - $start_time")
    diff_time=$(printf %.0f $diff_time) #round to integer milliseconds
    echo -n "finished in "; printf "%0dh:%0dm:%0ds" $(($diff_time/3600)) $(($diff_time%3600/60)) $(($diff_time%60)); echo ", return code: $return_code"
    if [ "$verbosity" -ge 4 ]; then
		echo "*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*ADMesh*"
	fi
    if [ $return_code -ne 0 ]; then
        pause "Uh oh, looks like there's an error. Hit any key to keep going anyway ... "
    fi

    return $return_code
}
"""


def render_scad():
    pass


def run_admesh():
    pass


def swap_yz(file_in, log=None):
    """ Swap a mesh "Up" direction betwenn "Y" and "Z" axes.

    Requires metadata to know what the current "Up" direction is.

    """
    fprefix, scale_meta, up_meta, fext = filename.check_metadata(file_in)
    if up_meta == 'Y':  # Y to Z: rotate 90d about X
        up_meta = 'Z'
        angle = 90
    else:  # Z to Y: rotate -90d about X
        up_meta = 'Y'
        angle = -90

    file_out = '%s(%s%s).%s' % (fprefix, scale_meta, up_meta, fext)
    script = 'TEMP3D_swapYZ.mlx'

    mlx.begin(script, file_in=file_in)
    mlx.transform.rotate(script, 'x', angle)
    mlx.end(script)
    mlx.run(log, file_in=file_in, file_out=file_out, script=script)
    return file_out


def blend(module_function=None, log=None, module_path=None, cmd=None):
    """Run a function inside a Blender Python module and pass it parameters.

    Args:
        module_function (str): the module, function and parameters you want to  run.
            example: 'bpylirious.boolean(source, operation, target, output)'
        module_path (str): full path to the module. If omitted it will use the
            path of this module.
        log (str): filename of the log file (optional)
        cmd (str): a full command to run with blender. This will override
            module_function and module_path.

    Returns:
        return_code (int): the blender return code
    """
    if cmd is None:
        cmd = 'blender --background --factory-startup --python'
        if module_function is None:
            print('Error: you must provide a python function')
            sys.exit(1)
        else:
            # Parse module_function
            module = module_function.split('.')[0]
            if module_path is None:
                # Assume module is in the same directory as this module
                this_modulepath = os.path.dirname(
                    os.path.realpath(inspect.getsourcefile(lambda: 0)))
                module_full = os.path.join(this_modulepath, module + '.py')
            else:
                module_full = os.path.join(module_path, module + '.py')
            function = '.'.join(module_function.split('.')[1:]).split('(')[0]
            parameters = module_function.split('(')[1].rsplit(')')[
                0].replace(', ', ' ')
            cmd += ' %s -- -f %s -p %s' % (module_full, function, parameters)
    if log is not None:
        log_file = open(log, 'a')
        if parameters is not None:
            log_file.write('\nBlender Python module and function:\n')
            log_file.write('%s.%s(%s)\n' %
                           (module, function, parameters.replace(' ', ', ')))
        log_file.write('cmd = %s\n' % cmd)
        log_file.write('***START OF BLENDER STDOUT & STDERR***\n')
        log_file.close()
        log_file = open(log, 'a')
    else:
        log_file = None
        print('blender cmd = %s' % cmd)
        print('***START OF BLENDER STDOUT & STDERR***')
    # subprocess.Popen( meshlabserver,
    #return_code = subprocess.call( [meshlabserver, '-i' + i])
    while True:
        return_code = subprocess.call(cmd, shell=True, stdout=log_file,
                                      stderr=log_file, universal_newlines=True)
        if return_code == 0:
            break
        else:
            print('Houston, we have a problem.')
            print('Blender did not finish sucessfully. Review the log file and the input file(s) to see what went wrong.')
            print('Blender command: "%s"' % cmd)
            print('log: "%s"' % log)
            print('\nWhere do we go from here?')
            print(
                ' r  - retry running Blender (probably after you\'ve fixed any problems with the input files)')
            print(
                ' c  - continue on with the script (probably after you\'ve manually re-run and generated the deisred output file(s)')
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
                mlx.util.delete_all('TEMP3D*')
                if log is not None:
                    os.remove(log)
                sys.exit(1)
            elif choice == 'c':
                print('Continuing on ...')
                break
            elif choice == 'r':
                print('Retrying blender cmd ...')
    if log is not None:
        log_file.write('***END OF BLENDER STDOUT & STDERR***\n')
        log_file.write('blender return code = %s\n\n' % return_code)
        log_file.close()
    return return_code


def setup(sys_argv):
    """Process arguments and create log file.

    Will also change into the directory of the first argument.

    Args:
        args (list): sys.argv . First argument (sys.argv[1])
            needs to be an input file.

    Returns:
        fpath (str): file path of the input file
        fbasename (str): file basename of the input file
        scriptname (str): filename of the running script
        log (str): filename of the log file

    """
    fpath = os.path.dirname(sys_argv[1])
    os.chdir(fpath)
    fbasename = os.path.basename(sys_argv[1])
    scriptname = os.path.basename(sys.argv[0])
    log = 'log_file-%s-%s.txt' % (
        os.path.splitext(scriptname)[0].strip(),
        datetime.now().strftime("%Y.%m.%d-%H.%M.%S"))
    log_file = open(log, 'w')
    log_file.write('%s\n' % sys.version)
    log_file.write('sys.argv = %s\n' % sys_argv)
    log_file.write('fpath (working directory) = %s\n' % fpath)
    log_file.write('fbasename = %s\n\n' % fbasename)
    log_file.close()
    return fpath, fbasename, scriptname, log


def write_pyfunc(return_val=None, function=None, **kargs):
    pass
