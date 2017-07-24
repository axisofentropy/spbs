from random import shuffle, choice
from csv import DictReader, DictWriter

names = [
]

shifts = [
]

bids = {}

with open('input.csv') as csvfile:
 csvreader = DictReader(csvfile)

 shifts = csvreader.fieldnames[1:]
 print 'These shifts are available:', shifts
 print ''

 for row in csvreader:
  name = row[csvreader.fieldnames[0]]
  names.append(name)
  row.pop(csvreader.fieldnames[0])
  bids[name] = row
  print name, 'bids for', bids[name]

print 'These applicants will bid for shifts:', ', '.join(names)
print ''


# for later output.
output_fieldnames = ['name',] + list(shifts)
#output_names = list(names)

roster = {
  shift : None for shift in shifts
}

def assign (name, shift, bid_index):
 roster[shift] = name
 #bids[name][shift] = 10000 + bid_index + 1
 names.remove(name)
 shifts.remove(shift)
 print "Assigned", name, 'to shift', shift, "in round", bid_index + 1

for i in range(len(shifts)):
 print ''
 print "ROUND", i+1
 for shift in list(shifts):
  bidders = filter(lambda name : bids[name][shift] == str(i + 1), names)
  if bidders:
   print ' and '.join(bidders), "bid on shift", shift
   # randomly assign one member of the list of bidders.
   assign(choice(bidders), shift, i)
  else:
   print "no bids this round for shift", shift

print ''
print 'ROSTER SCORE'
score_total = 0
for shift in roster.keys():
 score = int(bids[roster[shift]][shift]) - 1
 print "Score", score, "for Shift", shift, '-', roster[shift]
 score_total = score_total - score

print "Roster score:", score_total

print 'OUTPUT'
#print fieldnames
with open('/tmp/deleteme.csv', 'w') as csvfile:
 csvwriter = DictWriter(csvfile, fieldnames=csvreader.fieldnames)
 csvwriter.writeheader()
 for name in bids.keys():
  output_row = {csvreader.fieldnames[0]: name}
  output_row.update(bids[name])
  csvwriter.writerow(output_row)
  #csvwriter.writerow({shift: bid for shift, bid in zip(output_fieldnames,[name,] + bids[name])})
