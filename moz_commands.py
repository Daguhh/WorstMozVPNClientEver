#!!/usr/bin/env python3

"""
mozillavpn command wrapper
"""

import subprocess
import re

moz_help="mozillavpn -h"
moz_version="mozillavpn -v"
moz_status = "mozillavpn status"
moz_activate = "mozillavpn activate &"
moz_deactivate = "mozillavpn deactivate &"
moz_device = "mozillavpn device"
moz_login = "mozillavpn login"
moz_logout = "mozillavpn logout"
moz_select = "mozillavpn select"
moz_servers = "mozillavpn servers"
moz_ui = "mozillavpn ui"
moz_linuxdaemon = "mozillavpn linuxdaemon"

def help():
    print(subprocess.check_output(moz_help, shell=True))

def version():
    print(subprocess.check_output(moz_version, shell=True))

def status():
    output = subprocess.check_output(moz_status, shell=True).decode()

    items = re.split('\n(?!\s*-)', output)

    all_props = dict(re.split(':\s*', x,1) for x in [s for s in items if not re.match('^Device', s)] if x)
    all_props['Devices'] = '\n\n'.join([s for s in items if re.match('^Device', s)])

    return all_props

def activate():
    subprocess.check_output(moz_activate, shell=True)

def deactivate():
    subprocess.check_output(moz_deactivate, shell=True)

def device():
    pass

def login():
    pass

def logout():
    pass

def select(server):
    subprocess.check_output(' '.join([moz_select, server]), shell=True)

SERVERS = {}

for item in subprocess.check_output('mozillavpn servers', shell=True).decode().split('\n'):

    if "Country:" in item:
        country = item.split(':',1)[-1].strip()
        SERVERS[country] = {}

    if "City:" in item:
        city = item.split(':',1)[-1].strip()
        SERVERS[country][city] = []

    if "Server" in item:
        server = item.split(':',1)[-1].strip()
        SERVERS[country][city] += [server]

def servers():

    return SERVERS

def ui():
    pass

def linuxdaemon():
    pass




