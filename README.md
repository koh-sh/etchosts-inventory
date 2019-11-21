# etchosts-inventory
![](https://github.com/koh-sh/etchosts-inventory/workflows/.github/workflows/test.yml/badge.svg)

Python script to parse /etc/hosts for Ansible Inventory  
*python2.x is not supported

## Overview

This sctipt collects all hosts from /etc/hosts into `targets` group and set its ip address as `ansible_hostname`

```bash
$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.1.1 web1
192.168.1.2 web2
$ ansible-inventory -i etchosts-inventory/hosts.py --list
{
    "_meta": {
        "hostvars": {
            "web1": {
                "ansible_hostname": "192.168.1.1"
            },
            "web2": {
                "ansible_hostname": "192.168.1.2"
            }
        }
    },
    "all": {
        "children": [
            "targets",
            "ungrouped"
        ]
    },
    "targets": {
        "hosts": [
            "web1",
            "web2"
        ]
    }
}
$
```

## How to use

1. Clone

```bash
$ git clone https://github.com/koh-sh/etchosts-inventory.git
```

2. Config for Ansible

Set this sctipt as inventory with ansible.cfg or environment variable or command line option.

- ansible.cfg

```bash
$ cat ansible.cfg
[defaults]
inventory = /path/to/etchosts-inventory/hosts.py
$
```

- environment variable

```bash
$ export ANSIBLE_INVENTORY=/path/to/etchosts-inventory/hosts.py
```

- command line option

```bash
$ ansible-playbook -i /path/to/etchosts-inventory/hosts.py PLAYBOOK
```
