#!/usr/bin/python3
"""Rename a mesh file

Program to rename a mesh file, "slugify" it (remove any special or unwanted
characters) and add/check metadata ("scale" and "up" direction).
For obj files it will also rename its associated mtl and texture files.
For safety, this will not delete the original files; it will just make new copies.

Usage:
    Program accepts one filename as an argument. Can be provided on the
    command line or input file can be dragged & dropped on this script (if
    your system supports this method of running python files).

"""

# Builtin modules
import os
import sys
import re
from shutil import copy2

# Local modules
import meshlabxml as mlx
import pylirious

pylirious.setup_exe_paths()

if len(sys.argv) == 1:
    print('No arguments were provided; exiting...')
    sys.exit(1)


def rename_obj(old_fbasename, new_fbasename, new_fbasename_path,
               old_material_file, new_material_file):
    """ Copy obj file and rename mtl file references

    Will also rename references to itself.

    Read file line by line and write out at the same time, not storing the whole
    file in memory since the obj could be quite large

    Args:
        old_fbasename (str): name of old (current) obj file
        new_fbasename (str): name of new obj file
        new_fbasename_path (str): path and name of new obj file
        old_material_file (str): name of old (current) mtl file
        new_material_file (str): name of new mtl file

    """
    file_in = open(old_fbasename, 'r')
    file_out = open(new_fbasename_path, 'w')
    for line in file_in:
        file_out.write(line.replace(
            old_material_file,
            new_material_file).replace(old_fbasename, new_fbasename))
    file_in.close()
    file_out.close()


def rename_mtl(old_material_file, new_material_file_path,
               old_texture_files_unique, new_texture_files_unique):
    """Copy mtl file, renaming texture file references

    We'll load the whole mtl file in memory & then replace the texture references;
    performance should be fine since mtl files are pretty short.

    Args:
        old_material_file (str): name of old (current) material file
        new_material_file_path (str): path and name of new material file
        old_texture_files_unique (list of str): list of old (current) texture file names
        new_texture_files_unique (list of str): list of new texture file names

    """
    file_in = open(old_material_file).read()
    file_out = open(new_material_file_path, 'w')
    for i in range(0, len(old_texture_files_unique)):
        # Use re matching to match whole word; this prevents matching
        # the name of the material, which may also contain the texture name.
        # re.escape escapes any special characters that may be in name
        file_in = re.sub(r"\b" + re.escape(old_texture_files_unique[i]) + r"\b",
                         new_texture_files_unique[i], file_in)
    file_out.write(file_in)
    file_out.close()


def main():
    """Main function"""
    _, old_fbasename, _, log = pylirious.setup(sys.argv)

    old_fprefix, old_scale_meta, old_up_meta, fext = pylirious.filename.parse(
        old_fbasename, log)

    while True:
        # Request new name, find subfile (mtl and textures) of current file
        print()
        new_fprefix = input(' '.join([
            'Enter the subject or name of the mesh or hit ENTER to',
            'keep the current name "%s"' % old_fprefix,
            '(any invalid characters will be stripped or replaced): ']))
        if new_fprefix == '':
            new_fprefix = old_fprefix
        new_fprefix = pylirious.filename.slugify(new_fprefix)
        old_fprefix, new_scale_meta, new_up_meta, fext = pylirious.filename.check_metadata(
            old_fbasename, log)
        if (new_fprefix == old_fprefix) and (new_scale_meta ==
                                             old_scale_meta) and (new_up_meta == old_up_meta):
            wait = input(
                '\nFilename and metadata not changed, press ENTER to exit: ')
            os.remove(log)
            sys.exit(0)
        else:
            break
    _, old_texture_files_unique, old_material_file = mlx.find_texture_files(
        old_fbasename, log=log)
    new_texture_files_unique = []
    i = 0
    for fread in old_texture_files_unique:
        imgext = os.path.splitext(fread)[1][1:].strip().lower()
        new_texture_files_unique.append(
            '%s_texture_%s.%s' %
            (new_fprefix, str(i), imgext))
        i += 1
    new_fbasename = '%s(%s%s).%s' % (
        new_fprefix, new_scale_meta, new_up_meta, fext)
    if old_material_file is not None:
        new_material_file = '%s(%s%s).obj.mtl' % (
            new_fprefix, new_scale_meta, new_up_meta)
    else:
        new_material_file = None

    log_file = open(log, 'a')
    log_file.write('Old names:\n')
    log_file.write('old_fbasename = %s\n' % old_fbasename)
    log_file.write('old_fprefix = %s\n' % old_fprefix)
    log_file.write('old_scale_meta = %s\n' % old_scale_meta)
    log_file.write('old_up_meta = %s\n' % old_up_meta)
    log_file.write('old_material_file = %s\n' % old_material_file)
    log_file.write(
        'old_texture_files_unique = %s\n\n' %
        old_texture_files_unique)

    log_file.write('New names:\n')
    log_file.write('new_fbasename = %s\n' % new_fbasename)
    log_file.write('new_fprefix = %s\n' % new_fprefix)
    log_file.write('new_scale_meta = %s\n' % new_scale_meta)
    log_file.write('new_up_meta = %s\n' % new_up_meta)
    log_file.write('new_material_file = %s\n' % new_material_file)
    log_file.write(
        'new_texture_files_unique = %s\n\n' %
        new_texture_files_unique)
    log_file.close()

    print('\nOld model filename  = %s' % old_fbasename)
    print('Old material filename = %s' % old_material_file)
    if len(old_texture_files_unique) != 0:
        print('Old texture filename(s) = %s' % old_texture_files_unique)
    else:
        print('Old texture filename(s) = None')

    print('\nNew model filename  = %s' % new_fbasename)
    if fext == 'obj':
        print('New material filename = %s' % new_material_file)
        if len(new_texture_files_unique) != 0:
            print('New texture filename(s) = %s' % new_texture_files_unique)
        else:
            print('New texture filename(s) = None')

    #wait = input('\nPress ENTER to proceed with renaming files: ')

    ### Copy and rename files ###
    if (fext == 'obj') and (old_material_file is not None):
        rename_obj(old_fbasename, new_fbasename, new_fbasename,
                   old_material_file, new_material_file)
        if old_material_file is not None:
            rename_mtl(old_material_file, new_material_file,
                       old_texture_files_unique, new_texture_files_unique)
        # Copy texture files
        if len(old_texture_files_unique) > 0:
            for i in range(0, len(old_texture_files_unique)):
                copy2(old_texture_files_unique[i], new_texture_files_unique[i])
    else:
        copy2(old_fbasename, new_fbasename)

    wait = input(
        '\nPress ENTER to delete TEMP3D* files and log_file, or type "n" to keep them: ')
    if wait == '':
        mlx.util.delete_all('TEMP3D*')
        os.remove(log)
    return None

if __name__ == '__main__':
    main()
