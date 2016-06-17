"""Module to create (write) a Python script to be run by Blender"""

import os
import sys
import subprocess
from glob import glob


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


def import_mesh(file_in=None, script='TEMP3D_blender_default.py',
                return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write(
            '%s = bpylirious.import_mesh("%s")\n' %
            (return_vars, file_in))
    else:
        script_file.write('bpylirious.import_mesh("%s")\n' % (file_in))
    script_file.close()
    return return_vars


def export_mesh(mesh_object=None, file_out=None, texture=None,
                script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.export_mesh(%s, "%s", %s)\n' % (
            return_vars, mesh_object, file_out, texture))
    else:
        script_file.write('bpylirious.export_mesh(%s, "%s", %s)\n' % (
            mesh_object, file_out, texture))
    script_file.close()
    return return_vars


def rotate(mesh_object=None, axis='z', angle=0.0, apply=True,
           script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.rotate(%s, "%s", %s, %s)\n' % (
            return_vars, mesh_object, axis, angle, apply))
    else:
        script_file.write('bpylirious.rotate(%s, "%s", %s)\n' % (
            mesh_object, axis, angle))
    script_file.close()
    return return_vars


def translate(mesh_object=None, value=(0.0, 0.0, 0.0), apply=True,
              script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.translate(%s, %s, %s)\n' % (
            return_vars, mesh_object, value, apply))
    else:
        script_file.write('bpylirious.translate(%s, %s, %s)\n' % (
            mesh_object, value, apply))
    script_file.close()
    return return_vars


def join(objects=None, script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.join(%s)\n' % (
            return_vars, objects))
    else:
        script_file.write('bpylirious.join(%s)\n' % (
            objects))
    script_file.close()
    return return_vars


def plane_cut(mesh_object=None, axis='z', offset=0.0,
              script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.plane_cut(%s, "%s", %s)\n' % (
            return_vars, mesh_object, axis, offset))
    else:
        script_file.write('bpylirious.plane_cut(%s, "%s", %s)\n' % (
            mesh_object, axis, offset))
    script_file.close()
    return return_vars


def extrude_bottom(mesh_object=None, threshold=0.00001, distance=6,
                   script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.extrude_bottom(%s, %s, %s)\n' % (
            return_vars, mesh_object, threshold, distance))
    else:
        script_file.write('bpylirious.extrude_bottom(%s, %s, %s)\n' % (
            mesh_object, threshold, distance))
    script_file.close()
    return return_vars


def extrude_plane(mesh_object=None, center=(0.0, 0.0, 0.0),
                  radius=1, angle=1, distance=6,
                  script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.extrude_plane(%s, %s, %s, %s, %s)\n' % (
            return_vars, mesh_object, center, radius, angle, distance))
    else:
        script_file.write('bpylirious.extrude_plane(%s, %s, %s, %s, %s)\n' % (
            mesh_object, center, radius, angle, distance))
    script_file.close()
    return return_vars


def boolean(obj_src=None, operation='+', obj_trgt=None,
            script='TEMP3D_blender_default.py', return_vars=None):
    """ Run the same function in bpylirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = bpylirious.boolean(%s, "%s", %s)\n' % (
            return_vars, obj_src, operation, obj_trgt))
    else:
        script_file.write('bpylirious.boolean(%s, "%s", %s)\n' % (
            obj_src, operation, obj_trgt))
    script_file.close()
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
        log_file.write('***END OF BLENDER STDOUT & STDERR***\n')
        log_file.write('blender return code = %s\n\n' % return_code)
        log_file.close()
    return return_code


def delete_all(filename):
    """delete files in the current directory that match a pattern.

    Intended for temp files, e.g. mlx.delete('TEMP3D*').

    """
    for fread in glob(filename):
        os.remove(fread)
