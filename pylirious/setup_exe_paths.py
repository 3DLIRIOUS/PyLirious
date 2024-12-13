#!/usr/bin/env python3
"""Add external dependencies to the system path

If the required dependencies (most notably meshlabserver) are not on
your system path, you can define their locations here. Useful for
portable usage where you may not want to (or can't) permanently
modify the system path.

Requires python >= 3.3 for the shutil.which function.

License:
    Written in 2016 by Tim Ayres 3DLirious@gmail.com

    To the extent possible under law, the author(s) have dedicated all
    copyright and related and neighboring rights to this software to the
    public domain worldwide. This software is distributed without any
    warranty.

    You should have received a copy of the CC0 Public Domain Dedication
    along with this software. If not, see
    <http://creativecommons.org/publicdomain/zero/1.0/>.

"""

import os
import sys
import shutil
import platform

# TODO: add additional platform specific default locations,
# e.g. Linux & MacOS
if platform.system() == 'Windows':
    #meshlabserver_path = 'C:\\Program Files\\VCG\\MeshLab'
    meshlabserver_path = 'K:\\shared\\software\\3D\\MeshLab\\MeshLab2020.09-windows'
    openscad_path = 'C:\\Program Files\\OpenSCAD'
    admesh_path = 'C:\\Program Files\\admesh'
    #blender_path = 'C:\\Program Files\\Blender Foundation\\Blender'
    blender_path = 'K:\\shared\\software\\3D\\Blender\\Blender_Portable\\blender-2.79b-windows64'
    meshmixer_path = 'C:\\Program Files\\Autodesk\\Meshmixer'
    inkscape_path = 'C:\\Program Files\\Inkscape'
    pstoedit_path = 'C:\\Program Files\\pstoedit'


def add2path(newpath):
    """Add newpath to the system PATH environment variable."""
    if newpath not in os.environ['PATH']:
        #os.environ['PATH'] = newpath + os.pathsep + os.environ['PATH']
        os.environ['PATH'] += os.pathsep + newpath


def setup_exe_paths():
    """Add external dependencies to the system path."""
    if sys.version.split()[0] >= '3.3':
        if shutil.which('meshlabserver') is None:
            add2path(meshlabserver_path)
        if shutil.which('openscad') is None:
            add2path(openscad_path)
        if shutil.which('admesh') is None:
            add2path(admesh_path)
        if shutil.which('blender') is None:
            add2path(blender_path)
        if shutil.which('meshmixer') is None:
            add2path(meshmixer_path)
        if shutil.which('inkscape') is None:
            add2path(inkscape_path)
        if shutil.which('pstoedit') is None:
            add2path(pstoedit_path)
    else:
        # If shutil.which is not available, skip checking path
        add2path(meshlabserver_path)
        add2path(openscad_path)
        add2path(admesh_path)
        add2path(blender_path)
        add2path(meshmixer_path)
        add2path(inkscape_path)
        add2path(pstoedit_path)


if __name__ == "__main__":
    setup_exe_paths()
