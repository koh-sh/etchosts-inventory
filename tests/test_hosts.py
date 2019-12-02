from hosts import makeInventory


inventory = makeInventory('tests/testhosts')


def test_omitlocal():
    assert 'localhost' not in inventory['targets']['hosts']


def test_omitreserved():
    assert 'broadcasthost' not in inventory['targets']['hosts']
    assert 'ip6-allnodes' not in inventory['targets']['hosts']
    assert 'ip6-localnet' not in inventory['targets']['hosts']


def test_basic():
    for num in range(1, 4):
        assert 'basic' + str(num) in inventory['targets']['hosts']


def test_tabs():
    assert 'tab1' in inventory['targets']['hosts']


def test_multispace():
    for num in range(1, 3):
        assert 'multispace' + str(num) in inventory['targets']['hosts']
        assert 'multitabs' + str(num) in inventory['targets']['hosts']


def test_multihosts():
    assert 'multihost1' in inventory['targets']['hosts']
    for num in range(2, 4):
        assert 'multihost' + str(num) not in inventory['targets']['hosts']

