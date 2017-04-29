
# PyLirious

Assorted Python modules for 3D model creation and processing for 3D printing.

* Run stand-alone scripts on:
  * [Blender](https://www.blender.org/)
  * [MeshMixer](http://www.meshmixer.com/)
  * [MeshLab](http://www.meshlab.net/)
* Script with multiple programs, exchanging mesh data by importing and exporting files.
* Script with MeshLab and MeshMixer from within Blender.
* Includes [mm-api](https://github.com/meshmixer/mm-api) for MeshMixer scripting
* Filename metadata handling for scale and "up" direction

----
## Requirements

Both  Python 3.X (64-bit preferred) and 32-bit Python 2.7 (for mmlirious, mm-api and MeshMixer) are needed. For a fresh install, Python 3 should be installed last so that it is the default.

[MeshLabXML](https://github.com/3DLIRIOUS/MeshLabXML) is also required (will be installed automatically with pip)

----
## Installation

Installation examples are for Windows; modify paths accordingly for your operating system.

Installing in Python 3.X (should be the default python) with pip:
```sh
pip install pylirious
```

Installing in python 2.7 with pip:
```sh
"C:\Python27\python.exe" -m pip install pylirious
```

Installing in Blender's Python 3 with pip; Blender doesn't come with pip, so we have to install it first:
1. Download [get-pip.py](https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py)
2. Install pip
```sh
"C:\Program Files\Blender Foundation\Blender\2.78\python\bin\python.exe" get-pip.py
```
3. Install pylirious
```sh
"C:\Program Files\Blender Foundation\Blender\2.78\python\bin\python.exe" -m pip install pylirious
```

Install the following versions of the supported software:
* Blender 2.78
* MeshMixer 3.0(build 11.0.544)
* MeshLab 1.3.4BETA

----
## Metadata

To assist with scripting and exchanging mesh files between programs, certain metadata about the meshes must be known, namely its scale and "up" direction. As the various file formats do not have consistent mechanisms to store this data, it is stored at the end of the in filename in parentheses, for example "my_scan(-10Z).stl". Values:
 * Scale: the scale of the model with respect to the physical world, which is important for 3D scans and for 3D printing objects at the correct size. This is a floating point number. Positive values mean the model is larger than reality, for example a value of 2 means the model is twice as large. Negative values indicate an inverse scale, for example -10 means the model is 1:10 scale.
 * "Up" direction: one of the silliest things about 3D software is that no one can agree on which way is up! Generally speaking, CAD programs (and 3D printing) use Z as the up direction, while more "artistic" programs use Y up, however there are enough exceptions that this cannot be relied on. Only Y and Z directions are supported.

----
## Modules

* **pylirious** - functions to run Blender scripts and render OpenSCAD files to stl, plus various other functions that don't seem to fit anywhere else.
* **bpylirious** - a Blender Python module (runs within Blender). Most functions operate on mesh objects. The largest module, it contains functions to manipulate meshes, create textures and UV maps, and more. 
* **mmlirious** - a Python 2.7 module to script with MeshMixer. Currently only supports a few functions, including hollow and make_solid.
* **filename** - functions to parse and check metadata and "slugify" filenames.
* **setup_exe_paths** - simple module to add the program executable directories to the system path; useful if you can't (or don't want to) change your environment variables.


----
## License
[LGPL version 2.1](http://www.gnu.org/licenses/old-licenses/lgpl-2.1.en.html)
