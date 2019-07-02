import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
        city = input("Choose a city (Chicago, New York City, Washington) from the data?\n").lower()
        if city in ('chicago', 'new york city', 'washington'):
            print('Thank you!')
            break
        else:
            print('The entered city is not in the dataset, Choose an other one.')
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Choose a month (january, february, march, april, may, june, all) from the data?\n").lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Thank you!')
            break
        else:
            print('The entered month is not in the dataset, Choose an other one.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Choose a day (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday) from the data?\n").lower()
        if day in ('all', 'monday', 'tuesday','wednesday','thursday','friday','saturday','sunday'):
            print('Thank you!')
            break
        else:
            print('The entered day is not in the dataset, Choose an other one.')

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month


    df['day_of_week'] = df['Start Time'].dt.weekday_name
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print("Most popular month is: ", popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print("Most popular month is: ", popular_day)

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    print("Most popular hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_stationstart = df['Start Station'].mode()[0]
    print("Most most commonly used start staton is: ", common_stationstart)

    # display most commonly used end station
    common_stationend = df['End Station'].mode()[0]
    print("Most most commonly used end staton is: ", common_stationend)

    # display most frequent combination of start station and end station trip
    
    most_freq_station_comb = df[['Start Station', 'End Station']].mode().loc[0]
    # most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]

    print("Most most frequent combination of start and end station trip is:", )
    print(most_freq_station_comb[0], "and", most_freq_station_comb[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_total = df['Trip Duration'].sum()
    print("Total travel time :", travel_total)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df.groupby('User Type').size()
    print("User counts:")
    for index,value in enumerate(user_counts):
        print( user_counts.index[index],": ",value )

    # Display counts of gender
    try:
        gender_counts = df.groupby('Gender').size()
        print("\nGender count:")
        for index,value in enumerate(gender_counts):
            print( gender_counts.index[index],": ",value )
    except:
        print("No gender data in this dataset")

    # Display earliest, most recent, and most common year of birth

    try:
        earliest_birth = df['Birth Year'].min()
        print("\nEarliest Birthday :", int(earliest_birth))
        recent_birth = df['Birth Year'].max()
        print("Most recent Birthday :", int(recent_birth))
        common_birth = df['Birth Year'].mode()
        print("Most common year of birth :", int(common_birth))
    except:
        print("No birth year data in this dataset")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data."""
    rows_count = df.shape[0]

    # iterate start from 0 until the end of number of rows by steps of 5
    for i in range(0, rows_count, 5):

        if i == 0:
            yes = input('Do you want to see raw data? \'yes\' or \'no\'\n> ')
            if yes.lower() != 'yes': 
                break    

        print(df.iloc[i:i+5,:])

        more_lines = input('do you want to see more 5 lines of raw data? \'yes\' or \'no\'\n> ')
        if more_lines.lower() != 'yes': 
            break    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
