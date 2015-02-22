Python MOSS Script
==================

Helper script to upload a bunch of files downloaded from a Moodle or Canvas
course to MOSS to find hints of plagiarism.

Usage
-----

Must have the `moss` perl script in same directory with username and password
filled out.

```
python moss.py [-a assignment_name] [-d] [-l c|python] [-m]
```

Options:
 * -a Assignment name. Will be used in directory naming when uploading to MOSS.
 * -d Whether to delete the directories created in unzipping the files.
 * -l Language -- either 'c' or 'python'
 * -m Whether this is a Moodle course or not (default: no, Canvas)
