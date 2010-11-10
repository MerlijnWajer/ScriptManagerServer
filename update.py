#!/usr/bin/env python

#
#   update.py: XML List Updater
#   Part of the Simba project
#
#   This file produces a list.xml file based on the Scripts/ directory.
#
#   See the COPYING file on redistribution of this package.   
#   Merlijn Wajer, 2010
#

def add_node_value(d, r, n, v):
    t = d.createElement(n)
    v = d.createTextNode(v)
    r.appendChild(t)
    t.appendChild(v)


import xml.dom.minidom

doc = xml.dom.minidom.Document()

scripts = doc.createElement('Scripts')
doc.appendChild(scripts)

version = doc.createElement('Version')
version_v = doc.createTextNode('0.01')
scripts.appendChild(version)
version.appendChild(version_v)

scriptlist = doc.createElement('ScriptList')
scripts.appendChild(scriptlist)

import os

os.chdir(os.getcwd() + '/Scripts')
script_dir = os.getcwd()
script_folders = os.listdir(script_dir)

for folder in script_folders:
    os.chdir(script_dir + '/' + folder)
    info_files = os.listdir(os.getcwd())

    script_files = os.listdir(os.getcwd() + '/files')

    scriptnode = doc.createElement('Script')
    scriptlist.appendChild(scriptnode)

    add_node_value(doc, scriptnode, 'Name', folder)

    if 'version' in info_files:
        vers = open('version')
        sv = ''.join(vers.readlines())[:-1]
        add_node_value(doc, scriptnode, 'Version', sv)
        del vers
    else:
        raise Exception('Version file not found')

    if 'author' in info_files:
        auth = open('author')
        sa = ''.join(auth.readlines())[:-1]
        add_node_value(doc, scriptnode, 'Author', sa)
        del auth
    else:
        raise Exception('Author file not found')

    if 'tags' in info_files:
        tags = open('tags')
        scripttags = map(lambda x: x[:-1], tags.readlines())
        if len(scripttags) > 0:
            taglist = doc.createElement('Tags')
            scriptnode.appendChild(taglist)
            for tag in scripttags:
                add_node_value(doc, taglist, 'Tag', tag)

        del tags
    else:
        raise Exception('Tags file not found')

    if 'description' in info_files:
        desc = open('description')
        ds = ''.join(desc.readlines())[:-1]
        add_node_value(doc, scriptnode, 'Description', ds)
        del desc
    else:
        raise Exception('Description file not found')

    if len(script_files) > 0:
        sfiles = doc.createElement('Files')
        scriptnode.appendChild(sfiles)
        for sf in script_files:
            add_node_value(doc, sfiles, 'File', sf)



#print doc.toprettyxml(indent='    ')
print doc.toxml()

#from os.path import join, getsize
#for root, dirs, files in os.walk(os.getcwd()):
#    if '.git' in dirs:
#        dirs.remove('.git')
#        continue
#    print 'root:',root
#    print [name for name in files]


