#!/usr/bin/env python
import re
import json
import argparse
import ipaddress
from typing import Dict, List, TypedDict


# if you want to use different file as hosts, update hostsfile
hostsfile: str = '/etc/hosts'


class Inventories(TypedDict):
    _meta: Dict[str, Dict[str, str]]
    targets: Dict[str, List[str]]


def _getargs() -> argparse.Namespace:
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


def makeInventory(f: str) -> Inventories:
    inventories: Inventories = {
        '_meta':   {'hostvars': {}},
        'targets':     {'hosts': []}
    }

    with open(f, 'r') as filepath:
        hosts: List[str] = filepath.readlines()

    hostlines: List[str] = [host.strip() for host in hosts
                            if not host.startswith('#') and host.strip() != '']

    for i in hostlines:
        splitted: List[str] = re.split(' +|	+', i)
        if len(splitted) < 2:
            continue
        if splitted[1] == '':
            continue
        try:
            ip: ipaddress.IPv4Address = ipaddress.ip_address(splitted[0])
        except ValueError:
            continue
        hostname: str = splitted[1]
        if ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            continue
        if str(ip) == '255.255.255.255':
            continue
        if hostname in inventories['targets']['hosts']:
            continue

        inventories['targets']['hosts'].append(hostname)
    return inventories


if __name__ == "__main__":
    args: argparse.Namespace = _getargs()
    print(json.dumps(makeInventory(args.f), indent=4))
