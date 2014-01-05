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

import requests
import csv
import json
import re
import unicodedata
import sys

# Generate a list of URLs to be searched
def create_urlList(startRange, endRange):
	urls = []

	# Test attempts at making invalid urls
	if(startRange == "" or endRange == ""):
		print "Invalid range. Please enter a value greater than 0 for the start range."
		print "The end range must be greater than the start range."
		sys.exit()

	if(startRange < 1):
		print "Invalid start range for URL, start range should be at least 1."
		startRange = 1

	if(endRange < startRange):
		print "Invalid end range for URL, end range should be greater than start range."
		endRange = startRange + 1

	for i in range(startRange, endRange):
		urls.append(''.join(['https://api.angel.co/1/startups/', str(i)]))

	return urls

# Simple Data Validation Function
# Strip new line characters and encode as ascii instead of unicode.
# If column is empty we put a space character to maintain the correct number of columns in the CSV file.
def validate_data(data):
	if(data == ''):
		return ' '

	elif(type(data) == int or type(data) == bool or type(data) == list):
		return data
	
	else:
		return unicodedata.normalize('NFKD', data.rstrip('\r?\n|\r/')).encode('ascii','ignore')

# Validate the location of the Startup Company
def validate_location(location):
	try:
		return unicodedata.normalize('NFKD', location[0]['display_name'].rstrip('\r?\n|\r/')).encode('ascii','ignore') 

	except IndexError:
		return 'N/A'


urlList = [] # Store list of urls that will be used for obtaining startup company information
listCount = 0 # If somehow no data is obtained, we can relay an error message to the user.

print "Obtaining Startup Company Information..."
print "Hidden Startups will be skipped since we cannot obtain their information."

# Create and open CSV output file
outputFile = csv.writer(open("startups.csv", "wb+"))

# Write Header row for CSV
outputFile.writerow(["Id", "Community Profile", "Name", "AngelList URL", "Logo URL", "Thumbnail URL", "Quality", 
													 "Product Description", "High Concept", "Followers", "Company URL", "Created At", "Updated At",
													 "Twitter", "Blog", "Video URL", "City"])

# Pass in parameters from the command line while running a cron job
urlList = create_urlList(sys.argv[1], sys.argv[2])

for i in range(len(urlList)):
	# Create an http request to angellist
	r = requests.get(urlList[i])

	#print r.headers

	# If the API returns a 404, skip the data
	if(r.status_code != 404):
		data = json.loads(r.content) # data is stored as a dictionary
		
		# If the startup Company List Information isn't hidden, save to List
		if(data['hidden'] == False):
			startupLocation = validate_location(data['locations'])

			# Only Store NYC locations
			if(startupLocation == 'New York City'):
				listCount += 1

				outputFile.writerow([validate_data(data['id']),
														 validate_data(data['community_profile']), 
														 validate_data(data['name']), 
														 validate_data(data['angellist_url']), 
														 validate_data(data['logo_url']), 
														 validate_data(data['thumb_url']), 
														 validate_data(data['quality']),
														 validate_data(data['product_desc']),
														 validate_data(data['high_concept']),
														 validate_data(data['follower_count']),
														 validate_data(data['company_url']),
														 validate_data(data['created_at']),
														 validate_data(data['updated_at']),
														 validate_data(data['twitter_url']),
														 validate_data(data['blog_url']),
														 validate_data(data['video_url']),
														 startupLocation,
														 ])
				print data['name']

# Display an error message if no data is found for any companies
if(listCount == 0):
	print "No Startup Company Information was found or the server at Angellist could not be reached."