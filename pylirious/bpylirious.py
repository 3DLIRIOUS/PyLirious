# This script is an example of how you can run blender from the command line
# (in background mode with no interface) to automate tasks, in this example it
# creates a text object, camera and light, then renders and/or saves it.
# This example also shows how you can parse command line options to scripts.
#
# Example usage for this test.
#  blender --background --factory-startup --python $HOME/background_job.py -- \
#          --text="Hello World" \
#          --render="/tmp/hello" \
#          --save="/tmp/hello.blend"
#
# Notice:
# '--factory-startup' is used to avoid the user default settings from
#                     interfering with automated scene generation.
#
# '--' causes blender to ignore all following arguments so python can use them.
#
# See blender --help for details.



"""Command line:
blender_path = "U:\\My Documents\\No.Backup.Zone\\Apps\\PA\\PortableApps\\BlenderPortable\\BlenderPortable.exe"

In cmd.exe:
set blender_path="U:\\My Documents\\No.Backup.Zone\\Apps\\PA\\PortableApps\\BlenderPortable\\App\\Blender64\\blender.exe"

%blender_path% --background --factory-startup --python bld_union.py
"""

import bpy
import bmesh
import os
import sys
import argparse
import inspect

# Find the path of this script and add it to python's path.
this_scriptpath = os.path.dirname(os.path.realpath(inspect.getsourcefile(lambda:0)))
sys.path.append(this_scriptpath)
import pylirious

def import_mesh(fin=None):
    fprefix, mScale, mUp, fext = pylirious.parse_filename(fin)
    
    if mUp is not None:
        up = mUp.upper()
        if up == 'Z':
            fwd = 'Y'
        else: # up == 'Y'
            fwd = '-Z'
    if fext == 'stl':
        if mUp is None:
            up = 'Z'
            fwd = 'Y'
        bpy.ops.import_mesh.stl(filepath=fin, axis_forward=fwd, axis_up=up, global_scale=1.0, use_scene_unit=True, use_facet_normal=False)
        meshObject = bpy.context.active_object
    elif fext == 'obj':
        if mUp is None:
            up = 'Y'
            fwd = '-Z'
        # Deselect all first; not sure if this is needed
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.import_scene.obj(filepath=fin, axis_forward=fwd, axis_up=up, use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=True, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clamp_size=0.0)
        #active = bpy.context.active_object
        #selection = bpy.context.selected_objects
        #print('active:', active)
        #print('active:', active.name)
        #print('selection:', [o.name for o in selection])
        #wait = input('pause')
        meshObject = bpy.context.selected_objects[0]
    elif fext == 'ply':
        bpy.ops.import_mesh.ply(filepath=fin)
        meshObject = bpy.context.active_object
    else:
        print('Error: filetype "%s" is not supported. Exiting ...' % fext)
        sys.exit(1)
    return meshObject

def export_mesh(obj_src=None, fout=None, texture=None):
    # Deselect All
    bpy.ops.object.select_all(action='DESELECT')
    # Select Source and make active
    obj_src.select = True
    bpy.context.scene.objects.active = obj_src

    fprefix, mScale, mUp, fext = pylirious.parse_filename(fout)
    rc = 0
    
    if mUp is not None:
        up = mUp.upper()
        if up == 'Z':
            fwd = 'Y'
        else: # up == 'Y'
            fwd = '-Z'
    
    if fext == 'stl':
        if mUp is None:
            up = 'Z'
            fwd = 'Y'
        bpy.ops.export_mesh.stl(filepath=fout, check_existing=True, axis_forward=fwd, axis_up=up, use_selection=True, global_scale=1.0, use_scene_unit=False, ascii=False, use_mesh_modifiers=True, batch_mode='OFF')
    elif fext == 'obj':
        if mUp is None:
            up = 'Y'
            fwd = '-Z'
        if texture is None:
            texture=True
        bpy.ops.export_scene.obj(filepath=fout, check_existing=True, axis_forward=fwd, axis_up=up, use_selection=True, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=True, use_uvs=texture, use_materials=texture, use_triangles=True, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=False, global_scale=1.0, path_mode='STRIP')
    elif fext == 'ply':
        if mUp is None:
            up = 'Y'
            fwd = '-Z'
        if texture is None:
            texture=False
        # Triangulate first
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        
        bpy.ops.export_mesh.ply(filepath=fout, check_existing=True, axis_forward=fwd, axis_up=up, use_mesh_modifiers=True, use_normals=True, use_uv_coords=texture, use_colors=True, global_scale=1.0)
    else:
        print('Error: filetype "%s" is not supported. Exiting ...' % fext)
        sys.exit(1)
    
    if not os.path.isfile(fout):
        print('Error: output file was not created')
        rc = 1
    return rc
    
def join():
    ...

def plane_cut():
    ...

def select_bottom():
    ...

def select_sphere():
    ...

def select_plane():
    ...

def extrude_bottom():
    ...
    
def bevel():
    ...

def smart_uv_project():
    ...

def boolean(obj_src=None,  operation='+', obj_trgt=None):
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
    op = {'+':'UNION', '-':'DIFFERENCE', '*':'INTERSECT'}
    
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
    mod.operation = op[operation]
    #mod[0].operation = 'DIFFERENCE'
    #mod[0].operation = 'INTERSECT'
    #mod[0].operation = 'UNION'

    # Apply modifier
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
    #bpy.ops.object.select_all(action='DESELECT')
    #obj_src.select = True
    #bpy.context.scene.objects.active = obj_src
    #rc = export_mesh(output, texture=False)
    #return rc
    return None

def begin():
    """Start of new Blender script; set the scene and clear existing objects"""
    scene = bpy.context.scene
    # Clear existing objects.
    scene.camera = None
    for obj in scene.objects:
        scene.objects.unlink(obj)
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
    parser.add_argument("-p", "--parameters", dest="parameters", nargs='*', action='append',  required=True, help="Supply parameters to the function")
    args = parser.parse_args(argv)
    #print('args = %s' % args)
    #print('args.function = %s' % args.function)
    #print('args.parameters = %s' % args.parameters)
    """for f in args.parameters:
        params=tuple(f)
        print(params)"""    
    
    begin()

    # Run function and provide parameters
    #rc = globals()[args.function](*params)
    rc = globals()[args.function](*args.parameters[0])
    return rc

if __name__ == '__main__':
    main()
