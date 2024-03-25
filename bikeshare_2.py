import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_opts = ['january', 'feruary', 'march', 'april', 'may', 'june', 'all']
day_opts = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        city = input('Please insert the name of the city you are interested in:').lower()
        if city in CITY_DATA:
            print("Great, let's look at the data for", city.title())
            break
        else:
            print('This is not one of the supported cities, please provide the name of one of the three supported cities.')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please insert the month you are interested in, between January and June, '
                                    'or all if you are interested in the data for all months:').lower()
        if month in month_opts:
            print("Great, let's look at the data for", month.title())
            break
        else:
            print("Please provide a value between January and June or the word 'all' for all months")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please insert the day of the week you are interested in, '
                                    'or all if you are interested in the data for every day:').lower()
        if day in day_opts:
            print("Great, let's look at the data for", day.title())
            break
        else:
            print("Please provide a valid day of the week or the word 'all'")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df = df.dropna()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        month = month_opts.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print(df.head())

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    ## find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Popular Start Station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Popular End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['station_combo'] = list(zip(df['Start Station'], df['End Station']))
    popular_station_combo = df['station_combo'].mode()[0]
    print('Most Frequent Station Combination:', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def convert_seconds(seconds):
    # Create a timedelta object representing the duration in seconds
    duration = timedelta(seconds=seconds)

    # Access days and remaining seconds
    days = duration.days
    remaining_seconds = duration.seconds

    # Convert remaining seconds to minutes
    minutes = remaining_seconds // 60

    #calculate the seconds if any
    secs = remaining_seconds % 60

    return days, minutes, secs
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trav_days, total_trav_mins, total_trav_secs = convert_seconds(int(df['Trip Duration'].sum()))
    print('The total travel time for the selected time period is: ', total_trav_days, ' days', total_trav_mins, ' minutes',
          total_trav_secs, ' seconds')

    # display mean travel time
    mean_trav_days, mean_trav_mins, mean_trav_secs = convert_seconds(int(df['Trip Duration'].mean()))
    print('The mean travel time for the selected time period is: ', mean_trav_days, ' days', mean_trav_mins,
          ' minutes', mean_trav_secs, ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The value counts for the user types are:', user_types)

    # Display counts of gender
    gender_count = df['Gender'].value_counts()
    print('The value counts for the genders are:', gender_count)

    # Display earliest, most recent, and most common year of birth
    older = df['Birth Year'].min()
    younger = df['Birth Year'].max()
    most_common = df['Birth Year'].mode()[0]
    print('The earliest year of birth is:', older, ' the most recent year of birth is:', younger,
          ' the most common year of birth is:', most_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        try:
            time_stats(df)
        except KeyError:
            print('The time statistics could not be calculated due to missing data')

        try:
            station_stats(df)
        except KeyError:
            print('The station-related statistics could not be calculated due to missing data')
        try:
            trip_duration_stats(df)
        except KeyError:
            print('The trip duration statistics could not be calculated due to missing data')
        try:
            user_stats(df)
        except KeyError:
            print('Some user statistics could not be calculated due to missing data')

        idx = 0
        while True:
            raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
            if raw_data.lower() != 'no' and idx <= len(df):
                print(df.iloc[idx:idx+5])
                idx +=5
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
