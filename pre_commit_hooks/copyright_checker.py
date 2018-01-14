from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io, re
import sys, os
import commands
import platform

COPYRIGHT = '''
  Copyright (c) 2016 PaddlePaddle Authors. All Rights Reserve.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

LANG_COMMENT_MARK = None

NEW_LINE_MARK = None

COPYRIGHT_HEADER = None

if platform.system() == "Windows":
  NEW_LINE_MARK = "\r\n"
else:
  NEW_LINE_MARK = '\n'
  COPYRIGHT_HEADER = COPYRIGHT.split(NEW_LINE_MARK)[1]
  p = re.search('(\d{4})', COPYRIGHT_HEADER).group(0)
  date = commands.getoutput("date +%Y")
  COPYRIGHT_HEADER = COPYRIGHT_HEADER.replace(p, date)
 
def generate_copyright(template, lang='C'):
  if lang == 'Python':
    LANG_COMMENT_MARK = '#'
  else:
    LANG_COMMENT_MARK = "\\\\"

  lines = template.split(NEW_LINE_MARK)
  ans = LANG_COMMENT_MARK + COPYRIGHT_HEADER + NEW_LINE_MARK
  for lino, line in enumerate(lines):
    if lino == 0 or lino == 1 or lino == len(lines)-1 : continue
    ans += LANG_COMMENT_MARK + line + NEW_LINE_MARK

  return ans

def lang_type(filename):
  if filename.endswith(".py"):
    return "Python"
  else:
    return "C"

def main(argv=None):
    parser = argparse.ArgumentParser(description='Checker for copyright declaration.')
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    retv = 0
    for filename in args.filenames:
        first_line = io.open(filename).readline()
        if "Copyright" in first_line: continue
        original_contents = io.open(filename).read()
        new_contents = generate_copyright(COPYRIGHT, lang_type(filename)) + original_contents
        print('Auto Insert Copyright Header {}'.format(filename))
        retv = 1
        with io.open(filename, 'w') as output_file:
          output_file.write(new_contents)

    return retv


if __name__ == '__main__':
  exit(main())