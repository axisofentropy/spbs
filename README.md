# Simple Preferential Bidding System (SPBS)

## Overview and Goals
This repository implements a simple solution to the [Nurse Scheduling Problem](https://en.wikipedia.org/wiki/Nurse_scheduling_problem) using spreadsheet input and output.

## Problem Space
Administrators must assign two or more employees to a (usually) equal number of schedules.  The only criteria are employee preferences.  The most desirable roster assigns all employees their most preferred schedule.

## Dependencies
Python 3.something

## Usage
Initially, this implementation works best with Google Sheets and Forms.  We suggest creating a Form asking employees to rank their preferences for all available schedules in order from 1 (first choice) to N (last choice) where N is the number of available schedules.  This should result in a spreadsheet like this:
https://docs.google.com/spreadsheets/d/1WKzURDT-1bu0_G5PuhxL-fe-Ud3BvWr2yJQd-mYAruw/edit?usp=sharing

Download that spreadsheet as "Comma-seperated values (.csv)".  Store it somewhere accessible to the executable.

`python spbs.py "./downloaded.csv"`

## Roadmap
Of course, tighter integration with Google Sheets would make this process much easier.  Deploying an executable to Windows and Mac desktops or somewhere online would also help a lot.
