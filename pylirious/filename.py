""" Functions to process filenames

Parses and checks validity of metadata, slugify filename.

"""

from __future__ import print_function
from __future__ import division

import os
import unicodedata
import string

import meshlabxml as mlx


def parse(fbasename, log=None):
    """ Parse filename, spltting it up into the filename
    prefix, file extension, and reading "Scale" and "Up"
    metadata.

    """
    fpref_full = os.path.splitext(fbasename)[0].strip()
    fext = os.path.splitext(fbasename)[1][1:].strip().lower()
    try:
        metadata = fbasename.rsplit('(')[-1].rsplit(').')[-2]
        fprefix = fpref_full.rsplit('(', 1)[0]
        scale_meta = metadata[:-1]
        up_meta = metadata[-1]
    except IndexError:
        metadata = None
        fprefix = fpref_full
        scale_meta = None
        up_meta = None
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('Parsed filename:\n')
        log_file.write('fbasename = %s\n' % fbasename)
        log_file.write('fpref_full = %s\n' % fpref_full)
        log_file.write('fprefix = %s\n' % fprefix)
        log_file.write('metadata = %s\n' % metadata)
        log_file.write('scale_meta = %s\n' % scale_meta)
        log_file.write('up_meta = %s\n' % up_meta)
        log_file.write('fext = %s\n\n' % fext)
        log_file.close()
    return fprefix, scale_meta, up_meta, fext


def check_metadata(fbasename, log=None):
    """ Check filename metadata and make sure it is valid.

    If it is not valid, ask for valid input.

    """

    fprefix, scale_meta, up_meta, fext = parse(fbasename)
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('Metadata values at start of check_metadata:\n')
        log_file.write('fprefix = %s\n' % fprefix)
        log_file.write('scale_meta = %s\n' % scale_meta)
        log_file.write('up_meta = %s\n' % up_meta)
        log_file.write('fext = %s\n\n' % fext)
        log_file.close()

    # Check scale_meta
    scale_meta_default = '1'  # this needs to be a string
    while True:
        if mlx.util.is_number(scale_meta):
            if scale_meta == 0:
                print('Scale can\'t be zero!')
            else:
                break
        else:
            print('Error: scale factor is not a valid number!\n')
        print('Enter the current scale of the mesh.\n',
              'Valid values:\n',
              '  * Positive value greater than one, e.g. \"2\" means the',
              'mesh is twice its original size.\n',
              '  * Negative value for an inverse scale factor, (e.g.',
              '\"-10\" means 1/10th scale)\n',
              '  * Decimal value with period separator, (e.g. \"0.1\"',
              'for 1/10th scale)\n')
        scale_meta = input(' '.join(['Hit enter to accept the default',
                           '(\"%s\"): ' % scale_meta_default]))
        if scale_meta == "":
            scale_meta = scale_meta_default

    # Check up_meta, valid values are Y or Z
    if fext == 'stl':
        up_meta_default = 'Z'
    else:
        up_meta_default = 'Y'
    while True:
        if up_meta == 'Y':
            break
        elif up_meta == 'Z':
            break
        print('Enter the mesh \"up\" axis. Valid values are Y or Z.\n')
        up_meta = input(' '.join(['Hit enter to accept the default',
                        '(\"%s\"): ' % up_meta_default]))
        if up_meta == "":
            up_meta = up_meta_default

    if log is not None:
        log_file = open(log, 'a')
        log_file.write('Metadata values at end of check_metadata:\n')
        log_file.write('fprefix = %s\n' % fprefix)
        log_file.write('scale_meta = %s\n' % scale_meta)
        log_file.write('up_meta = %s\n' % up_meta)
        log_file.write('fext = %s\n\n' % fext)
        log_file.close()
    return fprefix, scale_meta, up_meta, fext


def slugify(fprefix):
    """ Ensure file prefix consists only of valid characters.

    Invalid characters will be replaced or stripped out.

    Currently this is very strict, only allowing letters, numbers, dashes,
    underscores and periods.
    """
    fprefix = fprefix.replace(' ', '_')
    # Notes: Shapeways doesn't like ampersands in mesh names or commas in
    # texture names
    valid_chars = '-_.%s%s\n' % (string.ascii_letters, string.digits)
    cleaned_filename = unicodedata.normalize(
        'NFKD', fprefix)  # .encode('ascii', 'ignore')
    return ''.join(c for c in cleaned_filename if c in valid_chars)
