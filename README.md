AngelList-Startups
==================

Using AngelList's API obtain data about all startups in NYC

#########################################################################
# Author: Nabil Jamaleddine
# Date  : 2014-01-03
# Description: Using AngelList's API obtain data about all startups.
# Output data as a csv file. Skips hidden startups.
# Rate Limit: 1000 requests per hour
# Parameters: sys.argv[1] = starting range for URLs to get startup info
#							sys.argv[2] = ending range for URLs
#	
#########################################################################

Each company on AngelList is represented by an id. 
Each request to the website will search for 1000 companies per hour using an external cron job with 2 input parameters for the file. 

angelliststartups.py "StartID" "EndID"

ex: angelliststartups.py "1" "1000"
The next can be angelliststartups.py "1001" "2000" etc...
