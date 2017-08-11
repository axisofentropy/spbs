import pytest
import random

from rostersearch import *

def test_roster():
    r = Roster({
        'shift1': 'name1',
        'shift2': 'name2',
        'shift3': 'name3',
    })

    # The .shifts() method should return iterables
    # whose members match what we put in. 

    assert len(r.shifts()) == 3
    assert list(r.shifts()).count('shift1') == 1
    assert list(r.shifts()).count('shift2') == 1
    assert list(r.shifts()).count('shift3') == 1

    assert len(r.names()) == 3
    assert list(r.names()).count('name1') == 1
    assert list(r.names()).count('name2') == 1
    assert list(r.names()).count('name3') == 1

def test_bids():
    bids = Bids({ #shuffled
        'name2': {
            'shift2': '1',
            'shift3': '2',
            'shift1': '3',
        },
        'name3': {
            'shift2': '3',
            'shift3': '1',
            'shift1': '2',
        },
        'name1': {
            'shift2': '2',
            'shift3': '3',
            'shift1': '1',
        },
    })

    assert len(bids.list_names()) == 3
    assert bids.list_names().count('name1') == 1
    assert bids.list_names().count('name2') == 1
    assert bids.list_names().count('name3') == 1

    assert len(bids.list_shifts()) == 3
    assert bids.list_shifts().count('shift1') == 1
    assert bids.list_shifts().count('shift2') == 1
    assert bids.list_shifts().count('shift3') == 1

    # The output of these methods should also be sorted, for use in random samples.
    assert bids.list_names() == ['name1', 'name2', 'name3']
    assert bids.list_shifts() == ['shift1', 'shift2', 'shift3']

def test_random_roster():
    bids = Bids({ #shuffled
        'name2': {
            'shift2': '1',
            'shift3': '2',
            'shift1': '3',
        },
        'name3': {
            'shift2': '3',
            'shift3': '1',
            'shift1': '2',
        },
        'name1': {
            'shift2': '2',
            'shift3': '3',
            'shift1': '1',
        },
    })

    random.seed(23) # This should make results predictable.

    roster1 = random_roster(bids)
    assert roster1['shift1'] == 'name2'
    assert roster1['shift2'] == 'name1'
    assert roster1['shift3'] == 'name3'

    roster2 = random_roster(bids)
    assert roster2['shift1'] == 'name3'
    assert roster2['shift2'] == 'name2'
    assert roster2['shift3'] == 'name1'
    
    roster3 = random_roster(bids)
    assert roster3['shift1'] == 'name2'
    assert roster3['shift2'] == 'name3'
    assert roster3['shift3'] == 'name1'

def test_rosterproblem_init():

    initial = Roster()
    initial['shift1'] = 'name2'
    initial['shift2'] = 'name3'
    initial['shift3'] = 'name1'

    goal = Roster()
    goal['shift1'] = 'name1'
    goal['shift2'] = 'name2'
    goal['shift3'] = 'name3'

    bids = Bids({ #shuffled
        'name2': {
            'shift2': '1',
            'shift3': '2',
            'shift1': '3',
        },
        'name3': {
            'shift2': '3',
            'shift3': '1',
            'shift1': '2',
        },
        'name1': {
            'shift2': '2',
            'shift3': '3',
            'shift1': '1',
        },
    })

    rp = RosterProblem(initial, bids, None, goal)

    assert rp.initial == initial
    assert rp.goal == goal
    assert rp.bids == bids

    # Derived values
    
    assert len(rp.shifts) == 3
    assert list(rp.shifts).count('shift1') == 1
    assert list(rp.shifts).count('shift2') == 1
    assert list(rp.shifts).count('shift3') == 1

    assert rp.shifts == bids.list_shifts()

    assert len(rp.names) == 3
    assert list(rp.names).count('name1') == 1
    assert list(rp.names).count('name2') == 1
    assert list(rp.names).count('name3') == 1

    assert rp.names == bids.list_names()
