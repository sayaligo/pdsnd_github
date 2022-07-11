import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': '/Users/sayaliagalave/Desktop/chicago.csv',
              'new york city': '/Users/sayaliagalave/Desktop/new_york_city.csv', 'washington': '/Users/sayaliagalave/Desktop/washington.csv' }

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
        city = input("Enter the city name between chicago, new york city or washington:\n").lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Please enter the valid name:")


    # get user input for month (all, january, february, ... , june)
    months = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = input("Enter the month name or enter all to see data of all the 6 months:\n").lower()
        if month in months:
            break
        else:
            print("Enter the month name in string and not in an integer form:")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    while True:
        day = input("Enter the day of the week or enter all to see the data of the entire week:\n").lower()
        if day in days:
            break
        else:
            print("Day should be entered in string and not in integer form:")

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
    # load city data
    df = pd.read_csv(CITY_DATA[city])

    # converting start_time column to date_time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extracting month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


   # filter by months
    if month != 'all':
     # filter by month to create the new dataframe
       df = df[df['month'].str.startswith(month.title())]

    # filter by day of week
    if day != 'all':
    # filter by day of week to create the new dataframe
       df = df[df['day_of_week'].str.startswith(day.title())]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month_name()
    most_common_month = df['month'].mode()[0]
    print("The most common month is:", most_common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day is:", most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is:", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is:", most_common_start_station)


    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is:", most_common_end_station)


    # display most frequent combination of start station and end station trip
    frequent_comb = 'from' + df['Start Station'] +" to "+ df['End Station'].mode()[0]
    print("The most frequent combination of start station and end station trip:", frequent_comb)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is:", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 3600.0
    print("mean travel time in hours is:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)


    """try clause in case of gender absent in filter and 
       in case of birth year column is absent in file."""
   
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n\n{gender}")
    except:
        print("\nThis file has no gender column.")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest, recent, common_year = int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Function if user wants to see additional data lines
def show_data (df):
    """5 rows in each pass"""
    print('press enter to see data, press no to skip')
    x = 0
    while (input()!= 'no'):
        x = x+5
        print(df.head(x))

# Main function to call other functions
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nDo you want to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
