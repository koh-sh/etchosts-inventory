from hosts import makeInventory


inventory = makeInventory('tests/testhosts')


def test_omitlocal():
    assert 'localhost' not in inventory['targets']['hosts']


def test_omitbroadcasts():
    assert 'broadcasthost' not in inventory['targets']['hosts']
    assert 'ip6-allnodes' not in inventory['targets']['hosts']


def test_basic():
    for num in range(1, 4):
        assert 'basic' + str(num) in inventory['targets']['hosts']
    assert inventory['_meta']['hostvars']['basic1']['ansible_hostname'] == '192.168.0.1'
    assert inventory['_meta']['hostvars']['basic2']['ansible_hostname'] == '192.168.0.2'
    assert inventory['_meta']['hostvars']['basic3']['ansible_hostname'] == '192.168.0.3'


def test_tabs():
    assert 'tab1' in inventory['targets']['hosts']
    assert inventory['_meta']['hostvars']['tab1']['ansible_hostname'] == '192.168.0.4'


def test_multispace():
    for num in range(1, 3):
        assert 'multispace' + str(num) in inventory['targets']['hosts']
        assert 'multitabs' + str(num) in inventory['targets']['hosts']
    assert inventory['_meta']['hostvars']['multispace1']['ansible_hostname'] == '192.168.0.5'
    assert inventory['_meta']['hostvars']['multispace2']['ansible_hostname'] == '192.168.0.6'
    assert inventory['_meta']['hostvars']['multitabs1']['ansible_hostname'] == '192.168.0.7'
    assert inventory['_meta']['hostvars']['multitabs2']['ansible_hostname'] == '192.168.0.8'


def test_multihosts():
    assert 'multihost1' in inventory['targets']['hosts']
    assert inventory['_meta']['hostvars']['multihost1']['ansible_hostname'] == '192.168.0.9'
    for num in range(2, 4):
        assert 'multihost' + str(num) not in inventory['targets']['hosts']


def test_dup():
    assert 'dup1' in inventory['targets']['hosts']
    assert inventory['_meta']['hostvars']['dup1']['ansible_hostname'] == '192.168.0.10'
