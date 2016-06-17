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


def add2path(newpath):
    """Add newpath to the system PATH environment variable."""
    if newpath not in os.environ['PATH']:
        os.environ['PATH'] += os.pathsep + newpath


def setup_exe_paths():
    """Add external dependencies to the system path

    Currently supports the following programs on Win64:
        meshlabserver
        openscad
        admesh
        blender
        meshmixer

    """
    # TODO: add additional platform specific default locations,
    # e.g. Linux & MacOS
    if sys.version.split()[0] >= '3.3':
        if shutil.which('meshlabserver') is None:
            if platform.system() == 'Windows':
                add2path('C:\\Program Files\\VCG\\MeshLab')
        if shutil.which('openscad') is None:
            if platform.system() == 'Windows':
                add2path('C:\\Program Files\\OpenSCAD')
        if shutil.which('admesh') is None:
            if platform.system() == 'Windows':
                add2path('C:\\Program Files\\admesh')
        if shutil.which('blender') is None:
            if platform.system() == 'Windows':
                add2path('C:\\Program Files\\Blender Foundation\\Blender')
        if shutil.which('meshmixer') is None:
            if platform.system() == 'Windows':
                add2path('C:\\Program Files\\Autodesk\\Meshmixer')
    else:
        # If shutil.which is not available, skip checking path
        add2path('C:\\Program Files\\VCG\\MeshLab')
        add2path('C:\\Program Files\\OpenSCAD')
        add2path('C:\\Program Files\\admesh')
        add2path('C:\\Program Files\\Blender Foundation\\Blender')
        add2path('C:\\Program Files\\Autodesk\\Meshmixer')


if __name__ == "__main__":
    setup_exe_paths()
