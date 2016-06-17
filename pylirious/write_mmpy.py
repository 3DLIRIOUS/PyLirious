"""Module to create (write) a Python 2 script to be run by MeshMixer"""

import os
import sys
import subprocess
import time
from glob import glob


def begin(script='TEMP3D_mix_default.py'):
    script_file = open(script, 'w')
    script_file.write('\n'.join([
        '#! python 2',
        '""" MeshMixer Python 2.7 script created by pylirious.mix"""\n',
        'import os',
        'import sys',
        'import inspect',
        'from pylirious import mmlirious',
        '\n']))
    script_file.write('remote = mmlirious.begin()\n')
    script_file.close()
    return None


def end(script='TEMP3D_mix_default.py'):
    script_file = open(script, 'a')
    script_file.write('mmlirious.end(remote)\n')
    script_file.close()
    return None


def import_mesh(file_in=None, script='TEMP3D_mix_default.py',
                return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write(
            '%s = mmlirious.import_mesh(remote, "%s")\n' %
            (return_vars, file_in))
    else:
        script_file.write('mmlirious.import_mesh(remote, "%s")\n' % (file_in))
    script_file.close()
    return return_vars


def export_mesh(object_id=None, file_out=None,
                script='TEMP3D_mix_default.py', return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write('%s = mmlirious.export_mesh(remote, %s, "%s")\n' % (
            return_vars, object_id, file_out))
    else:
        script_file.write('mmlirious.export_mesh(remote, %s, "%s")\n' % (
            object_id, file_out))
    script_file.close()
    return return_vars


def makeSolid(object_id=None, offset=None, minThickness=None,
              edgeCollapseThresh=None, solidType=None,
              solidResolution=None, meshResolution=None,
              closeHoles=True, transferFaceGroups=False,
              script='TEMP3D_mix_default.py', return_vars=None):
    """ Run the same function in mmlirious and return return_vars"""
    script_file = open(script, 'a')
    if return_vars is not None:
        script_file.write(
            '%s = mmlirious.makeSolid(remote, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n' % (
                return_vars, object_id, offset, minThickness,
                edgeCollapseThresh, solidType, solidResolution,
                meshResolution, closeHoles, transferFaceGroups))
    else:
        script_file.write(
            'mmlirious.makeSolid(remote, %s, %s, %s, %s, %s, %s, %s, %s, %s)\n' % (
                object_id, offset, minThickness,
                edgeCollapseThresh, solidType, solidResolution,
                meshResolution, closeHoles, transferFaceGroups))
    script_file.close()
    return return_vars


def command(cmd=None, script='TEMP3D_mix_default.py'):
    """ Write the command verbatim to the script file"""
    script_file = open(script, 'a')
    script_file.write(cmd)
    script_file.close()


def run(script='TEMP3D_mix_default.py', log=None):
    """Run MeshMixer in a subprocess and execute script.

    """
    python27 = 'C:\\Python27\\pythonw.exe'
    cmd = '%s %s' % (python27, script)

    if log is not None:
        log_file = open(log, 'a')
        log_file.write('cmd = %s\n' % cmd)
        log_file.write('***START OF MESHMIXER STDOUT & STDERR***\n')
        log_file.close()
        log_file = open(log, 'a+')
    else:
        log_file = None
        print('meshmixer cmd = %s' % cmd)
        print('***START OF MESHMIXER STDOUT & STDERR***')
    while True:
        if log is not None:
            # Find position in log_file before launching MeshMixer
            start_pos = log_file.tell()
        # Launch MeshMixer
        mm_proc = subprocess.Popen(['meshmixer'], stdout=log_file,
                                   stderr=log_file, universal_newlines=True)

        if log is not None:
            # Read log_file to see when MeshMixer has finished opening and is
            # ready to process script
            mm_ready = False
            while not mm_ready:
                # Go to the start of MeshMixer's output
                log_file.seek(start_pos)
                for line in log_file:
                    # print(line)
                    # Looks like gaManager needs an internet connection. Use a different line.
                    # if '[gaManager] success!' in line:
                    if '[Setting up global event filter]' in line:
                        mm_ready = True
                # log_file.seek(0,2) # Go to the end of the file
                time.sleep(0.1)
        else:
            # Use a fixed delay if there is no log. May not be enough if your
            # computer is slow.
            time.sleep(5)

        # Run mm python script
        return_code = subprocess.call(cmd, shell=True, stdout=log_file,
                                      stderr=log_file, universal_newlines=True)
        # return_code = 1 # for testing
        mm_proc.terminate()
        log_file.close()

        if return_code == 0:
            break
        else:
            print('Houston, we have a problem.')
            print('MeshMixer did not finish sucessfully. Review the log',
                  'file and the input file(s) to see what went wrong.')
            print('MeshMixer command: "%s"' % cmd)
            print('log: "%s"' % log)
            print('\nWhere do we go from here?')
            print(' r  - retry running MeshMixer (probably after',
                  'you\'ve fixed any problems with the input files)')
            print(' c  - continue on with the script (probably after',
                  'you\'ve manually re-run and generated the desired',
                  'output file(s)')
            print(' x  - exit, keeping the TEMP3D file and log')
            print(' xd - exit, deleting the TEMP3D files and log')
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
                print('Deleting TEMP3D* and log files and exiting ...')
                delete_all('TEMP3D*')
                if log is not None:
                    os.remove(log)
                sys.exit(1)
            elif choice == 'c':
                print('Continuing on ...')
                break
            elif choice == 'r':
                print('Retrying MeshMixer cmd ...')
    if log is not None:
        log_file = open(log, 'a')
        log_file.write('***END OF MESHMIXER STDOUT & STDERR***\n')
        log_file.write('MeshMixer return code = %s\n\n' % return_code)
        log_file.close()
    return return_code


def delete_all(filename):
    """delete files in the current directory that match a pattern.

    Intended for temp files, e.g. mlx.delete('TEMP3D*').

    """
    for fread in glob(filename):
        os.remove(fread)
