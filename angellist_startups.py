"""
Author: Nabil Jamaleddine
Date: 2014-01-03

Description: Using AngelList's API obtain startup data.
Output data as a csv file. Skips hidden startups.

Rate Limit: 1000 requests per hour

Parameters:
    sys.argv[1] = starting range for URLs to get startup info
    sys.argv[2] = ending range for URLs
    sys.argv[3] = Location to search
"""
from __future__ import print_function
import csv
import json
import requests
import sys
import unicodedata


def create_url_list(start_range, end_range):
    """ Generate a list of URLs to be searched """
    urls = []
    start_range = int(start_range)
    end_range = int(end_range)

    # Test attempts at making invalid urls
    if start_range == "" or end_range == "":
        print("Invalid range. Please enter a value greater than 0 for the start range.")
        print("The end range must be greater than the start range.")
        sys.exit()

    if start_range < 1:
        print("Invalid start range for URL, start range should be at least 1.")
        start_range = 1

    if end_range < start_range:
        print("Invalid end range for URL, end range should be greater than start range.")
        end_range = start_range + 1

    for i in range(start_range, end_range):
        urls.append('https://api.angel.co/1/startups/{}'.format(i))

    return urls


def validate_data(data):
    """
    Simple Data Validation Function

    Strip new line characters and encode as ascii instead of unicode.

    If column is empty we put a space character to maintain the correct number
    of columns in the CSV file.
    """
    if data == '':
        return ' '

    elif (type(data) == int or type(data) == bool or type(data) == list):
        return data

    else:
        return unicodedata.normalize(
            'NFKD', data.rstrip('\r?\n|\r/')
        ).encode('ascii', 'ignore')


def validate_location(location):
    """
    Validate the location of the Startup Company
    """
    try:
        return unicodedata.normalize(
            'NFKD', location[0]['display_name'].rstrip('\r?\n|\r/')
        ).encode('ascii', 'ignore')

    except IndexError:
        return 'N/A'

# Store list of urls that will be used for obtaining startup company information
url_list = []
# If somehow no data is obtained, we can relay an error message to the user.
list_count = 0

# Get Arguments
start_range = sys.argv[1]
end_range = sys.argv[2]
location = sys.argv[3].strip()

print("Obtaining Startup Company Information...")
print("Hidden Startups will be skipped since we cannot obtain their information.")

# Create and open CSV output file
with open("startups.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write Header row for CSV
    csv_writer.writerow([
        "Id", "Community Profile", "Name", "AngelList URL", "Logo URL",
        "Thumbnail URL", "Quality", "Product Description", "High Concept",
        "Followers", "Company URL", "Created At", "Updated At",
        "Twitter", "Blog", "Video URL", "City"
    ])

    # Pass in parameters from the command line while running a cron job
    url_list = create_url_list(start_range, end_range)

    for i in range(len(url_list)):
        # Create an http request to angellist
        r = requests.get(url_list[i])

        # If the API returns a 404, skip the data
        if r.status_code != 404:
            data = json.loads(r.content)

            if data['hidden'] == False:
                startup_location = validate_location(data['locations'])

                # Only Store NYC locations
                if startup_location == location:
                    list_count += 1

                    csv_writer.writerow([
                        validate_data(data.get('id')),
                        validate_data(data.get('community_profile')),
                        validate_data(data.get('name')),
                        validate_data(data.get('angellist_url')),
                        validate_data(data.get('logo_url')),
                        validate_data(data.get('thumb_url')),
                        validate_data(data.get('quality')),
                        validate_data(data.get('product_desc')),
                        validate_data(data.get('high_concept')),
                        validate_data(data.get('follower_count')),
                        validate_data(data.get('company_url')),
                        validate_data(data.get('created_at')),
                        validate_data(data.get('updated_at')),
                        validate_data(data.get('twitter_url')),
                        validate_data(data.get('blog_url')),
                        validate_data(data.get('video_url')),
                        startup_location,
                    ])
                    print(data.get('name'))

    # Display an error message if no data is found for any companies
    if list_count == 0:
        print(
            "No Startup Company Information was found or the server at "
            "Angellist could not be reached."
        )
