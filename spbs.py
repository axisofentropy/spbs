from random import shuffle, choice
from csv import DictWriter

names = [
 'Adam',
 'Bob',
 'Charlie',
 'Dave',
 'Einstein',
 'George',
 'Herbert',
 'Ingrid',
 'Jill',
 'Kate',
 'Louis',
 'Mallory',
 'Nancy',
]
print 'These applicants will bid for shifts:', ', '.join(names)
print ''

shifts = [
 x+1 for x in range(len(names))
]
print 'These shifts are available:', shifts
print ''

# for later output.
output_fieldnames = ['name',] + list(shifts)
#output_names = list(names)

roster = {
  shift : None for shift in shifts
}

bids = {}
for name in names:
 bids[name] = list(shifts)
 shuffle(bids[name])
 print name, 'bids for', bids[name]

def assign (name, shift, bid_index):
 roster[shift] = name
 #bids[name][bid_index] = 10000 + shift
 names.remove(name)
 shifts.remove(shift)
 print "Assigned", name, 'to shift', shift, "in round", bid_index + 1

for i in range(len(shifts)):
 print ''
 print "ROUND", i+1
 for shift in list(shifts):
  bidders = filter(lambda name : bids[name][shift-1] == i + 1, names)
  if bidders:
   print ' and '.join(bidders), "bid on shift", shift
   # randomly assign one member of the list of bidders.
   assign(choice(bidders), shift, i)
  else:
   print "no bids this round for shift", shift

print ''
print 'ROSTER'
for shift in roster.keys():
 print "Shift", shift, '-', roster[shift]

print 'SCORE'
print bids

print 'OUTPUT'
#print fieldnames
with open('/tmp/deleteme.csv', 'w') as csvfile:
 csvwriter = DictWriter(csvfile, fieldnames=output_fieldnames)
 csvwriter.writeheader()
 for name in bids.keys():
  csvwriter.writerow({shift: bid for shift, bid in zip(output_fieldnames,[name,] + bids[name])})
