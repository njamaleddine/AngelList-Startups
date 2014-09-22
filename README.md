AngelList-Startups
==================

Using AngelList's API obtain data about all startups in NYC
-----------------------------------------------------------

*Author:* Nabil Jamaleddine
*Date:* 2014-01-03
*Description:* Using AngelList's API obtain data about all startups. Output data as a csv file. Skips hidden startups.
API Rate Limit: 1000 requests per hour

*Parameters:*
sys.argv[1] = starting range for URLs to get startup info
sys.argv[2] = ending range for URLs

Each company on AngelList is represented by an id.
Each request to the website could potentially be scraped at 1000 companies per hour using an external cron job or task queue with 2 the start and end parameters.

AngelListStartups.py may run as a standalone script through a python shell as such:
`python AngelListStartups.py {start_number} {end_number}`

Ex:
`python AngelListStartups.py 1 1000`