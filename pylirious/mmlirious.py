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
sys.path.append(
    os.path.join(
        THIS_SCRIPTPATH,
        'mm-api-master',
        'distrib',
        'python'))
sys.path.append(
    os.path.join(
        THIS_SCRIPTPATH,
        'mm-api-master',
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
    object_id = mm.scene.append_objects_from_file(remote, file_in)
    print('object ID = %s' % object_id)
    return object_id


def open_mix(remote, file_in=None):
    mm.open_mix(remote, file_in)
    return None


def export_mesh(remote, object_id, file_out=None):
    mm.scene.select_objects(remote, object_id)
    mm.export_mesh(remote, file_out)
    return None


def hollow(remote, object_id, offset=2,
           solidResolution=128, meshResolution=128):
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
    mm.scene.select_objects(remote, object_id)
    mm.begin_tool(remote, 'hollow')
    mm.set_toolparam(remote, 'offsetDistanceWorld', offset)
    mm.set_toolparam(
        remote,
        'solidResolution',
        solidResolution)  # Solid Accuracy
    mm.set_toolparam(remote, 'meshResolution', meshResolution)  # Mesh Density
    mm.tool_utility_command(remote, 'update')
    mm.accept_tool(remote)
    return None


def makeSolid(remote, object_id, offset=None, minThickness=None,
              edgeCollapseThresh=None, solidType=None,
              solidResolution=None, meshResolution=None,
              closeHoles=True, transferFaceGroups=False):
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

    """
    mm.scene.select_objects(remote, object_id)
    mm.begin_tool(remote, 'makeSolid')

    if offset is not None:
        mm.set_toolparam(remote, 'offsetDistanceWorld', offset)
    if minThickness is not None:
        mm.set_toolparam(remote, 'minThicknessWorld', minThickness)
    if edgeCollapseThresh is not None:
        mm.set_toolparam(remote, 'edgeCollapseThresh', edgeCollapseThresh)
    if solidType is not None:
        mm.set_toolparam(remote, 'solidType', solidType)
    if solidResolution is not None:
        mm.set_toolparam(
            remote,
            'solidResolution',
            solidResolution)  # Solid Accuracy
    if meshResolution is not None:
        mm.set_toolparam(
            remote,
            'meshResolution',
            meshResolution)  # Mesh Density
    mm.set_toolparam(remote, 'closeHoles', closeHoles)
    mm.set_toolparam(remote, 'transferFaceGroups', transferFaceGroups)

    mm.tool_utility_command(remote, 'update')
    mm.accept_tool(remote)
    new_object_id = mm.scene.list_selected_objects(remote)
    print('new_object_id = %s' % new_object_id)
    return new_object_id


def scratch(remote):
    print(mm.list_selected_objects(remote))
    return None
