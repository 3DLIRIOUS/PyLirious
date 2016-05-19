"""Module to create (write) a Python script to be run by Blender"""

import os
import sys
import inspect
import subprocess

def begin(s='MLTEMP_default.mlx'):
    sf = open(s,'w')
    sf.write(
        '""" Blender Python script created by pylirious.writebpy"""\n\n'
        + 'import bpy\n' 
        + 'import bmesh\n'
        + 'import os\n'
        + 'import sys\n'
        + 'import argparse\n'
        + 'import inspect\n\n'
        )
    # Find the path of this script and add it to python's path.
    this_scriptpath = os.path.dirname(os.path.realpath(inspect.getsourcefile(lambda:0)))
    # TODO: do we need to move this up a directory?
    sf.write(
        'sys.path.append(%s)\n' % this_scriptpath
        + 'import pylirious\n'
        )
    sf.write('def pylirious.bpy.begin()')
    sf.close()
    return None

def import_mesh(fin=None, s='MLTEMP_default.mlx', return_vars=None):
    """ Run the same function in bpylirios and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpy.import_mesh(%s)' % (return_vars, fin))
    else:
        sf.write('pylirious.bpy.import_mesh(%s)' % (fin))
    
    return None

def export_mesh(fout=None, texture=None, s='MLTEMP_default.mlx', return_vars=None):
    """ Run the same function in bpylirios and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpy.export_mesh(%s, %s)' % (
            return_vars, fout, texture))
    else:
        sf.write('pylirious.bpy.export_mesh(%s, %s)' % (fout, texture))
    return None

def boolean(source=None,  operation='+', target=None, output=None,
            s='MLTEMP_default.mlx', return_vars=None):
    """ Run the same function in bpylirios and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = pylirious.bpy.boolean(%s, %s, %s, %s)' % (
            return_vars, source, operation, target, output))
    else:
        sf.write('pylirious.bpy.boolean(%s, %s, %s, %s)' % (
            source, operation, target, output))
    return None


