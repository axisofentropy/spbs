"""Command-line utility to identify a good roster from preferencial bids"""

from __future__ import print_function

from rostersearch import mountain_range_search

names = [
]

shifts = [
]

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
            print(name, 'bids for', bids[name])

        return fieldnames

def score(roster):
    """Return relative value of a potential roster."""
    score_total = 0
    for shift in roster.keys():
        score = int(bids[roster[shift]][shift]) - 1
        score_total = score_total - score
    return score_total

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

    bids = {}

    fieldnames = importcsvbids(args.bidcsv, bids)

    print('These applicants will bid for shifts:', ', '.join(bids.keys()))

    best_roster = mountain_range_search(bids)

    print("BEST", best_roster)
    print("SCORE", score(best_roster))
