#!/usr/bin/env python

import os
from AR import AccuRev, ARWorkspace, ARException

STREAMS_FILE = r'D:\Test\streams.txt'
ACCUREV_WS_PATH = r'D:\Test'
ACCUREV_WS_PATTERN = 'dev.ws.OpenGrok_'
ACCUREV_USER= 'buildmgr'
ACCUREV_PWD = '$1330BLD!'

ar = AccuRev()
ar.login(ACCUREV_USER, ACCUREV_PWD)

with open(STREAMS_FILE, 'r') as streams_file:
    streams = [s.rstrip() for s in streams_file.readlines()]

for stream in streams:
    print "*"*10 + stream + "*"*10
    try:
        ws = ARWorkspace(ACCUREV_WS_PATTERN + stream)
        ws.update()
    except ARException:
        ws = ARWorkspace()
        ws.name = ACCUREV_WS_PATTERN + stream
        ws.location = os.path.join(ACCUREV_WS_PATH, ACCUREV_WS_PATTERN + stream)
        ws.stream = stream
        ws.create()
        ws = ARWorkspace(ACCUREV_WS_PATTERN + stream)
        ws.update()