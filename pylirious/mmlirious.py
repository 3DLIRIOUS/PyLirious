#! python2.7
""" Python 2.7 functions to script MeshMixer"""

from __future__ import print_function
from __future__ import division
import os
import sys
import inspect

from . import filename

# Need to add mm-api to path and import locally since it is not yet in PyPi
# Find the path of this script and add it to python's path.
THIS_SCRIPTPATH = os.path.dirname(
    os.path.realpath(
        inspect.getsourcefile(
            lambda: 0)))
sys.path.insert(
    0, os.path.join(
        THIS_SCRIPTPATH,
        'mm-api',
        'distrib',
        'python'))
sys.path.insert(
    0, os.path.join(
        THIS_SCRIPTPATH,
        'mm-api',
        'python'))

import mmapi
from mmRemote import *
import mm


def begin():
    """Start of new MeshMixer script; initialize connection"""
    remote = mmRemote()
    remote.connect()
    return remote


def end(remote):
    remote.shutdown()
    return None


def import_mesh(remote, file_in=None):
    """

    mesh_object: the object ID of the mesh object
    """

    mesh_object = mm.scene.append_objects_from_file(remote, file_in)
    print('object ID = %s' % mesh_object)
    return mesh_object


def open_mix(remote, file_in=None):
    mm.open_mix(remote, file_in)
    return None


def export_mesh(remote, mesh_object, file_out=None):
    mm.scene.select_objects(remote, mesh_object)
    mm.export_mesh(remote, file_out)
    return None


def hollow(remote, mesh_object, offset=2,
           solid_resolution=128, mesh_resolution=128):
    """ Hollow mesh

    offsetDistance 	float
    offsetDistanceWorld 	float   GUI default: 2
    holeRadiusWorld 	float
    holeTaperWorld 	float
    hollowType 	integer
    solidResolution 	integer   GUI default: this depends on the mesh size. Try using 256 as default
    meshResolution 	integer   GUI default: 128
    holesPerComponent 	integer

    """
    mm.scene.select_objects(remote, mesh_object)
    mm.begin_tool(remote, 'hollow')
    mm.set_toolparam(remote, 'offsetDistanceWorld', offset)
    mm.set_toolparam(
        remote,
        'solidResolution',
        solid_resolution)  # Solid Accuracy
    mm.set_toolparam(remote, 'meshResolution', mesh_resolution)  # Mesh Density
    mm.tool_utility_command(remote, 'update')
    mm.accept_tool(remote)
    return None


def make_solid(remote, mesh_object, offset=None, min_thickness=None,
               edge_collapse_thresh=None, solid_type=None,
               solid_resolution=None, mesh_resolution=None,
               close_holes=True, transfer_face_groups=False):
    """ Make Solid tool
    offsetDistance : float ; default 0
    offsetDistanceWorld : float
    minThickness : float ; default 0
    minThicknessWorld : float
    edgeCollapseThresh : float ; default 100
    solidType : integer ; default 1 (Fast)
        0 = Blocky
        1 = Fast
        2 = Accurate (Required for offset & minThickness)
        3 = Sharp Edge Preserve
    solidResolution : integer ; default 128
    meshResolution : integer ; default 128
    closeHoles : boolean ; default True
    transferFaceGroups : boolean ; default False

    http://www.mmmanual.com/make-solid/
    Make Solid approximates your object with small cubes (voxels).
    This approximation actually happens twice. First we voxelize
    the shape using solid_resolution as the sampling rate. Then we
    use a second set of voxels to create a mesh of the first voxel
    approximation; mesh_resolution is the sampling rate of this second
    voxelization. These sampling rates can be the same, but they do
    not have to be.

    """
    mm.scene.select_objects(remote, mesh_object)
    mm.begin_tool(remote, 'makeSolid')

    if offset is not None:
        mm.set_toolparam(remote, 'offsetDistanceWorld', offset)
    if min_thickness is not None:
        mm.set_toolparam(remote, 'minThicknessWorld', min_thickness)
    if edge_collapse_thresh is not None:
        mm.set_toolparam(remote, 'edgeCollapseThresh', edge_collapse_thresh)
    if solid_type is not None:
        mm.set_toolparam(remote, 'solidType', solid_type)
    if solid_resolution is not None:
        mm.set_toolparam(
            remote,
            'solidResolution',
            solid_resolution)  # Solid Accuracy
    if mesh_resolution is not None:
        mm.set_toolparam(
            remote,
            'meshResolution',
            mesh_resolution)  # Mesh Density
    mm.set_toolparam(remote, 'closeHoles', close_holes)
    mm.set_toolparam(remote, 'transferFaceGroups', transfer_face_groups)

    mm.tool_utility_command(remote, 'update')
    mm.accept_tool(remote)
    new_mesh_object = mm.scene.list_selected_objects(remote)
    print('new_mesh_object = %s' % new_mesh_object)
    return new_mesh_object


def scratch(remote):
    print(mm.list_selected_objects(remote))
    return None
