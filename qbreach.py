#!/usr/bin/env python
# qbreach.py
#
# A tool designed to query the kill logs and player list data available from http://thebreach.ca
#
# author : dan witkowski

import argparse
from lxml import html
import requests
import datetime
import re

# Global variables
in_file = ""
names = []
t_min = 0
max_count = 0


# Determines whether the killer or killed are at least a partial match to one of the names provided
def in_names(name):
    interest = False
    
    if args.s:
        # Iterate over our list to look for matches, including partial matches
        for n in names:
            p = re.compile(".*" + n + ".*", re.IGNORECASE)
            if p.match(name):
                interest = True
                break
            
    else:
        if name in names:
            interest = True
    
    return interest

def query_player_list():
    # Get page
    page = requests.get('http://thebreach.ca/player-list/')
    
    # Parse into a structured tree
    tree = html.fromstring(page.text)
    
    # Query just the table rows with player list data
    rows = tree.xpath('//div[@class="entry themeform"]/div/table//tr')
    
    print "\n--- Players Online ---\n"
    
    # Iterate over the rows of the kill log table
    for row in rows:
            
            # Returns a list containing each table data element for the table row	
            children = row.getchildren()
            
            # There should be 4 children but for some reason sometimes one of the entries is blank
            if len(children) == 4:
                    
                    # Encode as utf-8 since people like to use retarded unicode characters in their name	
                    name = children[1].text_content().encode('utf_8', 'ignore')
                    online = children[3].text_content()
                    
                    # Skip over the row if the name is 'Player' since this means we are in the header
                    if name != 'Player':
                        
                        # Print only the names found in the list unless no names are provided
                        # in which case all are displayed
                        if in_names(name.lower()) or len(names) == 0:
                        
                            # Trim off the trailing 's'
                            online = online[:-1]
                                
                            # Calculate the minutes and seconds online
                            hours = int(online) / 3600
                            minutes = ( int(online)  - (hours * 3600 ) )/ 60
                            seconds = int(online) % 60
                            
                            s = name + " - "
                            
                            if (hours > 0):
                                s += str(hours) + "h "
                                
                            if (minutes > 0):
                                s += str(minutes) + "m "
                                
                            print s + str(seconds) + "s"
                            
    print ""


# Requests, parses, and prints the results from the kill log according to the options specified
def query_kill_logs():
    
    cur_count = 0
    
    # Get page
    page = requests.get('http://thebreach.ca/kill-log/')

    # Parse into a structured tree
    tree = html.fromstring(page.text)

    # Query just the table rows with kill log data
    rows = tree.xpath('//div[@class="entry themeform"]/div/table//tr')
    
    # Set local time to utc then offset by two hours to get the time used by thebreach.ca kill logs
    minutes_dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
    
    # Subtract the number of minutes specified by -t
    minutes_dt -= datetime.timedelta(minutes=t_min)
    
    #print datetime.datetime.strftime(minutes_dt, '%Y-%m-%d %H:%M:%S')
    
    # Header
    print "\n--- Kill Log ---\n"
    
    # Iterate over the rows of the kill log table
    for row in rows:
            
            # Returns a list containing each table data element for the table row	
            children = row.getchildren()
            
            # There should be 3 children but for some reason sometimes one of the entries is blank
            if len(children) == 3:
                    
                    # Encode as utf-8 since people like to use retarded unicode characters in their name
                    killed = children[0].text_content().encode('utf_8', 'ignore')
                    killer = children[1].text_content().encode('utf_8', 'ignore')
                    time = children[2].text_content()
    
                    # The string literal value 'Time' indicates we are in the header which should be skipped
                    if time != 'Time':
                            cur_count += 1
 
                            # Convert the time values into datetime objects so they can be compared
                            time_dt = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                            
                            # Stop if the current time is outside the range specified with -t
                            if (t_min != 0 and (time_dt < minutes_dt)):
                                break
                            
                            # Stop if the current count exceeds the maximum specified with -n
                            if max_count != 0 and cur_count > max_count:
                                break
                            
                            # Print the row if we are interested in the name of the killer or killed
                            # Will print all results if no "interesting" names are provided.
                            if in_names(killer.lower()) or in_names(killed.lower()) or len(names) == 0:
                                print killer + " killed " + killed + " at " + time


# Setup parser
parser = argparse.ArgumentParser(description='Queries the kill log and user list on the thebreach.ca Rust server')
parser.add_argument('-f', nargs=1, metavar='file', help = 'Reads input of names from file, with one name per line')
parser.add_argument('-t', nargs=1, metavar='minutes', help = 'Indicates how many minutes back to look at kill logs')
parser.add_argument('-n', nargs=1, metavar='count', help = 'Returns the first n results from the kill log')
parser.add_argument('-k', action='store_true', help = 'Queries kill log')
parser.add_argument('-p', action='store_true', help = 'Queries current player list')
parser.add_argument('-s', action='store_true', help = 'Allow partial (substring) name matches')
parser.add_argument('names', metavar='name', nargs='*')
args = parser.parse_args()

# Read names from file
if args.f:
    in_file = open(args.f[0], "r")
    
    lines = in_file.readlines()
    for line in lines:
        names.append(line.rstrip().lower()) # remove line termination characters
    
    in_file.close()

# Read names from command line
if args.names:
    for name in args.names:
        names.append(name.lower())
        
# Determine if we need to filter by time
if args.t:
    # Confirm that a number was actually entered
    p = re.compile("[0-9]+")
    if p.match(args.t[0]):
        t_min = int(args.t[0])
        
# Handles printing a maximum of n results
if args.n:
    # Confirm that a number was actually entered
    p = re.compile("[0-9]+")
    if p.match(args.n[0]):
        max_count = int(args.n[0])
        
# Query kill logs
if args.k:
    query_kill_logs()

# Query player list
if args.p:
    query_player_list()