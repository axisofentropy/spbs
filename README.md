# Simple Preferential Bidding System (SPBS)

## Overview and Goals
This repository implements a simple solution to the [Nurse Scheduling Problem](https://en.wikipedia.org/wiki/Nurse_scheduling_problem) using spreadsheet input and output.

## Problem Space
Administrators must assign two or more employees to a (usually) equal number of schedules.  The only criteria are employee preferences and validity (every employee is assigned a shift.)  Employees will each indicate how much they value each available schedule.  The most desirable roster assigns all employees their most preferred schedule.

## Design History
When Catherine and I first discussed this, I recognized this as an economic problem:  allocation of scarce resources.  In the real world, the organization was solving this problem with little structure:  Employees in a classroom discussed potential assignments, eventually arriving somewhere near consensus.  This process was time-consuming, sometimes dramatic, and often left someone feeling disenfranchised.  I felt a more formal process could deliver greater overall employee satisfaction in less time.

We identified a specific metric for a roster's desirability.  The best possible roster assigns every employee to the schedule they desire most.  Conversely, the worst roster assigns everyone their least favorite.  We can measure this spectrum by scoring how "close" every employee got to their most preferred shift.  I began with a very simple quantification:  subtracting `1` for each employee choice denied.  An ideal roster, assigning all employees to their first-choice shift, has a score of `0`.  If one employee gets their second-choice shift, that subtracts `1`.  If three employees got their fourth choices, the total roster score would be `-9`.

The first, most straightforward process first asked each employee to rank every available schedule in order of preference.  Then, an administrator could first consider all shifts receiving first-choice bids.  If any received only one first-choice, award that shift to the most desiring employee, removing him or her from future consideration.  If more than one first-choice is received for a shift, then randomly allocate the winner.  After considering all first-choices, move on to the second-choices and repeat.  We implemented this first with pencil and paper, and then I implemented a proof-of-concept visible in this repository's initial commit.

Stakeholders considered this process an improvement over free-form discussion.  Employees understood and accepted the algorithm as fair, impartial, and often produced "good" schedules.  Yet I believed a more sophisticated algorithm would more often deliver the best-possible roster.

The next obvious step beyond pencil and paper is enumerating and scoring all possible rosters.  My laptop did this in seconds for rosters of one to seven employees, but couldn't calculate larger roster sets fast enough.  This needed a more effective search strategy, so I dug up my college [Artificial Intelligence textbook](https://en.wikipedia.org/wiki/Artificial_Intelligence:_A_Modern_Approach).  Read Chapter 4.3, "Local Search Algorithms and Optimization Problems".

# Implementation

## Dependencies
Python 3.something, probably 3.3

## Usage
Initially, this implementation works best with Google Sheets and Forms.  We suggest creating a Form asking employees to rank their preferences for all available schedules in order from 1 (first choice) to N (last choice) where N is the number of available schedules.  This should result in a spreadsheet like this:
https://docs.google.com/spreadsheets/d/1WKzURDT-1bu0_G5PuhxL-fe-Ud3BvWr2yJQd-mYAruw/edit?usp=sharing

Download that spreadsheet as "Comma-seperated values (.csv)".  Store it somewhere accessible to the executable.

`python spbs.py "./downloaded.csv"`

You may also use an anonymized example in this repository:

`python spbs.py "./example.csv"`

## Roadmap
Of course, tighter integration with Google Sheets would make this process much easier.  Deploying an executable to Windows and Mac desktops or somewhere online would also help a lot.
