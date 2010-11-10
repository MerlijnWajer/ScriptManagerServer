#!/usr/bin/env python
from flup.server.fcgi import WSGIServer
from webtool import WebTool
import re
import subprocess
import bz2
import os

BASE_URL = '/sm'
BASE_PATH = '/home/merlijn/sm'

os.chdir(BASE_PATH)

def sm(env, start_response):
    r = wt.apply_rule(env['REQUEST_URI'])
    if r is None:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        r = '404: %s' % env['REQUEST_URI']
    elif type(r) in (dict,):
        start_response('200 OK', [('Content-Type', r['ftype'])])
        r = r['data']
    else:
        start_response('200 OK', [('Content-Type', 'text/html;charset=utf8')])

    return [r]

def tarball(name=None):
    folders = os.listdir('%s/Scripts/' % BASE_PATH)

    dirs = os.listdir('Scripts')

    if not name in dirs:
        return None

    os.chdir('Scripts')

    outp = subprocess.Popen(['git', 'archive', '--format=tar', 'HEAD',
        name], stdout=subprocess.PIPE)
    d = outp.stdout.read()
    c = bz2.compress(d)

    os.chdir('..')

    return {'ftype': 'application/x-bzip-compressed-tar',
            'data' : c}

def general():
    s = [x for x in open('/home/merlijn/sm/list.xml')]

    return {'ftype': 'text/xml;charset=utf8', 'data' : ''.join(s)}

if __name__ == '__main__':

    wt = WebTool()

    wt.add_rule(re.compile('^%s/scripts/([0-9,A-z,_]+)\.tar\.bz2$' % BASE_URL),
        tarball, ['name'])

    wt.add_rule(re.compile('^%s/?$' % BASE_URL),
                general, [])

    WSGIServer(sm).run()
