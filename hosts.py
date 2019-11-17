#!/usr/bin/env python
import os
import re
import json
import argparse


# if you want to use different file as hosts, update hostsfile
hostsfile = '/etc/hosts'


def _getargs():
    parser = argparse.ArgumentParser(
        description='Parse /etc/hosts for Ansible Inventory')
    parser.add_argument('--list',
                        help='Option for Ansible execution.',
                        action='store_true',
                        default=False)
    parser.add_argument('-f',
                        help='Specify different hosts [for debug purpose]',
                        default=hostsfile)
    args = parser.parse_args()
    return args


def makeInventory(f):
    inventories = {
        '_meta':   {'hostvars': {}},
        'targets':     {'hosts': []}
    }

    with open(f, 'r') as f:
        hosts = f.readlines()

    hostlines = [host.strip() for host in hosts
                 if not host.startswith('#') and host.strip() != '']

    hostlist = []  # This is to omit duplicated entry

    for i in hostlines:
        splitted = re.split(' +|	+', i)
        if len(splitted) < 2:
            continue
        if splitted[1] == '':
            continue
        ip = splitted[0]
        hostname = splitted[1]
        if ip.startswith('127') or ip == '::1':
            continue
        if ip.startswith('ff') or ip == '255.255.255.255':
            continue
        if hostname in hostlist:
            continue

        inventories['targets']['hosts'].append(hostname)
        inventories['_meta']['hostvars'][hostname] = {
            'ansible_hostname': ip
        }
        hostlist.append(hostname)
    return inventories


if __name__ == "__main__":
    args = _getargs()
    print(json.dumps(makeInventory(args.f), indent=4))
