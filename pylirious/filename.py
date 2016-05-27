""" Functions to process filenames"""

#Builtin modules
import os
import sys
import unicodedata
import string

def parse(fbasename, runlogname = None):
    """ Parse filename, spltting it up into the filename
    prefix, file extension, and reading "Scale" and "Up"
    metadata."""
    fpref_full = os.path.splitext(fbasename)[0].strip()
    fext = os.path.splitext(fbasename)[1][1:].strip().lower()
    try:
        metadata = fbasename.rsplit('(')[-1].rsplit(').')[-2]
        fprefix = fpref_full.rsplit('(',1)[0]
        mScale = metadata[:-1]
        mUp = metadata[-1]
    except IndexError:
        metadata = None
        fprefix = fpref_full
        mScale = None
        mUp = None
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Parsed filename:\n')
        RUNLOG.write('fbasename = %s\n' % fbasename)
        RUNLOG.write('fpref_full = %s\n' % fpref_full)
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('metadata = %s\n' % metadata)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()
    return fprefix, mScale, mUp, fext

def check_metadata(fbasename, runlogname = None):
    """ Check filename metadata and make sure it is valid.
    
    If it is not valid, ask for input."""
    
    fprefix, mScale, mUp, fext = parse_filename(fbasename)
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Metadata values at start of check_metadata:\n')
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()

    # Check mScale
    mScaleDefault = '1' # this needs to be a string
    while True:
        if mlx.is_number(mScale):
            if mScale == 0:
                print ('Scale can\'t be zero!')
            else :
                break
        else :
            print ('Error: scale factor is not a valid number!\n')
        print ('Enter the current scale of the mesh.\n',
               'Valid values:\n',
               '  * Positive value greater than one, e.g. \"2\" means the ' +
               'mesh is twice its original size.\n',
               '  * Negative value for an inverse scale factor, (e.g. ' +
               '\"-10\" means 1/10th scale)\n',
               '  * Decimal value with period separator, (e.g. \"0.1\" ' +
               'for 1/10th scale)\n')
        mScale = input('Hit enter to accept the default' +
                        ' (\"%s\"): ' % mScaleDefault)
        if mScale == "":
            mScale = mScaleDefault

    # Check mUp, valid values are Y or Z
    if fext == 'stl':
        mUpDefault = 'Z'
    else:
        mUpDefault = 'Y'
    while True:
        if mUp == 'Y':
            break
        elif mUp == 'Z':
            break
        print('Enter the mesh \"up\" axis. Valid values are Y or Z.\n')
        mUp = input('Hit enter to accept the default' +
                        ' (\"%s\"): ' % mUpDefault)
        if mUp == "":
            mUp = mUpDefault

    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('Metadata values at end of check_metadata:\n')
        RUNLOG.write('fprefix = %s\n' % fprefix)
        RUNLOG.write('mScale = %s\n' % mScale)
        RUNLOG.write('mUp = %s\n' % mUp)
        RUNLOG.write('fext = %s\n\n' % fext)
        RUNLOG.close()
    return fprefix, mScale, mUp, fext

def slugify(fprefix):
    """ Ensure file prefix consists only of valid characters.
    
    Invalid characters will be replaced or stripped out.
    
    Currently this is very strict, only allowing letters, numbers, dashes,
    underscores and periods. 
    """
    fprefix = fprefix.replace(' ','_')
    # Notes: Shapeways doesn't like ampersands in mesh names or commas in texture names
    validFilenameChars = '-_.%s%s\n' % (string.ascii_letters, string.digits)
    cleanedFilename = unicodedata.normalize('NFKD', fprefix) #.encode('ascii', 'ignore')
    return ''.join(c for c in cleanedFilename if c in validFilenameChars)
