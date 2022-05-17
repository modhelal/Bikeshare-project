# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:09:05 2021

@author: user
"""
import time
import sys
from time import strftime
from time import gmtime
import pyinputplus as pyip
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def introduction():
    """ welcome statement"""

    opening_statment = input('WelcOme(-.-)Do you want to know about US'
                             ' BikeShare data?!'
                             'Enter yes or no: \n')
    if opening_statment == "yes":
        print("'Hello! Let\'s explore some US bikeshare data!'")
    elif opening_statment == "no":
        print("Thank you for your time")
        sys.exit()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no'
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply'
        no day filter
    """

    cities = ['chicago', 'new york city', 'washington']
    city = pyip.inputMenu(cities, 'please, pick one of te following '
                                  'cities\n').lower()

    select_month = ['all', 'january', 'february', 'march', 'april', 'may',
                    'june']
    month = pyip.inputMenu(select_month, 'please pick month of the'
                                         ' following and pick \'all\' if you '
                                         'want no month filter.\n').lower()

    days_of_week = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday',
                    'thursday',  'friday', 'all']
    while True:
        try:
            day = input('please pick one of the week days[saturday,'
                        'sunday, .....,friday], or \'all\'to apply no'
                        ' day filter:\n').lower()

        except ValueError:
            continue
        if day in days_of_week:
            print('Now, let\'s start analysis...')
        else:
            print('please, enter valid day')
        break

    return city, month, day


def load_data(city, month, day):
    """
  Loads data for the specified city and filters by month and day if applicable.

  Args:
      (str) city - name of the city to analyze
      (str) month - name of the month to filter by, or "all" to apply no'
      month filter
      (str) day - name of the day of week to filter by, or "all" to apply'
      no day filter
  Returns:
      bike_data - Pandas DataFrame containing city data filtered by month'
      and day
  """

    # load data file into a dataframe
    bike_data = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    bike_data['Start Time'] = pd.to_datetime(bike_data['Start Time'])

    # extract month, day and hour from Start Time to create new columns
    bike_data['month'] = bike_data['Start Time'].dt.month_name()
    bike_data['day'] = bike_data['Start Time'].dt.day_name()
    bike_data['hour'] = bike_data['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        bike_data = bike_data[bike_data['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        bike_data = bike_data[bike_data['day'] == day.title()]

    return bike_data


def time_stats(bike_data, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    while True:
        if month == 'all' and day == 'all':

            # display the most common month
            most_common_month = bike_data['month'].mode()[0]
            print('The most common month of travel is:', most_common_month)

            # display the most common day
            most_common_day = bike_data['day'].mode()[0]
            print('The most common day of travel :', most_common_day)

            # display the most common hour
            most_common_hour = bike_data['hour'].mode()[0]
            print('The most common hour of travel is:', most_common_hour)

        if month == 'all' and day != 'all':

            # display the most common month
            most_common_month = bike_data['month'].mode()[0]
            print('The most common month of travel is:', most_common_month)

            # display the most common hour
            most_common_hour = bike_data['hour'].mode()[0]
            print('The most common hour of travel is:', most_common_hour)

        if day == 'all' and month != 'all':

            # display the most common day
            most_common_day = bike_data['day'].mode()[0]
            print('The most common day of travel is:', most_common_day)

            # display the most common hour
            most_common_hour = bike_data['hour'].mode()[0]
            print('The most common hour of day\'s travel is', most_common_hour)

        if month != 'all' and day != 'all':

            # display the most common hour
            most_common_hour = bike_data['hour'].mode()[0]
            print('The most common hour of travel during month:',
                  most_common_hour)

        break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(bike_data):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stations = bike_data['Start Station']
    most_common_start = start_stations.mode()[0]
    print('The most commonly used start station is:', most_common_start)
    print(most_common_start, 'is used about: ',
          start_stations.value_counts()[most_common_start],
          'times')

    # display most commonly used end station
    most_common_end = bike_data.mode()['End Station'][0]
    print('The most commonly used End Station is:', most_common_end)
    print(most_common_end, 'is used about: ',
          bike_data['End Station'].value_counts()[most_common_end], 'times')

    # display most frequent combination of start station and end station trip
    combination = bike_data['Start Station'] + ('/') + bike_data['End Station']
    most_common_combination = combination.mode()[0]
    print('The most common Start-End station trip is\n',
          most_common_combination)
    print(most_common_combination, 'is used about',
          combination.value_counts()[most_common_combination], 'times')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(bike_data):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = bike_data['Trip Duration'].sum()
    duration = total_trip_duration
    day = duration // (3600*24)
    duration %= (3600*24)
    hour = duration // 3600
    duration %= 3600
    minute = duration // 60
    duration %= 60
    second = duration
    print('Total Trip Duration in seconds are:', total_trip_duration)
    print('Total Trip Duration in d hr min sec are: {} day(s) {} hour(s) {}'
          ' minute(s) {} second(s)'.format(day, hour, minute, second))

    # display mean travel time
    mean_in_seconds = bike_data['Trip Duration'].mean()
    mean_travel_time = strftime('%H:%M:%S', gmtime(mean_in_seconds))
    print('Mean Travel Time in seconds are:', mean_in_seconds)
    print('Mean Travel Time in hours are:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(bike_data, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('N.B ... Data for washington does not display Gender and Birthday')

    # Display counts of user types
    user_types = bike_data['User Type'].value_counts()
    print('The counts of User Types are:\n', user_types)

    while True:
        if city in ('new york city', 'chicago'):

            # Display counts of gender in ('new york city', 'chicago')
            gender_counts = bike_data['Gender'].value_counts()
            print('The Gender Counts are :\n', gender_counts)

            # Display earliest, most recent, and most common year of birth
            earliest_birth_year = bike_data['Birth Year'].min()
            print('The Earliest year of birth is:', int(earliest_birth_year))

            recent_birth_year = bike_data['Birth Year'].max()
            print('The most recent year of birth is:', int(recent_birth_year))

            common_birth_year = bike_data['Birth Year'].mode()[0]
            print('The most common year of birth is:', int(common_birth_year))
        break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(bike_data):
    """ Asking user about displaying Raw Data """

    raw = input(' Do you want showing the first 5 rows of data? yes or no \n')

    if raw.lower() == 'yes':
        rows = 0
        while True:
            print(bike_data.iloc[rows:rows+5])
            rows += 5
            more_data = input("Do you need mor data? \n")
            if more_data.lower() != 'yes':
                break


def main():
    """
       play all programe functions and giving option to restart analysis for
       more choices"""

    while True:
        introduction()
        city, month, day = get_filters()
        bike_data = load_data(city, month, day)

        time_stats(bike_data, month, day)
        station_stats(bike_data)
        trip_duration_stats(bike_data)
        user_stats(bike_data, city)
        raw_data(bike_data)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank You')
            break


if __name__ == "__main__":
    main()
from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])