#!/usr/bin/env python

import sys
import subprocess
import re

def get_apk_infos(path):
    dump = subprocess.check_output(['aapt', 'dump', 'badging', path])
    package_spec = re.search(r'package: ([^\n]+)', dump).group(1)
    package_name = re.search(r"name='([^']+)'", package_spec).group(1)
    version_code = re.search(r"versionCode='([^']+)'", package_spec).group(1)
    version_name = re.search(r"versionName='([^']+)'", package_spec).group(1)

    return {'package_name': package_name,
            'version_code': version_code,
            'version_name': version_name}


if __name__ == '__main__':
    if len(sys.argv) == 2:
        for entry in get_apk_infos(sys.argv[1]).iteritems():
            print '%s="%s"' % entry
    elif len(sys.argv) == 3:
        print get_apk_infos(sys.argv[2])[sys.argv[1]]
