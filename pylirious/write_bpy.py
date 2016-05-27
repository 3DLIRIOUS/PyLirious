"""Module to create (write) a Python script to be run by Blender"""

import os
import sys
import inspect
import subprocess

def begin(s='MLTEMP_blender_default.py'):
    sf = open(s,'w')
    sf.write(
        '""" Blender Python script created by pylirious.writebpy"""\n\n'
        + 'import bpy\n' 
        + 'import bmesh\n'
        + 'import os\n'
        + 'import sys\n'
        + 'import inspect\n'
        + 'import pylirious.bpylirious\n'
        + 'import meshlabxml as mlx\n'
        + '\n'
        )
    # Find the path of this script and add it to python's path.
    """this_scriptpath = os.path.dirname(os.path.realpath(inspect.getsourcefile(lambda:0)))
    # TODO: do we need to move this up a directory?
    sf.write(
        'sys.path.append(%s)\n' % this_scriptpath
        + 'import pylirious\n'
        )"""
    sf.write('pylirious.bpylirious.begin()\n')
    sf.close()
    return None

def import_mesh(fin=None, s='MLTEMP_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpylirious.import_mesh("%s")\n' % (return_vars, fin))
    else:
        sf.write('pylirious.bpylirious.import_mesh("%s")\n' % (fin))
    sf.close ()
    return return_vars

def export_mesh(obj_src=None, fout=None, texture=None, s='MLTEMP_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpylirious.export_mesh(%s, "%s", %s)\n' % (
            return_vars, obj_src, fout, texture))
    else:
        sf.write('pylirious.bpylirious.export_mesh(%s, "%s", %s)\n' % (
            obj_src, fout, texture))
    sf.close ()
    return return_vars

def boolean(obj_src=None,  operation='+', obj_trgt=None,
            s='MLTEMP_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpylirious.boolean(%s, "%s", %s)\n' % (
            return_vars, obj_src, operation, obj_trgt))
    else:
        sf.write('pylirious.bpylirious.boolean(%s, "%s", %s)\n' % (
            obj_src, operation, obj_trgt))
    sf.close ()
    return return_vars

def command(command=None, s='MLTEMP_blender_default.py'):
    """ Write the command verbatim to the script file"""
    sf = open(s,'a')
    sf.write(command)
    sf.close ()

def run(s='MLTEMP_blender_default.py', runlogname=None):
    cmd = 'blender --background --factory-startup --python %s' % s
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('cmd = %s\n' % cmd)
        RUNLOG.write('***START OF BLENDER STDOUT & STDERR***\n')
        RUNLOG.close()
        RUNLOG = open(runlogname, 'a')
    else:
        RUNLOG = None
        print('blender cmd = %s' % cmd)
        print('***START OF BLENDER STDOUT & STDERR***')
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
