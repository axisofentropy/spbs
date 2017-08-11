"""Roster and problem objects, and some search functions"""

try:
    from aima.search import Problem, hill_climbing
except ImportError:
    raise Exception("This needs Python 3.3 or newer.")

from itertools import product
from collections import OrderedDict

class Roster(OrderedDict):
    """Map of shifts to names"""

    def shifts(self):
        return self.keys()

    def names(self):
        return self.values()

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
        self.names = bids.keys()
        self.shifts = bids[list(bids.keys())[0]] #risky

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""

        available_names = list(
            filter(lambda x: x not in state.names(), self.names)
        )

        available_shifts = list(
            filter(lambda x: x not in state.shifts(), self.shifts)
        )

        return product(available_shifts, available_names)

    def result(self, state, action): #pylint: disable=no-self-use
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        output = Roster()
        output.update(state)
        output[action[0]] = action[1]
        #print(output)
        return output

    def goal_test(self, state):
        """Determine if this state has reached our problem's goal."""
        if state in self.badgoals:
            return False
        return len(state.names) == len(self.names)

    # path_cost(self, c, state1, action, state2) # method of parent class

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        score_total = 0 - (1000 * len(self.names))
        for shift in state.keys():
            score = int(self.bids[state[shift]][shift]) - 1
            # print "Score", score, "for Shift", shift, '-', roster[shift]
            score_total = score_total - score + 1000
        #print("SCORE", score_total, state)
        return score_total

def hill_climbing_roster_search(bids):
    """Straightforward search through space of potential rosters"""
    problem = RosterProblem(Roster(), bids, badgoals=[])
    return hill_climbing(problem)

def mountain_range_search(bids):
    """Run simple Hill Climbing search many times, returning the best result"""
    # List of previously discovered goal states.
    attempts = 10000
    previous_goals = []
    while len(previous_goals) < attempts:
        problem = RosterProblem(Roster(), bids, badgoals=previous_goals)
        previous_goals.append(hill_climbing(problem))
        print("finished run", len(previous_goals), "of", attempts)

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
