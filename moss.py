#!/usr/bin/python

import getopt
import os
import re
import subprocess
import sys

prefix = ''
error = []
output = ''
valid_archives = ['.tar.gz', '.tar', '.tgz', '.zip', '.7z', '.jar']
valid_endings = {
    'python' : ['.py'],
    'c' : ['.h', '.c'],
    'java' : ['.java']
}

#From http://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
def istext(path):
    output = subprocess.Popen(["file", '-L', path], stdout=subprocess.PIPE).stdout.read()
    #print(output)
    return b'text' in output

def valid_archive_name(path):
    for e in valid_archives:
        if path.endswith(e):
            return True
    return False

def valid_code_name(path, mode):
    for e in valid_endings[mode]:
        if path.endswith(e):
            return True
    return False

def extract(path, destination):
    if path.endswith('.tar'):
        return not os.system('tar -xf "{}" -C "{}"'.format(path, destination))
    elif path.endswith('.tar.gz') or path.endswith('.tgz'):
        return not os.system('tar -zxf "{}" -C "{}"'.format(path, destination))
    elif path.endswith('.zip') or path.endswith('.jar'):
        return not os.system('unzip "{}" -d "{}"'.format(path, destination))
    elif path.endswith('.7z'):
        return not os.system('7za x "{}" "-o{}"'.format(path, destination))
    return False


def gather_files(parent_path, mode):
    valid_files = []
    for directory, junk, files in os.walk(parent_path):
        for f in files:
            f = directory + '/' + f
            print(f)
            if valid_code_name(f, mode):
                if istext(f):
                    valid_files.append(f)
                else:
                    error.append('{} is not a text file. Check manually.'.format(f))
    return valid_files

def main():
    options, args = getopt.getopt(sys.argv[1:], 'a:dl:m', ['assignment',
        'delete', 'language', 'moodle'])
    mode = 'python'
    moodle = False
    tmp_file = None
    auto_delete = False
    for option, value in options:
        if option in ['-a', '--assignment']:
            tmp_file = value
        elif option in ['-d', '--delete']:
            auto_delete = True
        elif option in ['-l', '--language']:
            mode = value.lower()
        elif option in ['-m', '--moodle']:
            moodle = True
        print(option, value)

    if not tmp_file:
        tmp_file = input('Assignment name? ')

    for f in os.listdir('.'):
        if f.endswith('.zip'):
            delete_all_tar = True
            os.system('unzip "{}" -d {}'.format(f, tmp_file))

    for f in os.listdir(tmp_file):
        if valid_archive_name(f):
            if moodle:
                l = f.split('_')[0].split(' ')
                last_name, first_name = l[-1], l[0]
                dirname = prefix + last_name + '_' + first_name
                os.system('mkdir "{}/{}"'.format(tmp_file, dirname))

                f = tmp_file + '/' + f
            else:
                last_name, first_name = f.split('_')[0].split('--', 1)
                first_name = first_name.split('-')[0] #remove possible '-late'
                dirname = prefix + last_name + '_' + first_name
                os.system('mkdir "{}/{}"'.format(tmp_file, dirname))

                f = tmp_file + '/' + f

            if not extract(f, tmp_file + '/' + dirname):
                print('File failed to extract: {}.'.format(f))
                #sys.exit()

    c = "find ./" + tmp_file + " -depth -name \"* *\" -execdir perl-rename 's/ /_/g' \"{}\" \;"
    os.system(c);

    base_files = gather_files('base', mode)
    student_files = gather_files(tmp_file, mode)

    base = ''
    if len(base_files) > 0:
        base = '-b ' + ' -b '.join(base_files)
    student = '"' + '" "'.join(student_files) + '"'

    #print output
    command = './moss -l {lang} -d {base} {student}'.format(base = base, student = student, lang = mode)
    print('Uploading {} files.'.format(len(base_files) + len(student_files)))
    #print command
    os.system(command)

    if not auto_delete:
        input('Press enter to delete created files.')

    print('Deleting extra files.')
    os.system('rm -rf "{}"'.format(tmp_file))

    if len(error):
        print('ERRORS:')
        for e in error:
            print(e)


if __name__ == '__main__':
    main()
