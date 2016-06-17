""" Pylirious's Blender Python 3 module

Use within blender

At the start of each function you should be in OBJECT mode.
"""

# Blender modules
import bpy
import bmesh
from mathutils import Vector

# Built-in modules
import os
import sys
import argparse
import inspect
import math

# Sub-modules
from . import filename


def import_mesh(file_in=None):
    fprefix, scale_meta, up_meta, fext = filename.parse(file_in)

    if up_meta is not None:
        up = up_meta.upper()
        if up == 'Z':
            fwd = 'Y'
        else:  # up == 'Y'
            fwd = '-Z'
    if fext == 'stl':
        if up_meta is None:
            up = 'Z'
            fwd = 'Y'
        bpy.ops.import_mesh.stl(
            filepath=file_in,
            axis_forward=fwd,
            axis_up=up,
            global_scale=1.0,
            use_scene_unit=True,
            use_facet_normal=False)
        mesh_object = bpy.context.active_object
    elif fext == 'obj':
        if up_meta is None:
            up = 'Y'
            fwd = '-Z'
        # Deselect all first; not sure if this is needed
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.obj(
            filepath=file_in,
            axis_forward=fwd,
            axis_up=up,
            use_edges=True,
            use_smooth_groups=True,
            use_split_objects=True,
            use_split_groups=True,
            use_groups_as_vgroups=False,
            use_image_search=True,
            split_mode='ON',
            global_clamp_size=0.0)
        #active = bpy.context.active_object
        #selection = bpy.context.selected_objects
        #print('active:', active)
        #print('active:', active.name)
        #print('selection:', [o.name for o in selection])
        #wait = input('pause')
        mesh_object = bpy.context.selected_objects[0]
    elif fext == 'ply':
        bpy.ops.import_mesh.ply(filepath=file_in)
        mesh_object = bpy.context.active_object
    else:
        print('Error: filetype "%s" is not supported. Exiting ...' % fext)
        sys.exit(1)
    # Apply any rotations
    bpy.ops.object.transform_apply(rotation=True)

    # Deselect all in edit mode
    # Object must be active to switch into edit mode
    bpy.context.scene.objects.active = mesh_object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    return mesh_object


def export_mesh(mesh_object=None, file_out=None, texture=None):
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    fprefix, scale_meta, up_meta, fext = filename.parse(file_out)
    return_code = 0

    if up_meta is not None:
        up = up_meta.upper()
        if up == 'Z':
            fwd = 'Y'
        else:  # up == 'Y'
            fwd = '-Z'

    if fext == 'stl':
        if up_meta is None:
            up = 'Z'
            fwd = 'Y'
        bpy.ops.export_mesh.stl(
            filepath=file_out,
            check_existing=True,
            axis_forward=fwd,
            axis_up=up,
            use_selection=True,
            global_scale=1.0,
            use_scene_unit=False,
            ascii=False,
            use_mesh_modifiers=True,
            batch_mode='OFF')
    elif fext == 'obj':
        if up_meta is None:
            up = 'Y'
            fwd = '-Z'
        if texture is None:
            texture = True
        bpy.ops.export_scene.obj(
            filepath=file_out,
            check_existing=True,
            axis_forward=fwd,
            axis_up=up,
            use_selection=True,
            use_mesh_modifiers=True,
            use_edges=True,
            use_smooth_groups=False,
            use_smooth_groups_bitflags=False,
            use_normals=True,
            use_uvs=texture,
            use_materials=texture,
            use_triangles=True,
            use_nurbs=False,
            use_vertex_groups=False,
            use_blen_objects=True,
            group_by_object=False,
            group_by_material=False,
            keep_vertex_order=False,
            global_scale=1.0,
            path_mode='STRIP')
    elif fext == 'ply':
        if up_meta is None:
            up = 'Y'
            fwd = '-Z'
        if texture is None:
            texture = False
        # Triangulate first
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.quads_convert_to_tris(
            quad_method='BEAUTY', ngon_method='BEAUTY')

        bpy.ops.export_mesh.ply(
            filepath=file_out,
            check_existing=True,
            axis_forward=fwd,
            axis_up=up,
            use_mesh_modifiers=True,
            use_normals=True,
            use_uv_coords=texture,
            use_colors=True,
            global_scale=1.0)
    else:
        print('Error: filetype "%s" is not supported. Exiting ...' % fext)
        sys.exit(1)

    if not os.path.isfile(file_out):
        print('Error: output file was not created')
        return_code = 1
    return return_code


def rotate(mesh_object=None, axis='z', angle=0.0, apply=True):
    """ Rotate object """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    angle = math.radians(angle)
    if axis.lower() == 'x':
        mesh_object.rotation_euler = (angle, 0.0, 0.0)
    elif axis.lower() == 'y':
        mesh_object.rotation_euler = (0.0, angle, 0.0)
    elif axis.lower() == 'z':
        mesh_object.rotation_euler = (0.0, 0.0, angle)
    else:
        print('Axis name is not valid; exiting ...')
        sys.exit(1)
    # Do we need to apply rotation?
    if apply:
        bpy.ops.object.transform_apply(rotation=True)
    return None


def translate(mesh_object=None, value=(0.0, 0.0, 0.0), apply=True):
    """ translate object """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    mesh_object.location += Vector(value)

    # Do we need to apply translation?
    if apply:
        bpy.ops.object.transform_apply(location=True)
    return None


def join(objects=None):
    """ Join objects. Objects must be iterable (list, tuple, etc.) """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    for mesh_object in objects:
        mesh_object.select = True

    bpy.ops.object.join()
    return None


def separate(mesh_object):
    """ Separate object by loose parts """

    bpy.ops.mesh.separate(type='LOOSE')
    # How to select subsequent objects and assign them to variables?


def plane_cut(mesh_object=None, axis='z', offset=0.0):
    """ Plane cut using  the bisect operator """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    if axis.lower() == 'x':
        plane_no = (1.0, 0.0, 0.0)
        plane_co = (offset, 0.0, 0.0)
    elif axis.lower() == 'y':
        plane_no = (0.0, 1.0, 0.0)
        plane_co = (0.0, offset, 0.0)
    elif axis.lower() == 'z':
        plane_no = (0.0, 0.0, 1.0)
        plane_co = (0.0, 0.0, offset)

    # Select all
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.bisect(
        plane_co=plane_co,
        plane_no=plane_no,
        use_fill=True,
        clear_inner=True,
        clear_outer=False,
        threshold=0.0001,
        xstart=0,
        xend=0,
        ystart=0,
        yend=0)

    # Triangulate faces
    bpy.ops.mesh.quads_convert_to_tris(
        quad_method='BEAUTY', ngon_method='BEAUTY')

    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def extrude_bottom(mesh_object=None, threshold=0.00001, distance=6):
    """ Select all vertices on the XY plane (Z = 0) and extrude"""
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Get the active mesh
    #me = bpy.context.object.data

    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(mesh_object.data)

    for vert in bm.verts:
        if -threshold <= vert.co.z <= threshold:
            vert.select = True

    # Select edges
    """for edge in bm.edges:
        if edge.verts[0].select and edge.verts[1].select:
            edge.select = True"""

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(mesh_object.data)
    bm.free()

    # Switch to edit mode to view selection
    bpy.ops.object.mode_set(mode='EDIT')

    # Change to vertex selection mode to ensure that vertices are selected
    bpy.ops.mesh.select_mode(type='VERT')
    # Change to face select mode to select faces encompassed by vertices
    bpy.ops.mesh.select_mode(type='FACE')

    # Extrude bottom
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (0, 0, -distance),
            "constraint_axis": (False, False, True),
            "constraint_orientation": 'GLOBAL'})

    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def extrude_plane(mesh_object=None, center=(0.0, 0.0, 0.0),
                  radius=1, angle=1, distance=6):
    """ Select all vertices on the XY plane (Z = 0) and extrude"""
    center = Vector(center)
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(mesh_object.data)

    # Select all faces with their center median within a circle of
    # radius=radius
    for face in bm.faces:
        vert1 = mesh_object.matrix_world * face.calc_center_median()  # global face median
        face.select = ((center - vert1).length <= radius)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(mesh_object.data)
    bm.free()

    # Switch to edit mode to view selection
    bpy.ops.object.mode_set(mode='EDIT')

    # Change to face select mode
    bpy.ops.mesh.select_mode(type='FACE')

    # Select linked flat faces
    bpy.ops.mesh.faces_select_linked_flat(sharpness=math.radians(angle))

    # Extrude bottom
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (0, 0, -distance),
            "constraint_axis": (False, False, True),
            "constraint_orientation": 'GLOBAL'})

    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def bevel():
    ...


def smart_uv_project():
    ...


def boolean(obj_src=None, operation='+', obj_trgt=None):
    """Perform a boolean operation on a source mesh with a target mesh.

    The result of the operation will be exported to the output file.

    Args:
        source (str): filename of mesh to be modified.
        operation(str) = symbol for the boolean operation to perform:
            + = UNION
            - = DIFFERENCE
            * = INTERSECT
        target (str): filename of mesh to act on the source
        output (str): filename to export the result to

    Returns:
        None
    """
    operation_dict = {'+': 'UNION', '-': 'DIFFERENCE', '*': 'INTERSECT'}

    print(
        '\nPerforming boolean:\n'
        '%s %s %s\n' % (obj_src.name, operation, obj_trgt.name)
    )

    #obj_src = import_mesh(source)
    #obj_trgt = import_mesh(target)
    print('obj_src: %s' % obj_src.name)
    print('obj_trgt: %s' % obj_trgt.name)

    #active = bpy.context.active_object
    #selection = bpy.context.selected_objects
    #print('active:', active.name)
    #print('selection:', [o.name for o in selection])

    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    obj_src.select = True
    bpy.context.scene.objects.active = obj_src

    # Add a modifier
    bpy.ops.object.modifier_add(type='BOOLEAN')

    mod = obj_src.modifiers[0]
    mod.name = 'mybool'
    mod.object = obj_trgt
    mod.operation = operation_dict[operation]
    #mod[0].operation = 'DIFFERENCE'
    #mod[0].operation = 'INTERSECT'
    #mod[0].operation = 'UNION'

    # Apply modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
    # bpy.ops.object.select_all(action='DESELECT')
    #obj_src.select = True
    #bpy.context.scene.objects.active = obj_src
    #return_code = export_mesh(output, texture=False)
    # return return_code
    return None


def begin():
    """Start of new Blender script; set the scene and clear existing objects"""
    scene = bpy.context.scene
    # Clear existing objects.
    scene.camera = None
    for mesh_object in scene.objects:
        scene.objects.unlink(mesh_object)
    return None


def main():
    # get the args passed to blender after "--", all of which are ignored by
    # blender so scripts may receive their own arguments
    argv = sys.argv
    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    # When --help or no args are given, print this help
    usage_text = (
        'Select a Blender function to run and provide parameters'
        'bpylirious -f boolean -p source target')
    parser = argparse.ArgumentParser(description=usage_text)

    # Example utility, add some text and renders or saves it (with options)
    # Possible types are: string, int, long, choice, float and complex.
    parser.add_argument("-f", "--function", dest="function", type=str, required=True,
                        help="The function in this module that you want to call")
    parser.add_argument(
        "-p",
        "--parameters",
        dest="parameters",
        nargs='*',
        action='append',
        required=True,
        help="Supply parameters to the function")
    args = parser.parse_args(argv)
    #print('args = %s' % args)
    #print('args.function = %s' % args.function)
    #print('args.parameters = %s' % args.parameters)
    """for f in args.parameters:
        params=tuple(f)
        print(params)"""

    begin()

    # Run function and provide parameters
    #return_code = globals()[args.function](*params)
    return_code = globals()[args.function](*args.parameters[0])
    return return_code

if __name__ == '__main__':
    main()
