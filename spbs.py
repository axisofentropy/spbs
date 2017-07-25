from __future__ import print_function

from random import shuffle, choice
from itertools import product, permutations
from math import factorial

from rostersearch import mountain_range_search

names = [
]

shifts = [
]

def importcsvbids(csvfilename, bids):
 from csv import DictReader
 with open(csvfilename) as csvfile:
  csvreader = DictReader(csvfile)
  fieldnames = list(csvreader.fieldnames) # copy

  for row in csvreader:
   # Remove first field leaving just the bid numbers.
   name = row[csvreader.fieldnames[0]]
   row.pop(csvreader.fieldnames[0])

   # Add this person's bids.
   bids[name] = row
   print(name, 'bids for', bids[name])

  return fieldnames

def score(roster):
 score_total = 0
 for shift in roster.keys():
  score = int(bids[roster[shift]][shift]) - 1
  score_total = score_total - score
 return score_total

def assign (name, shift, bid_index):
 roster[shift] = name
 #bids[name][shift] = 10000 + bid_index + 1
 names.remove(name)
 shifts.remove(shift)
 #print "Assigned", name, 'to shift', shift, "in round", bid_index + 1

def exhaustive_search(bids, shifts):
 best_score = -100
 best_roster = {}
 roster_length = len(shifts)
 if roster_length is not len(bids.keys()):
  raise Exception('not square bids.')

 search_len = factorial(roster_length) * factorial(roster_length)
 print("Search through", search_len, "possibilities.")

 iii = 0
 for roster in product(permutations(shifts, roster_length), permutations(bids.keys(), roster_length)):
  iii = iii + 1
  percent = 100 * float(iii) / float(search_len)
  if not percent % 1:
   print(percent, "%  generated", iii, "of", search_len)

  roster = zip(roster[0],roster[1])
  roster = dict(roster)
  this_score = score(roster)
  if this_score > best_score:
   best_score = this_score
   print("found", this_score, roster)
   best_roster = roster

 return best_roster

def exportcsvbids(csvfilename='/tmp/deleteme.csv', bids={}, fieldnames=[]):
 from csv import DictWriter
 with open(csvfilename, 'w') as csvfile:
  csvwriter = DictWriter(csvfile, fieldnames=fieldnames)
  csvwriter.writeheader()
  for name in bids.keys():
   output_row = {fieldnames[0]: name}
   output_row.update(bids[name])
   csvwriter.writerow(output_row)
   #csvwriter.writerow({shift: bid for shift, bid in zip(output_fieldnames,[name,] + bids[name])})

# Main loop if called via command-line
if __name__ == "__main__":
 from argparse import ArgumentParser

 argparser = ArgumentParser(
  description='Simple Preferential Bidding System',
  epilog='https://github.com/axisofentropy/spbs/'
 )

 argparser.add_argument("bidcsv",
  help='Filename of input bids in CSV format.'
 )

 args = argparser.parse_args()

 bids = {}

 fieldnames = importcsvbids(args.bidcsv, bids)

 print('These applicants will bid for shifts:', ', '.join(bids.keys()))

 shifts = bids[list(bids.keys())[0]] # risky

 #best_roster = hill_climbing_roster_search(bids, shifts)
 best_roster = mountain_range_search(bids, shifts)

 print("BEST", best_roster)
 print("SCORE", score(best_roster))

 exportcsvbids(bids=bids, fieldnames=fieldnames)
