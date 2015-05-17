# qbreach.py
Script to query the kill log and player list provided at http://thebreach.ca

##Usage: 

**qbreach.py [-h] [-f file] [-t minutes] [-n count] [-k] [-p] [-s] [name [name ...]]**

&nbsp;&nbsp;&nbsp;&nbsp;Queries the kill log and user list for thebreach.ca Rust server

positional arguments:
  
  &nbsp;&nbsp;&nbsp;&nbsp;name
  
optional arguments:
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-h, --help**  show this help message and exit
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-f file**     Reads input of names from file, with one name per line
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-t minutes**  Indicates how many minutes back to look at kill logs
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-n count**    Returns the first *count* results from the kill log
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-k**          Queries kill log
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-p**          Queries current player list
  
  &nbsp;&nbsp;&nbsp;&nbsp;**-s**          Allow partial (substring) name matches
