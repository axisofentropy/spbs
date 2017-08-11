import pytest

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

def test_rosterproblem_init():

    initial = Roster()
    initial['shift1'] = 'name2'
    initial['shift2'] = 'name3'
    initial['shift3'] = 'name1'

    goal = Roster()
    goal['shift1'] = 'name1'
    goal['shift2'] = 'name2'
    goal['shift3'] = 'name3'

    bids = {
        'name1': {
            'shift1': '1',
            'shift2': '2',
            'shift3': '3',
        },
        'name2': {
            'shift1': '3',
            'shift2': '1',
            'shift3': '2',
        },
        'name3': {
            'shift1': '2',
            'shift2': '3',
            'shift3': '1',
        },
    }

    rp = RosterProblem(initial, bids, None, goal)

    assert rp.initial == initial
    assert rp.goal == goal
    assert rp.bids == bids

    # Derived values
    
    assert len(rp.shifts) == 3
    assert list(rp.shifts).count('shift1') == 1
    assert list(rp.shifts).count('shift2') == 1
    assert list(rp.shifts).count('shift3') == 1

    assert len(rp.names) == 3
    assert list(rp.names).count('name1') == 1
    assert list(rp.names).count('name2') == 1
    assert list(rp.names).count('name3') == 1
