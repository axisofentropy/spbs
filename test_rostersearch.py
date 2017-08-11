import pytest
import random

from rostersearch import *

@pytest.fixture
def simple_initial():
    initial = Roster()
    initial['shift1'] = 'name2'
    initial['shift2'] = 'name3'
    initial['shift3'] = 'name1'
    return initial

@pytest.fixture
def simple_goal():
    goal = Roster()
    goal['shift1'] = 'name1'
    goal['shift2'] = 'name2'
    goal['shift3'] = 'name3'
    return goal

@pytest.fixture
def simple_bids():
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
    return bids

@pytest.fixture
def simple_roster_problem(simple_initial, simple_bids, simple_goal):
    return RosterProblem(simple_initial, simple_bids, simple_goal)

def test_roster(simple_bids):
    r = Roster({
        'shift1': 'name2',
        'shift2': 'name3',
        'shift3': 'name1',
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

    # Test scoring too why not.

    assert r.score(simple_bids) == -6

def test_roster_score(simple_bids, simple_initial, simple_goal):
    assert simple_goal.score(simple_bids) == 0 # Zero is ideal.

    # Let's compare some Rosters and enforce which is better.

    # An ideal roster is better than the worst possible roster.
    assert simple_goal.score(simple_bids) > simple_initial.score(simple_bids)

    r22 = Roster({
        'shift1': 'name3', # second choice
        'shift2': 'name1', # second choice
    })

    r13 = Roster({
        'shift1': 'name1', # first choice
        'shift2': 'name3', # third choice
    })

    r12 = Roster({
        'shift3': 'name3', # first choice
        'shift2': 'name1', # second choice
    })

    # A first and second choice are better than two seconds.
    assert r12.score(simple_bids) > r22.score(simple_bids)

    # And better than a first and third, of course.
    assert r12.score(simple_bids) > r13.score(simple_bids)

    # Two second choices is better than a first and third!
    #TODO#assert r22.score(simple_bids) > r13.score(simple_bids)

def test_roster_comparison():
    """Confirm that two "identical" Rosters compare as such."""

    r1 = Roster()
    r1['shift1'] = 'name1'
    r1['shift2'] = 'name2'
    r1['shift3'] = 'name3'

    r2 = Roster() # reverse order
    r2['shift3'] = 'name3'
    r2['shift2'] = 'name2'
    r2['shift1'] = 'name1'

    assert r1 == r2

    # Random shuffle just to be sure!
    r3 = Roster(random.sample(r1.items(), len(r1)))
    r4 = Roster(random.sample(r2.items(), len(r2)))

    assert r3 == r4

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

    # Test .list_names method.
    assert len(bids.list_names()) == 3
    assert bids.list_names().count('name1') == 1
    assert bids.list_names().count('name2') == 1
    assert bids.list_names().count('name3') == 1

    # Test .list_shifts method.
    assert len(bids.list_shifts()) == 3
    assert bids.list_shifts().count('shift1') == 1
    assert bids.list_shifts().count('shift2') == 1
    assert bids.list_shifts().count('shift3') == 1

    # The output of these methods should also be sorted, for use in random samples.
    assert bids.list_names() == ['name1', 'name2', 'name3']
    assert bids.list_shifts() == ['shift1', 'shift2', 'shift3']

def test_random_roster(simple_bids):

    random.seed(23) # This should make results predictable.

    roster1 = random_roster(simple_bids)
    assert roster1['shift1'] == 'name2'
    assert roster1['shift2'] == 'name1'
    assert roster1['shift3'] == 'name3'

    roster2 = random_roster(simple_bids)
    assert roster2['shift1'] == 'name3'
    assert roster2['shift2'] == 'name2'
    assert roster2['shift3'] == 'name1'

    roster3 = random_roster(simple_bids)
    assert roster3['shift1'] == 'name2'
    assert roster3['shift2'] == 'name3'
    assert roster3['shift3'] == 'name1'

    # Can we score these too?  Why not!
    assert roster1.score(simple_bids) == -3
    assert roster2.score(simple_bids) == -3
    assert roster3.score(simple_bids) == -6

class TestRosterProblem(object):
    def test_init(self, simple_initial, simple_goal, simple_bids):

        rp = RosterProblem(simple_initial, simple_bids, simple_goal)

        assert rp.initial == simple_initial
        assert rp.goal == simple_goal
        assert rp.bids == simple_bids

        # Derived values

        assert len(rp.shifts) == 3
        assert list(rp.shifts).count('shift1') == 1
        assert list(rp.shifts).count('shift2') == 1
        assert list(rp.shifts).count('shift3') == 1

        assert rp.shifts == simple_bids.list_shifts()

        assert len(rp.names) == 3
        assert list(rp.names).count('name1') == 1
        assert list(rp.names).count('name2') == 1
        assert list(rp.names).count('name3') == 1

        assert rp.names == simple_bids.list_names()

    def test_value(self, simple_roster_problem, simple_initial, simple_goal):
        rp = simple_roster_problem

        # Try on its own internal initial state first.
        assert rp.value(rp.initial) == rp.initial.score(rp.bids)

        assert rp.value(simple_initial) == simple_initial.score(rp.bids)
        assert rp.value(simple_goal) == simple_goal.score(rp.bids)

    def test_goal_test(self, simple_roster_problem, simple_initial, simple_goal):
        rp = simple_roster_problem

        assert rp.goal_test(simple_initial) == False
        assert rp.goal_test(simple_goal) == True

    def test_actions(self, simple_roster_problem):
        expected_actions = [
            ('shift1', 'shift2'), # Swap first and second.
            ('shift1', 'shift3'), # Swap first and third.
            ('shift2', 'shift3'), # Swap second and third.
        ]

        rp = simple_roster_problem

        # Cast iterable as list for comparison.
        assert list(rp.actions(rp.initial)) == expected_actions

    def test_result(self, simple_roster_problem):
        rp = simple_roster_problem

        action = ('shift1', 'shift3') # Swap first and third shifts.

        expected_roster = Roster({
            'shift1': 'name1',
            'shift2': 'name3',
            'shift3': 'name2',
        })

        resultant_roster = rp.result(rp.initial, action)

        for key in expected_roster.keys():
            assert resultant_roster[key] == expected_roster[key]
