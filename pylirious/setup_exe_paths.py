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
    openscad_path = 'C:\\Program Files\\OpenSCAD'
    meshmixer_path = 'C:\\Program Files\\Autodesk\\Meshmixer'
    inkscape_path = 'C:\\Program Files\\Inkscape\\bin'    

    #meshlabserver_path = 'C:\\Program Files\\VCG\\MeshLab'
    meshlabserver_path = 'K:\\shared\\software\\3D\\MeshLab\\MeshLab2020.09-windows'
    #blender_path = 'C:\\Program Files\\Blender Foundation\\Blender'
    blender_path = 'K:\\shared\\software\\3D\\Blender\\Blender_Portable\\blender-2.79b-windows64'

    potrace_path = 'K:\\shared\\software\\2D\\potrace\\potrace-1.16.win64'
    apngopt_path = 'K:\\shared\\software\\2D\\apngopt\\apngopt-1.4-bin-win32'
    ffmpeg_path = 'K:\\shared\\software\\2D\\ffmpeg\\ffmpeg-7.1-full_build\\bin'
    
    pstoedit_path = 'C:\\Program Files\\pstoedit'
    admesh_path = 'K:\\shared\\software\\3D\\admesh\\admesh-win64-0.98.2'

def add2path(cmd, newpath):
    """Add `newpath` to the system PATH environment variable."""
    """Only add to path if `cmd` does not already exist in path"""
    if shutil.which(cmd) is None:
        if newpath not in os.environ['PATH']:
            #os.environ['PATH'] = newpath + os.pathsep + os.environ['PATH']
            os.environ['PATH'] += os.pathsep + newpath

def setup_exe_paths():
    """Add external dependencies to the system path."""
    add2path('openscad', openscad_path)
    add2path('meshmixer', meshmixer_path)
    add2path('inkscape', inkscape_path)
    add2path('meshlabserver', meshlabserver_path)
    add2path('blender', blender_path)

    add2path('potrace', potrace_path)
    add2path('apngopt', apngopt_path)
    add2path('ffmpeg', ffmpeg_path)

    add2path('pstoedit', pstoedit_path)
    add2path('admesh', admesh_path)

if __name__ == "__main__":
    setup_exe_paths()
