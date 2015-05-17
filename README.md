# qbreach.py
Script to query the kill log and player list provided at http://thebreach.ca

#Usage: 

qbreach.py [-h] [-f file] [-t minutes] [-n count] [-k] [-p] [-s] [name [name ...]]

Queries the kill log and user list on the thebreach.ca Rust server

positional arguments:
  name

optional arguments:
  -h, --help  show this help message and exit
  -f file     Reads input of names from file, with one name per line
  -t minutes  Indicates how many minutes back to look at kill logs
  -n count    Returns the first n results from the kill log
  -k          Queries kill log
  -p          Queries current player list
  -s          Allow partial (substring) name matches
