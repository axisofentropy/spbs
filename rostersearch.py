"""Roster and problem objects, and some search functions"""

try:
    from aima.search import Problem, hill_climbing
except ImportError:
    raise Exception("This needs Python 3.3 or newer.")

from itertools import combinations
from collections import OrderedDict
from random import sample

class Roster(OrderedDict):
    """Map of shifts to names"""

    def shifts(self):
        return self.keys()

    def names(self):
        return self.values()

    def score(self, bids):
        score_total = 0
        for shift in self.shifts():
            score = int(bids[self[shift]][shift]) - 1
            # print "Score", score, "for Shift", shift, '-', roster[shift]
            score_total = score_total - score
        return score_total


class Bids(OrderedDict):
    """Map of names to map of shifts to preference."""

    def list_names(self):
        """List all the names referenced in this set of bids."""
        l = list(self.keys())
        l.sort() # Needs to be deterministic for later randomizing.
        return l

    def list_shifts(self):
        """List all unique shifts referenced in this set of bids."""
        l = list(self[list(self.keys())[0]].keys()) #TODO
        l.sort() # Needs to be deterministic for later randomizing.
        return l

def random_roster(bids):
    """Generate a random complete Roster from a set of bids."""
    return Roster(zip(
        bids.list_shifts(),
        sample(bids.list_names(), k=len(bids.list_names()))
    ))

class RosterProblem(Problem):
    """Definition of our Problem"""

    def __init__(self, initial, bids, badgoals, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""

        self.initial = initial
        self.goal = goal
        self.bids = bids
        self.badgoals = badgoals

        self.names = bids.list_names()
        self.shifts = bids.list_shifts()

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        # Return an iterable yielding all pairings of shifts to swap.
        return combinations(state.shifts(), 2)

    def result(self, state, action): #pylint: disable=no-self-use
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        # Create a new state object so we don't clobber the original.
        output = Roster()
        output.update(state)

        # Swap the values of the two keys in the `action` tuple.
        output[action[0]] = state[action[1]]
        output[action[1]] = state[action[0]]
        return output

    def goal_test(self, state):
        """Determine if this state has reached our problem's goal."""

        # Because this is an optimization problem, we don't have a goal.
        # But if we somehow find a "perfect" roster, we can stop.
        if state.score(self.bids) == 0:
            return True
        else:
            return False

    # path_cost(self, c, state1, action, state2) # method of parent class

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""

        return state.score(self.bids)

def hill_climbing_roster_search(bids):
    """Straightforward search through space of potential rosters"""
    problem = RosterProblem(Roster(), bids, badgoals=[])
    return hill_climbing(problem)

def mountain_range_search(bids):
    """Run simple Hill Climbing search many times, returning the best result"""
    # List of previously discovered goal states.
    ATTEMPTS = 1000
    previous_goals = []
    while len(previous_goals) < ATTEMPTS:
        problem = RosterProblem(random_roster(bids), bids, badgoals=previous_goals)
        previous_goals.append(hill_climbing(problem))
        print(previous_goals[-1].score(bids), end=' ')
        if len(previous_goals) % 12  == 0:
            print("finished run", len(previous_goals), "of", ATTEMPTS)

    high_score = float('-inf')
    best_roster = {}
    problem = RosterProblem(Roster(), bids, badgoals=None)
    for roster in previous_goals:
        this_score = problem.value(roster)
        if this_score > high_score:
            #print("new best")
            best_roster = roster
            high_score = this_score
    return best_roster
