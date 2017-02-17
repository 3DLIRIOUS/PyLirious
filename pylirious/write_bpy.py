"""Module to create (write) a Python script to be run by Blender"""

import os
import sys
import subprocess

from meshlabxml.util import delete_all
from meshlabxml import handle_error


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

    # Need to manually add any arguments that are strings to this list
    # TODO: can we automatically determine if a value is a string instead of having to use a hardcoded list?
    filename_args = ['file_in', 'file_out', 'image_file']
    str_args = ['axis', 'operation', 'method', 'tex_name', 'mat_name', 'view', 'perspective',
                'coord_system', 'solver']

    if function == 'uv_cylinder_project':
        str_args.append('direction')

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


def begin(script='TEMP3D_blender_default.py'):
    """ Create new Blender Python script and write opening lines"""
    script_file = open(script, 'w')
    script_file.write('\n'.join([
        '""" Blender Python script created by pylirious.writebpy"""\n',
        'import bpy',
        'import bmesh',
        'from mathutils import Vector',
        'import os',
        'import sys',
        'import inspect',
        'import math',
        'from pylirious import bpylirious',
        #'import meshlabxml as mlx',
        '\n']))
    script_file.write('bpylirious.begin()\n')
    script_file.close()
    return None


def import_mesh(return_vars=None,
                script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'import_mesh'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def export_mesh(return_vars=None,
                script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'export_mesh'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def duplicate_mesh(return_vars=None,
                script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'duplicate_mesh'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars

def rotate(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'rotate'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def translate(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'translate'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def scale(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'scale'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def join(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'join'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def plane_cut(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'plane_cut'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def select_plane(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'select_plane'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def spherical_select(return_vars=None,
                     script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'spherical_select'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def extrude_bottom(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'extrude_bottom'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def extrude_plane(return_vars=None,
                  script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'extrude_plane'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def remove_vert_color(return_vars=None,
                  script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'remove_vert_color'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def remove_tex_color(return_vars=None,
                  script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'remove_tex_color'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def create_tex_mat(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'create_tex_mat'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def uv_smart_project(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'uv_smart_project'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def uv_cylinder_project(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'uv_cylinder_project'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def rotate_view(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'rotate_view'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def uv_project_from_view(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'uv_project_from_view'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def translate_uv(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'translate_uv'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def scale_uv(return_vars=None,
                   script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'scale_uv'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def boolean(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'boolean'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def measure_aabb(return_vars=None, script='TEMP3D_blender_default.py', **kwargs):
    """ Run the same function in bpylirious and return return_vars"""
    function = 'measure_aabb'
    write_bpyfunc(return_vars=return_vars, script=script,
                  function=function, **kwargs)
    return return_vars


def command(return_vars=None, script='TEMP3D_blender_default.py', cmd=None):
    """ Write the command verbatim to the script file

    """
    script_file = open(script, 'a')
    script_file.write(cmd + '\n')
    script_file.close()
    return return_vars


def run(script='TEMP3D_blender_default.py', log=None):
    """Run Blender in a subprocess and execute script.

    """
    cmd = 'blender --background --factory-startup --python "%s"' % script
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
        if (return_code == 0) or handle_error(program_name='Blender', cmd=cmd, log=log):
            break
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('***END OF BLENDER STDOUT & STDERR***\n')
        log_file.write('blender return code = %s\n\n' % return_code)
        log_file.close()
    return return_code
