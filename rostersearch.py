from search import Problem, hill_climbing
from itertools import product, permutations

class Roster(dict):
 def shifts(self):
  return self.keys()

 def names(self):
  return self.values()

class RosterProblem(Problem):
 def __init__(self, initial, bids, goal=None):
  """The constructor specifies the initial state, and possibly a goal
  state, if there is a unique goal.  Your subclass's constructor can add
  other arguments."""
  self.initial = initial
  self.goal = goal
  self.bids = bids
  self.names = bids.keys()
  self.shifts = bids[list(bids.keys())[0]] #risky

 def actions(self, state):
  """Return the actions that can be executed in the given
  state. The result would typically be a list, but if there are
  many actions, consider yielding them one at a time in an
  iterator, rather than building them all at once."""
  available_names = list(filter(lambda x: x not in state.names(), self.names))
  available_shifts = list(filter(lambda x: x not in state.shifts(), self.shifts))
  print(list(product(available_shifts, available_names)))
  return product(available_shifts, available_names)

 def result(self, state, action):
  """Return the state that results from executing the given
  action in the given state. The action must be one of
  self.actions(state)."""
  output = Roster()
  output.update(state)
  output[action[0]] = action[1]
  print(output)
  return output

 def goal_test(self, state):
  return len(state.names) == len(self.names)

 # path_cost(self, c, state1, action, state2)

 def value(self, state):
  """For optimization problems, each state has a value.  Hill-climbing
  and related algorithms try to maximize this value."""
  score_total = 0 - (1000 * len(self.names))
  for shift in state.keys():
   score = int(self.bids[state[shift]][shift]) - 1
   # print "Score", score, "for Shift", shift, '-', roster[shift]
   score_total = score_total - score + 1000
  print(score_total, state)
  return score_total

def hill_climbing_roster_search(bids, shifts):
 problem = RosterProblem(Roster(), bids)
 return hill_climbing(problem) 
