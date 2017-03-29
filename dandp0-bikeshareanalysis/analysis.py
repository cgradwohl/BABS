#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#
# Chris Gradwohl March 2017
# analysis.py
# exploration file for the open Bay Area Bike Share Data set
# in this exploration we are going to look at a subset of trip data to
# get our bearing and understand our data.
#
# The data comes in three parts:
#	the first half of Year 1 (files starting 201402),
#	the second half of Year 1 (files starting 201408),
#	and all of Year 2 (files starting 201508).
#
#
# There are three main datafiles associated with each part:
#	trip data showing information about each trip taken in the system (*_trip_data.csv),
#	information about the stations in the system (*_station_data.csv),
#	and daily weather data for each city in the system (*_weather_data.csv).
#
#
# In this exploration, we're going to concentrate on factors in the trip
# data that affect the number of trips that are taken.
#
# Let's focus on a few selected columns:
#	trip duration,
#	start time,
#	start terminal,
# 	end terminal,
#	subscription type.
#
#	Start time will be divided into year, month, and hour components.
#
# We will also add a column for the day of the week and abstract the start
# and end terminal to be the start and end city.
#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#	#

# import all necessary packages and functions.
import csv
from datetime import datetime
import numpy as np
import pandas as pd
from babs_datacheck import question_3
from babs_visualizations import usage_stats, usage_plot
from IPython.display import display
# this attempts to make matplotlib run display inline
# %matplotlib inline


#  NOTE file_out is a new file that we create by reading a
#	subset of 201402_trip_data.csv and writing that subset to
#   201309_trip_data.csv, right now the filename is not clear.


# file locations
file_in  = '201402_trip_data.csv'
file_out = '201309_trip_data.csv' # <-- to be subset file we write too

# open files with write and read privledges
with open(file_out, 'w') as f_out, open(file_in, 'r') as f_in:
    # set up csv reader and writer objects
    in_reader = csv.reader(f_in)
    out_writer = csv.writer(f_out)

    # write rows from in-file to out-file until specified date reached
    while True:
        datarow = next(in_reader)
        # trip start dates in 3rd column, m/d/yyyy HH:MM formats
        if datarow[2][:9] == '10/1/2013':
            break
        out_writer.writerow(datarow)


# Display the first few rows of the file we just created
print '\n\n\nTrip Data Subset file header: \n'
sample_data = pd.read_csv('201309_trip_data.csv')
display(sample_data.head())


print '\n\n\nStation Data file header: \n'
# Display the first few rows of the station data file.
station_info = pd.read_csv('201402_station_data.csv')
display(station_info.head())

# Since it is possible that more stations are added or dropped over time,
# this function will allow us to combine the station information across
# all three parts of our data when we are ready to explore everything.
# This function will be called by another function later on to create the mapping.
def create_station_mapping(station_data):
    """
    Create a mapping from station IDs to cities, returning the
    result as a dictionary.
    """
    station_map = {}
    for data_file in station_data:
        with open(data_file, 'r') as f_in:
            # set up csv reader object - note that we are using DictReader, which
            # takes the first row of the file as a header row for each row's
            # dictionary keys
            weather_reader = csv.DictReader(f_in)


			# this is tricky here
			# station_map['key'] = row['landmark'], where 'key' = row['station_id']
            for row in weather_reader:
                station_map[row['station_id']] = row['landmark']
    return station_map


# There are two tasks that you will need to complete to finish the summarise_data()
# function.

# First, you should perform an operation to convert the trip durations from
# being in terms of seconds to being in terms of minutes. (There are 60 seconds in a
# minute.)

# Secondly, you will need to create the columns for the year, month, hour,
# and day of the week. Take a look at the documentation for datetime objects in the
# datetime module. Find the appropriate attributes and method to complete the below code.
def summarise_data(trip_in, station_data, trip_out):
    """
    This function takes trip and station information and outputs a new
    data file with a condensed summary of major trip information. The
    trip_in and station_data arguments will be lists of data files for
    the trip and station information, respectively, while trip_out
    specifies the location to which the summarized data will be written.
    """
    # generate dictionary of station - city mapping
    station_map = create_station_mapping(station_data)

    with open(trip_out, 'w') as f_out:
        # set up csv writer object
        out_colnames = ['duration', 'start_date', 'start_year',
                        'start_month', 'start_hour', 'weekday',
                        'start_city', 'end_city', 'subscription_type']
        trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
        trip_writer.writeheader()

        for data_file in trip_in:
            with open(data_file, 'r') as f_in:
                # set up csv reader object
                trip_reader = csv.DictReader(f_in)

                # collect data from and process each row
                for row in trip_reader:
                    new_point = {}

                    # convert duration units from seconds to minutes
                    ### Question 3a: Add a mathematical operation below   ###
                    ### to convert durations from seconds to minutes.     ###
                    new_point['duration'] = float(row['Duration'])/60

                    # reformat datestrings into multiple columns
                    ### Question 3b: Fill in the blanks below to generate ###
                    ### the expected time values.                         ###
                    trip_date = datetime.strptime(row['Start Date'], '%m/%d/%Y %H:%M')
                    new_point['start_date']  = trip_date.strftime('%Y-%m-%d')
                    new_point['start_year']  = trip_date.year
                    new_point['start_month'] = trip_date.month
                    new_point['start_hour']  = trip_date.hour
                    new_point['weekday']     = trip_date.weekday()

                    # remap start and end terminal with start and end city
                    new_point['start_city'] = station_map[row['Start Terminal']]
                    new_point['end_city'] = station_map[row['End Terminal']]
                    # two different column names for subscribers depending on file
                    if 'Subscription Type' in row:
                        new_point['subscription_type'] = row['Subscription Type']
                    else:
                        new_point['subscription_type'] = row['Subscriber Type']

                    # write the processed information to the output file.
                    trip_writer.writerow(new_point)

# Process the data by running the function we wrote above.
station_data = ['201402_station_data.csv']
trip_in = ['201309_trip_data.csv']
trip_out = '201309_trip_summary.csv'
summarise_data(trip_in, station_data, trip_out)

# Load in the data file and print out the first few rows
sample_data = pd.read_csv(trip_out)
display(sample_data.head())

# Verify the dataframe by counting data points matching each of the time features.
question_3(sample_data)



# Data Exploration
trip_data = pd.read_csv('201309_trip_summary.csv')

usage_stats(trip_data)

usage_plot(trip_data, 'subscription_type')
usage_plot(trip_data, 'duration')

# plot using the filter to make data more useful and understandable
usage_plot(trip_data, 'duration', ['duration < 60'])

# still need to clean up the presentation, here we corect bin boundaries and edges
usage_plot(trip_data, 'duration', ['duration < 60'], boundary = 0, bin_width = 5)








# process' data into a single data file
station_data = ['201402_station_data.csv',
                '201408_station_data.csv',
                '201508_station_data.csv' ]
trip_in = ['201402_trip_data.csv',
           '201408_trip_data.csv',
           '201508_trip_data.csv' ]
trip_out = 'babs_y1_y2_summary.csv' # <-- new data file :)

# This function will take in the station data and trip data and
# write out a new data file to the name listed above in trip_out.
summarise_data(trip_in, station_data, trip_out)

# read and print the data header
trip_data = pd.read_csv('babs_y1_y2_summary.csv')
print 'New Condensed Data File'
display(trip_data.head



# Use the usage_stats() and usage_plot() methods from
# babs_visualizations.py to exlpore the data set and report
# new findings.

# usage_plot(first, second, third) , where:
 		# first(required)  - loaded data frame for data analysis
		# second(required) - variable, trip counts will be divided
		# third(optional)  - data filters limiting the data points
		# 					that will be counted. Filters should be given as a list
		# 					of conditions, each element should be a string in the
		# 					following format: '<field> <op> <value>' using one of
		# 					the following operations: >, <, >=, <=, ==, !=. Data
		# 					points must satisfy all conditions to be counted or
		# 					visualized. For example, ["duration < 15",
		# 					"start_city == 'San Francisco'"] retains only trips that
		# 					 originated in San Francisco and are less than 15 minutes
		# 					long.

# additional parameters
# "n_bins" specifies the number of bars in the resultant plot (default is 10).
# "bin_width" specifies the width of each bar (default divides the range of the data by number of bins).
# "n_bins" and "bin_width" cannot be used simultaneously.
# "boundary" specifies where one of the bar edges will be placed; other bar edges will be placed around
# that value (this may result in an additional bar being plotted). This argument may be used alongside
# the "n_bins" and "bin_width" arguments.



# Exploretory analysis with usage_plot() and usage_stats()
usage_plot(trip_data)

usage_stats(trip_data)



# Final Plot 1
usage_plot(trip_data)



# Final Plot 2
usage_plot(trip_data)
