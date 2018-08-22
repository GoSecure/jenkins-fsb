#!/usr/bin/env python

import xml.etree.ElementTree as ET
import os
import re
import subprocess

SIMPLE_TYPES = {
    'V': 'void',
    'B': 'byte',
    'C': 'char',
    'S': 'short',
    'I': 'int',
    'J': 'long',
    'F': 'float',
    'D': 'double',
    'Z': 'boolean'
}


def find_source_path(class_name):
    return '/'.join(class_name.split('.')) + '.java'


def parse_jni_types(t):
    '''Extract approximate types from a JNI type list'''

    if t is None:
        return []

    types = []
    i = 0

    while i < len(t):
        if t[i] in SIMPLE_TYPES:
            types.append(SIMPLE_TYPES[t[i]])

        if t[i] == 'L':
            class_name = t[i+1:]

            # class name ends with ;
            class_name = class_name[:class_name.index(';')]

            # take only the class, not the package
            class_name = class_name.split('/')[-1]

            # take the nested class if present
            class_name = class_name.split('$')[-1]

            types.append(class_name)

            i += t[i:].index(';') - 1

        i += 1

    return types


def parse_jni_signature(sig):
    '''
    Generate a regex to match a type declaration using the JNI signature
    '''

    groups = re.match(r"(\(([^\)]*)\)(.*)|.*)", sig).groups()

    if len(groups) == 3:
        _, arguments, return_type = groups

        return parse_jni_types(arguments), parse_jni_types(return_type)
    else:
        pass
        # it's probably a field


def find_method_line(source, class_name, method_name, method_signature):
    arguments, return_type = parse_jni_signature(method_signature)
    regex = ''
    i = 0

    # if method is constructor of static initializer
    if method_name in ['<init>', '<clinit>']:
        method_name = class_name.split('.')[-1].split('$')[-1]
    else:
        regex += return_type[0]
        regex += '(<.*>)? ' # handle type parameters before method name

    regex += method_name + '\\('

    for arg in arguments:
        regex += '.*'
        regex += arg

    regex += '.*\)'

    regex = re.compile(regex)

    for line in source:
        if regex.search(line):
            return i

        i += 1

    return -1


def main():
    tree = ET.parse('target/findbugsXml.xml')
    messages = ET.parse('/scripts/messages.xml')

    for bug in tree.findall('BugInstance'):
        bug_type = bug.attrib['type']
        class_node = bug.find('Class')
        method_node = bug.find('Method')
        message = messages.findtext('BugPattern[@type="%s"]/ShortDescription' % bug_type)
        message = 'FSB %s: %s' % (bug_type, message)
        class_name = class_node.attrib['classname']
        file_path = 'src/' + find_source_path(class_name)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                source = f.readlines()

            if method_node is not None:
                method_name = method_node.attrib['name']
                method_signature = method_node.attrib['signature']
                index = find_method_line(source, class_name, method_name, method_signature)
            else:
                index = -1

            if index == -1:
                source.append('// ' + message + '\n')
            else:
                source[index] = source[index].rstrip() + ' // ' + message + ' ' + '\n'

            source = ''.join(source)

            with open(file_path, 'w') as f:
                f.write(source)

            commit_msg = "%s %s" % (bug_type, class_name + "#" + method_name)

            subprocess.call(['git', 'add', file_path])
            subprocess.call(['git', 'commit', '-m', commit_msg])


if __name__ == '__main__':
    main()
