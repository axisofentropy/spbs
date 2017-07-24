from random import shuffle, choice

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

roster = {
  shift : None for shift in shifts
}

bids = {}
for name in names:
 bids[name] = list(shifts)
 shuffle(bids[name])
 print name, 'bids for', bids[name]

def assign (name, shift):
 roster[shift] = name
 names.remove(name)
 shifts.remove(shift)
 print "Assigned", name, 'to shift', shift

for i in range(len(shifts)):
 print ''
 print "ROUND", i+1
 for shift in list(shifts):
  bidders = filter(lambda name : bids[name][i] == shift, names)
  if bidders:
   print ' and '.join(bidders), "bid on shift", shift
   assign(choice(bidders), shift)
  else:
   print "no bids this round for shift", shift

print ''
print 'ROSTER'
for shift in roster.keys():
 print "Shift", shift, '-', roster[shift]
