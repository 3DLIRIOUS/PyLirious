#!/usr/bin/python3
"""Pylirious module

Miscellaneous functions to work with 3D models in Python 3.

"""

import os
import sys
import platform
import inspect
import subprocess
from datetime import datetime

import meshlabxml as mlx

from . import filename
from . import write_mmpy

def render_scad(script=None, log=None, file_out=None, constants=None):
    """Run openscad and render a scad script to an output file.

    OpenSCAD will not start the GUI, but execute the given file and export the result to the output_file in a format depending on the extension (.stl / .off / .dxf, .csg).
    constants (dict): dictionary of variable:value pairs to override with constants (uses -D switch)
    Unlike normal OpenSCAD assignments, these assignments don't define variables, but constants, which can not be changed inside the program, and can thus be used to overwrite values defined in the program at export time.

    If you want to assign the -D variable to another variable, the -D variable MUST be initialised in the main .scad program

    """
    if platform.system() == 'Windows':
        cmd = 'openscad.com '
    else:
        cmd = 'openscad '
    cmd += '-o %s ' % file_out

    if log is not None:
        log_file = open(log, 'a')
        log_file.write('//OpenSCAD constants for %s\n\n' % script)
    if constants is not None:
        for key, value in constants.items():
            if isinstance(value, str):
                cmd += '-D "%s=\\"%s\\"" ' % (key, value)
                if log is not None:
                    log_file.write('%s="%s";\n' % (key, value))
            else:
                cmd += '-D %s=%s ' % (key, value)
                if log is not None:
                    log_file.write('%s=%s;\n' % (key, value))
    cmd += '%s' % script
    if log is not None:
        log_file.write('\n\ncmd = %s\n\n' % cmd)
        log_file.write('***START OF OPENSCAD STDOUT & STDERR***\n')
        log_file.close()
        log_file = open(log, 'a')
    else:
        log_file = None
        print('openscad cmd = %s' % cmd)
        print('***START OF OPENSCAD STDOUT & STDERR***')
    while True:
        return_code = subprocess.call(cmd, shell=True, stdout=log_file,
                                      stderr=log_file, universal_newlines=True)
        if log is not None:
            log_file.close()
        if (return_code == 0) or mlx.handle_error(program_name='OpenSCAD', cmd=cmd, log=log):
            break
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('***END OF OPENSCAD STDOUT & STDERR***\n')
        log_file.write('openscad return code = %s\n\n' % return_code)
        log_file.close()
    return return_code


def run_admesh():
    pass


def swap_yz(file_in, file_out=None, log=None):
    """ Swap a mesh "Up" direction betwenn "Y" and "Z" axes.

    Requires metadata to know what the current "Up" direction is.

    """
    fprefix, scale_meta, up_meta, fext = filename.check_metadata(file_in)
    if up_meta.upper() == 'Y':  # Y to Z: rotate 90d about X
        up_meta = 'Z'
        angle = 90.0
    elif up_meta.upper() == 'Z':  # Z to Y: rotate -90d about X
        up_meta = 'Y'
        angle = -90.0

    if file_out is None:
        file_out = '%s(%s%s).%s' % (fprefix, scale_meta, up_meta, fext)
    script = 'TEMP3D_swapYZ.mlx'

    mlx.begin(script, file_in=file_in)
    mlx.transform.rotate(script, axis='x', angle=angle)
    mlx.end(script)
    mlx.run(log=log, file_in=file_in, file_out=file_out, script=script)
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
        if (return_code == 0) or mlx.handle_error(program_name='Blender', cmd=cmd, log=log):
            break
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
    fpath = os.path.dirname(os.path.abspath(sys.argv[1]))
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


def hollow_volume(fullpath_in, fullpath_out, log, offset=-3,
                  solid_resolution=128, mesh_resolution=128):
    """ Create hollow (offset) volume using MeshMixer
    
    Make Solid approximates your object with small cubes (voxels).
    This approximation actually happens twice. First we voxelize
    the shape using solid_resolution as the sampling rate. Then we
    use a second set of voxels to create a mesh of the first voxel
    approximation; mesh_resolution is the sampling rate of this second
    voxelization. These sampling rates can be the same, but they do
    not have to be.
    -- MeshMixer manual
    """
    mix_script = 'TEMP3D_mix_hollow.py'

    write_mmpy.begin(mix_script)
    obj_a = write_mmpy.import_mesh(
        'obj_a',
        mix_script,
        file_in=fullpath_in)
    obj_b = write_mmpy.make_solid(
        'obj_b',
        mix_script,
        mesh_object=obj_a,
        offset=offset,
        solid_type=2,
        solid_resolution=solid_resolution,
        mesh_resolution=mesh_resolution)
    write_mmpy.export_mesh(
        None,
        mix_script,
        mesh_object=obj_b,
        file_out=fullpath_out)
    write_mmpy.end(mix_script)
    write_mmpy.run(mix_script, log)
    
    return None


def scale_meta2scale(scale_meta):
    scale_meta_float = mlx.util.to_float(scale_meta)
    if scale_meta_float < 0.0:
        scale = -1.0 / scale_meta_float
    else:
        scale = scale_meta_float
    return scale
