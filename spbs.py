"""Command-line utility to identify a good roster from preferencial bids"""

from __future__ import print_function

from rostersearch import Bids, mountain_range_search

def importcsvbids(csvfilename, bids):
    """Import preferencial bids from a CSV file."""
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

        return fieldnames

# Main loop if called via command-line
if __name__ == "__main__":
    from argparse import ArgumentParser

    argparser = ArgumentParser(
        description='Simple Preferential Bidding System',
        epilog='https://github.com/axisofentropy/spbs/'
    )

    argparser.add_argument(
        "bidcsv",
        help='Filename of input bids in CSV format.'
    )

    args = argparser.parse_args()

    bids = Bids()

    fieldnames = importcsvbids(args.bidcsv, bids)

    #print('These applicants will bid for shifts:', ', '.join(bids.keys()))

    best_rosters = mountain_range_search(bids)

    best_roster = best_rosters[0]

    print('\n')
    print("BEST")
    for roster in best_rosters:
        print(best_rosters.index(roster))
        print(str(roster))
    print('')
    print("SCORE", best_roster.score(bids), "in", len(best_rosters), "rosters")
