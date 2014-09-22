"""
Author: Nabil Jamaleddine
Date: 2014-01-03

Description: Using AngelList's API obtain data about all startups.
Output data as a csv file. Skips hidden startups.

Rate Limit: 1000 requests per hour

Parameters:
    sys.argv[1] = starting range for URLs to get startup info
    sys.argv[2] = ending range for URLs
"""
import requests
import csv
import json
import re
import unicodedata
import sys

# Generate a list of URLs to be searched
def create_url_list(start_range, end_range):
    urls = []
    start_range = int(start_range)
    end_range = int(end_range)

    # Test attempts at making invalid urls
    if start_range == "" or end_range == "":
        print "Invalid range. Please enter a value greater than 0 for the start range."
        print "The end range must be greater than the start range."
        sys.exit()

    if start_range < 1:
        print "Invalid start range for URL, start range should be at least 1."
        start_range = 1

    if end_range < start_range:
        print "Invalid end range for URL, end range should be greater than start range."
        end_range = start_range + 1

    for i in range(start_range, end_range):
        urls.append(''.join(['https://api.angel.co/1/startups/', str(i)]))

    return urls

# Simple Data Validation Function
# Strip new line characters and encode as ascii instead of unicode.
# If column is empty we put a space character to maintain the correct number of columns in the CSV file.
def validate_data(data):
    if data == '':
        return ' '

    elif (type(data) == int or type(data) == bool or type(data) == list):
        return data

    else:
        return unicodedata.normalize('NFKD', data.rstrip('\r?\n|\r/')).encode('ascii','ignore')

# Validate the location of the Startup Company
def validate_location(location):
    try:
        return unicodedata.normalize('NFKD', location[0]['display_name'].rstrip('\r?\n|\r/')).encode('ascii','ignore')

    except IndexError:
        return 'N/A'


url_list = [] # Store list of urls that will be used for obtaining startup company information
list_count = 0 # If somehow no data is obtained, we can relay an error message to the user.

print "Obtaining Startup Company Information..."
print "Hidden Startups will be skipped since we cannot obtain their information."

# Create and open CSV output file
output_file = csv.writer(open("startups.csv", "wb+"))

# Write Header row for CSV
output_file.writerow(["Id", "Community Profile", "Name", "AngelList URL", "Logo URL", "Thumbnail URL", "Quality",
                    "Product Description", "High Concept", "Followers", "Company URL", "Created At", "Updated At",
                    "Twitter", "Blog", "Video URL", "City"])

# Pass in parameters from the command line while running a cron job
url_list = create_url_list(sys.argv[1], sys.argv[2])

for i in range(len(url_list)):
    # Create an http request to angellist
    r = requests.get(url_list[i])

    #print r.headers

    # If the API returns a 404, skip the data
    if r.status_code != 404:
        data = json.loads(r.content) # data is stored as a dictionary

        # If the startup Company List Information isn't hidden, save to List
        if data['hidden'] == False:
            startup_location = validate_location(data['locations'])

            # Only Store NYC locations
            if(startup_location == 'New York City'):
                list_count += 1

                output_file.writerow([validate_data(data['id']),
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
                    startup_location,
                    ])
                print data['name']

# Display an error message if no data is found for any companies
if list_count == 0:
    print "No Startup Company Information was found or the server at Angellist could not be reached."