"""Module to create (write) a Python 2 script to be run by MeshMixer"""

import os
import sys
import inspect
import subprocess
import time
from glob import glob

def begin(s='MLTEMP_mix_default.py'):
    sf = open(s,'w')
    sf.write(
        '#! python 2\n'
        + '""" MeshMixer Python 2.7 script created by pylirious.mix"""\n\n'
        + 'import os\n'
        + 'import sys\n'
        + 'import inspect\n'
        + 'from pylirious import mmlirious\n'
        + '\n'
        )
    # Find the path of this script and add it to python's path.
    """this_scriptpath = os.path.dirname(os.path.realpath(inspect.getsourcefile(lambda:0)))
    # TODO: do we need to move this up a directory?
    sf.write(
        'sys.path.append(%s)\n' % this_scriptpath
        + 'import pylirious\n'
        )"""
    sf.write('r = mmlirious.begin()\n')
    sf.close()
    return None

def end(s='MLTEMP_mix_default.py'):
    sf = open(s,'a')
    sf.write('mmlirious.end(r)\n')
    sf.close()
    return None

def import_mesh(fin=None, s='MLTEMP_mix_default.py', return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = mmlirious.import_mesh(r, "%s")\n' % (return_vars, fin))
    else:
        sf.write('mmlirious.import_mesh(r, "%s")\n' % (fin))
    sf.close ()
    return return_vars

def export_mesh(object_id=None, fout=None, s='MLTEMP_mix_default.py', return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = mmlirious.export_mesh(r, %s, "%s")\n' % (
            return_vars, object_id, fout))
    else:
        sf.write('mmlirious.export_mesh(r, %s, "%s")\n' % (
            object_id, fout))
    sf.close ()
    return return_vars

def makeSolid(object_id=None,  offset=None, minThickness=None, edgeCollapseThresh=None, solidType=None, solidResolution=None, meshResolution=None, closeHoles=True, transferFaceGroups=False, s='MLTEMP_mix_default.py', return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    sf = open(s,'a')
    if return_vars is not None:
        sf.write('%s = mmlirious.makeSolid(r, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n' % (
            return_vars, object_id,  offset, minThickness, edgeCollapseThresh, solidType, solidResolution, meshResolution, closeHoles, transferFaceGroups))
    else:
        sf.write('mmlirious.makeSolid(r, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n' % (
            object_id,  offset, minThickness, edgeCollapseThresh, solidType, solidResolution, meshResolution, closeHoles, transferFaceGroups))
    sf.close ()
    return return_vars

def command(command=None, s='MLTEMP_mix_default.py'):
    """ Write the command verbatim to the script file"""
    sf = open(s,'a')
    sf.write(command)
    sf.close ()

def run(s='MLTEMP_mix_default.py', runlogname=None):
    
    python27 = 'C:\\Python27\\pythonw.exe'
    cmd = '%s %s' % (python27, s)
    
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('cmd = %s\n' % cmd)
        RUNLOG.write('***START OF MESHMIXER STDOUT & STDERR***\n')
        RUNLOG.close()
        RUNLOG = open(runlogname, 'a+')
    else:
        RUNLOG = None
        print('meshmixer cmd = %s' % cmd)
        print('***START OF MESHMIXER STDOUT & STDERR***')
    while True:
        
        #for a in follow(RUNLOG):
            #print(a)
        # Launch MeshMixer
        mm_proc = subprocess.Popen(['meshmixer'], stdout=RUNLOG,
                                   stderr=RUNLOG, universal_newlines=True)
        #time.sleep(5)
        
        
        if runlogname is not None:
        # Read RUNLOG to see when MeshMixer has finished opening and is ready to process script
            mmReady = False
            while not mmReady:
                RUNLOG.seek(0,0) # Go to the start of the file
                for line in RUNLOG:
                    #print(line)
                    if '[gaManager] success!' in line:
                        mmReady = True
                #RUNLOG.seek(0,2) # Go to the end of the file
                time.sleep(0.1)
        else:
        # Use a fixed delay if there is no runlog
            time.sleep(5)
            
        # Run mm python script
        return_code = subprocess.call(cmd, shell=True, stdout=RUNLOG,
                                   stderr=RUNLOG, universal_newlines=True)
        return_code = 1
        mm_proc.terminate()
        RUNLOG.close()

        if return_code == 0:
            break
        else:
            print('Houston, we have a problem.')
            print('MeshMixer did not finish sucessfully. Review the runlog file and the input file(s) to see what went wrong.')
            print('MeshMixer command: "%s"' % cmd)
            print('runlog: "%s"' % runlogname)
            print('\nWhere do we go from here?')
            print(' r  - retry running MeshMixer (probably after you\'ve fixed any problems with the input files)')
            print(' c  - continue on with the script (probably after you\'ve manually re-run and generated the deisred output file(s)')
            print(' x  - exit, keeping the MLTEMP file and runlog')
            print(' xd - exit, deleting the MLTEMP files and runlog')
            while True:
                choice = input('Select r, c, x, or xd: ')
                if choice not in ('r', 'c', 'x', 'xd'):
                    print('Please enter a valid option.')
                else:
                    break
            if choice == 'x':
                print('Exiting ...')
                sys.exit(1)
            elif choice == 'xd':
                print('Deleting MLTEMP* and runlog files and exiting ...')
                delete_all('MLTEMP*')
                if runlogname is not None:
                    os.remove(runlogname)
                sys.exit(1)
            elif choice == 'c':
                print('Continuing on ...')
                break
            elif choice == 'r':
                print('Retrying blender cmd ...')
    if runlogname is not None:
        RUNLOG = open(runlogname, 'a')
        RUNLOG.write('***END OF MESHMIXER STDOUT & STDERR***\n')
        RUNLOG.write('MeshMixer return code = %s\n\n' % return_code)
        RUNLOG.close()
    return return_code

def delete_all (filename):
    """delete files in the current directory that match a pattern. Intended for temp files, e.g. mlx.delete('MLTEMP*')"""
    for f in glob(filename):
        os.remove(f)

def follow(filename):
    filename.seek(0,2) # Go to the end of the file
    while True:
        line = filename.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield line