""" Pylirious's Blender Python 3 module

Use within blender

At the start of each function you should be in OBJECT mode.
"""

# Built-in modules
import os
import sys
import argparse
import inspect
import math

# Blender modules
import bpy
import bmesh
from mathutils import Vector

# Sub-modules
from . import filename


def begin():
    """Start of new Blender script; set the scene and clear existing objects"""
    scene = bpy.context.scene
    # Clear existing objects.
    scene.camera = None
    for mesh_object in scene.objects:
        scene.objects.unlink(mesh_object)
    return None


def import_mesh(file_in=None):
    _, _, up_meta, fext = filename.parse(file_in)

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
        # ply files are assumed to be Z up; rotate if it is Y up.
        bpy.ops.import_mesh.ply(filepath=file_in)
        mesh_object = bpy.context.active_object
        if up_meta.upper() == 'Y':
            rotate(mesh_object=mesh_object, axis='x', angle=90.0, apply=False)
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


def export_mesh(mesh_object=None, file_out=None, texture=None, triangulate=True):
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    _, _, up_meta, fext = filename.parse(file_out)
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
        if triangulate:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.quads_convert_to_tris(
                quad_method='BEAUTY', ngon_method='BEAUTY')
            bpy.ops.object.mode_set(mode='OBJECT')
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


def duplicate_mesh(mesh_object):
    """ Duplicate mesh object
    
    This function is causeing blender to crash if we duplicate after
    performing a boolean. Why? It is the bpy.ops.object.duplicate
    function that causes it.
    Note that script still executes correctly.
    The problem is related to duplicating an object that is already a duplicate,
    e.g. duplicating, dropping colors, then duplicating again.
    Workaround is to duplicate the orginal multiple times.
    """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    bpy.ops.object.duplicate(linked=False, mode="TRANSLATION")
    #bpy.ops.object.duplicate()
    
    #bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "constraint_axis":(False, False, False), "constraint_orientation":'GLOBAL', "mirror":False, "proportional":'DISABLED', "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False})

    dupe_mesh_object = bpy.context.selected_objects[0]
    return dupe_mesh_object


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

    if apply:
        bpy.ops.object.transform_apply(location=True)
    return None


def scale(mesh_object=None, value=(0.0, 0.0, 0.0), apply=True):
    """ scale object """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    mesh_object.scale = Vector(value)

    if apply:
        bpy.ops.object.transform_apply(scale=True)
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
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    bpy.ops.mesh.separate(type='LOOSE')
    # How to select subsequent objects and assign them to variables?
    # Could query all the current objects & save to list, separate mesh,
    # then re-query and compare the two lists to find the new objects
    # bpy.context.scene.objects ?


def plane_cut(mesh_object=None, axis='z', offset=0.0, direction=1,
              use_fill=True, clear_inner=True, clear_outer=False,
              threshold=0.0001, triangulate=False):
    """ Plane cut using  the bisect operator """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Switch to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    if axis.lower() == 'x':
        plane_co = (offset, 0.0, 0.0)
        if direction >= 0:
            plane_no = (1.0, 0.0, 0.0)
        else:
            plane_no = (-1.0, 0.0, 0.0)
    elif axis.lower() == 'y':
        plane_co = (0.0, offset, 0.0)
        if direction >= 0:
            plane_no = (0.0, 1.0, 0.0)
        else:
            plane_no = (0.0, -1.0, 0.0)
    elif axis.lower() == 'z':
        plane_co = (0.0, 0.0, offset)
        if direction >= 0:
            plane_no = (0.0, 0.0, 1.0)
        else:
            plane_no = (0.0, 0.0, -1.0)

    # Select all
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.bisect(
        plane_co=plane_co,
        plane_no=plane_no,
        use_fill=use_fill,
        clear_inner=clear_inner,
        clear_outer=clear_outer,
        threshold=threshold,
        xstart=0,
        xend=0,
        ystart=0,
        yend=0)

    # Triangulate faces
    if triangulate:
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.quads_convert_to_tris(
            quad_method='BEAUTY', ngon_method='BEAUTY')

    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def select_plane(mesh_object=None, axis='z', offset=0.0,
                 threshold=0.00001, method='FACE', clear_selection=False):
    """ Select all the vertices or faces along a plane """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Clear any exisitng selections
    if clear_selection:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(mesh_object.data)

    for vert in bm.verts:
        if axis.lower() == 'x':
            if (offset - threshold) <= vert.co.x <= (offset + threshold):
                vert.select = True
        elif axis.lower() == 'y':
            if (offset - threshold) <= vert.co.y <= (offset + threshold):
                vert.select = True
        elif axis.lower() == 'z':
            if (offset - threshold) <= vert.co.z <= (offset + threshold):
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

    if method == 'FACE':
        # Change to face select mode to select faces encompassed by vertices
        bpy.ops.mesh.select_mode(type='FACE')
    # NOTE: still in EDIT mode
    return None


def spherical_select(mesh_object=None, center=(0.0, 0.0, 0.0),
                     radius=1, method='FACE', clear_selection=False):
    """Select within a spherical volume with center and radius

    Select either by face centers or vertices.

    At the end, will be in edit mode with the faces or vertices selected.
    """
    center = Vector(center)
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Clear any exisitng selections
    if clear_selection:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(mesh_object.data)

    if method == 'FACE':
        # Select all faces with their center median within a sphere of
        # radius=radius
        for face in bm.faces:
            vert1 = mesh_object.matrix_world * face.calc_center_median()  # global face median
            face.select = ((center - vert1).length <= radius)
    else:  # VERT
        # Select all vertices with within a circle of radius=radius
        for vert in bm.verts:
            vert.select = ((center - vert.co).length <= radius)

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(mesh_object.data)
    bm.free()

    # Switch to edit mode to view selection
    bpy.ops.object.mode_set(mode='EDIT')

    if method == 'FACE':
        # Change to face select mode
        bpy.ops.mesh.select_mode(type='FACE')
    else:  # VERT
        # Change to vert select mode
        bpy.ops.mesh.select_mode(type='VERT')
    # NOTE: still in EDIT mode
    return None


def extrude_bottom(mesh_object=None, threshold=0.00001, distance=6):
    """ Select all vertices on the XY plane (Z = 0) and extrude"""
    select_plane(
        mesh_object=mesh_object,
        axis='z',
        offset=0.0,
        threshold=threshold,
        method='FACE')

    # Extrude bottom
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (0.0, 0.0, -distance),
            "constraint_axis": (False, False, True),
            "constraint_orientation": "GLOBAL"})

    # Switch to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def extrude_plane(mesh_object=None, center=(0.0, 0.0, 0.0),
                  radius=1, angle=1, distance=6):
    """ Select all faces with centers within spherical radius and center,
        select connected plane, and extrude distance"""
    spherical_select(mesh_object, center, radius, 'FACE')

    # Select linked flat faces
    bpy.ops.mesh.faces_select_linked_flat(sharpness=math.radians(angle))

    # Extrude bottom
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (0, 0, -distance),
            "constraint_axis": (False, False, True),
            "constraint_orientation": 'GLOBAL'})

    # Switch to OBJECT mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return None


def remove_vert_color(mesh_object=None):
    """ Drop vertex colors from mesh """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    bpy.ops.mesh.vertex_color_remove()
    return None


def remove_tex_color(mesh_object=None):
    """Unlink images, textures, UV maps and materials from source object

    """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Remove images
    for texlay in mesh_object.data.uv_textures:
        for tf in texlay.data:
            tf.image = None

    # Remove textures
    for i in range(len(mesh_object.data.materials)):
        mesh_object.data.materials[i].active_texture = None

    # Remove UV maps
    bpy.ops.mesh.uv_texture_remove()

    # Remove materials
    mesh_object.data.materials.pop(0, update_data=True)
    return None


def create_tex_mat(mesh_object=None, image_file=None,
                   tex_name='texture_0', mat_name='material_0'):
    """ Create texture and material for mesh object.

    Presumes that UV map and image file already exist
    """
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    bpy.ops.object.mode_set(mode='EDIT')

    # Create image texture from image.
    tex = bpy.data.textures.new(tex_name, type="IMAGE")

    # Note: this needs to be the full path to the file
    tex.image = bpy.data.images.load(image_file)

    # Create Material
    mat = bpy.data.materials.new(mat_name)
    mat.use_shadeless = True
    mtex = mat.texture_slots.add()
    mtex.texture = tex
    mtex.texture_coords = "UV"
    mtex.use_map_color_diffuse = True
    mesh_object.data.materials.append(mat)

    # Set image in UV Editing window
    bpy.data.screens["UV Editing"].areas[1].spaces[0].image = tex.image

    # This is not needed. Not sure under what circumstances it would be needed.
    # bpy.context.object.active_material.texture_slots[0].uv_layer = "UVMap"

    bpy.ops.object.mode_set(mode="OBJECT")
    return


def uv_smart_project(mesh_object=None, angle_limit=66.0,
                     island_margin=0.0, user_area_weight=0.0,
                     use_aspect=True, stretch_to_bounds=True):
    """ UV map the selected mesh using smart project"""
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=angle_limit, island_margin=island_margin, user_area_weight=user_area_weight, use_aspect=use_aspect, stretch_to_bounds=stretch_to_bounds)
    bpy.ops.object.mode_set(mode="OBJECT")
    return None


def rotate_view(view='TOP', perspective='ORTHO'):
    """ Rotate to a numpad view """
    # Need to set correct context to modify 3D View
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            break

    for region in area.regions:
        if region.type == "WINDOW":
            break

    space = area.spaces[0]

    context = bpy.context.copy()
    context['area'] = area
    context['region'] = region
    context['space_data'] = space

    space.region_3d.view_perspective = perspective
    bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type=view)
    bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type=view)

    return None


def uv_project_from_view(view='TOP', perspective='ORTHO', camera_bounds=False,
                         correct_aspect=True, scale_to_bounds=True):
    """

    This presumes that you are in EDIT mode and have the faces selected that
    you wish to project

    view (enum in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', 'BACK', 'CAMERA'])
    perspective (enum in ['ORTHO', 'PERSP']): perspective/orthographic projection


    http://blender.stackexchange.com/questions/34488/view3d-operations-problem
    """
    # Need to set correct context to modify 3D View
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            break

    for region in area.regions:
        if region.type == "WINDOW":
            break

    space = area.spaces[0]

    context = bpy.context.copy()
    context['area'] = area
    context['region'] = region
    context['space_data'] = space

    # This swaps between orthographic and perspective projection
    #bpy.ops.view3d.view_persportho(context, 'EXEC_DEFAULT')

    space.region_3d.view_perspective = perspective

    # This needs to be run twice, otherwise the projection will happen
    # at some intermediate roation point.
    # I'm not sure why this is.
    # Adding a time delay after this command has no impact on this
    # I'm also not sure what the 'EXEC_DEFAULT' argument does, or if it's really needed
    bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type=view)
    bpy.ops.view3d.viewnumpad(context, 'EXEC_DEFAULT', type=view)

    bpy.ops.uv.project_from_view(context, 'EXEC_DEFAULT', camera_bounds=camera_bounds, correct_aspect=correct_aspect, scale_to_bounds=scale_to_bounds)
    return None


def scale_uv(mesh_object=None, value=(0.0, 0.0), center=(0.5, 0.5)):
    """ Let's try this using bmesh """
    list(value)
    list(center)

    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    mesh_object.select = True
    bpy.context.scene.objects.active = mesh_object

    # Get a BMesh representation
    bm = bmesh.new()
    bm.from_mesh(mesh_object.data)

    uv_lay = bm.loops.layers.uv.active

    for face in bm.faces:
        for loop in face.loops:
            uv = loop[uv_lay].uv
            # Scale about center point: S(x-c) + c
            uv[0] = value[0] * (uv[0] - center[0]) + center[0]
            uv[1] = value[1] * (uv[1] - center[1]) + center[1]

    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(mesh_object.data)
    bm.free()
    return None


def scale_uv_gui(value=(0.0, 0.0)):
    """ Scale selected UV coordinates in IMAGE_EDITOR

    Need to be in EDIT mode

    This works when run inside the GUI, but not from a script!

    """
    value = value + (1.0,)
    original_area = bpy.context.area.type
    # change current area to image editor
    bpy.context.area.type = 'IMAGE_EDITOR'

    # insert UV specific transforms here
    bpy.ops.transform.resize(value=value, constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

    # return to previouswindow for good measure ( and cleanliness )
    bpy.context.area.type = original_area
    return None


def bevel():
    pass


def boolean(obj_src=None, operation='+', obj_trgt=None, solver='CARVE'):
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
    mod.solver = solver
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


def measure_aabb(mesh_object):
    """ Find the axis aligned bounding box of the mesh object"""
    # Note that bound_box is not axis aligned. Will it be if all rotations are applied first?

    # Convert boundign box corners from object space to world space
    #bbox_corners = [ob.matrix_world * Vector(corner) for corner in ob.bound_box]

    # Let's do this using veritces instead
    """
    matrix_w = mesh_object.matrix_world
    vectors = [matrix_w * vertex.co for vertex in mesh_object.data.vertices]
    aabb = {'min': [x_co, y_co, z_co], 'max': [x_co, y_co, z_co]}

    return min(vectors, key=lambda item: item.z)
    """

    aabb = {'min': [999999.0, 999999.0, 999999.0], 'max': [-999999.0, -999999.0, -999999.0]}

    for vertex in mesh_object.data.vertices:
        # object vertices are in object space, translate to world space
        v_world = mesh_object.matrix_world * Vector((vertex.co[0], vertex.co[1], vertex.co[2]))

        if v_world[0] < aabb['min'][0]:
            aabb['min'][0] = v_world[0]
        if v_world[1] < aabb['min'][1]:
            aabb['min'][1] = v_world[1]
        if v_world[2] < aabb['min'][2]:
            aabb['min'][2] = v_world[2]
        if v_world[0] > aabb['max'][0]:
            aabb['max'][0] = v_world[0]
        if v_world[1] > aabb['max'][1]:
            aabb['max'][1] = v_world[1]
        if v_world[2] > aabb['max'][2]:
            aabb['max'][2] = v_world[2]

    aabb['center'] = [(aabb['max'][0] + aabb['min'][0]) / 2,
                      (aabb['max'][1] + aabb['min'][1]) / 2,
                      (aabb['max'][2] + aabb['min'][2]) / 2]
    aabb['size'] = [aabb['max'][0] - aabb['min'][0], aabb['max'][1] - aabb['min'][1],
                    aabb['max'][2] - aabb['min'][2]]
    aabb['diagonal'] = math.sqrt(
        aabb['size'][0]**2 +
        aabb['size'][1]**2 +
        aabb['size'][2]**2)
    return aabb


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
