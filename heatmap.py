"""
Second attempt at visualising busy periods. This time using a heatmap. The idea is to have a grid with
hours of the day being columns and days of the week being rows. The colour of each cell is determined
by the number of events that occurred in that hour of the day on that day of the week.
"""

import logging
import datetime as dt
import argparse
import random

import pandas as pd

def GenerateShapedRandoms(start, weeks, number):
    """
    Generates a random set of times between start and end. The times are distributed according to the
    dayhist and hourhist distributions - i.e. Mondays will be busier than Sundays, working hours
    will be busier than non-working hours etc.

    Weeks starts on a Monday (0) and end on a Sunday (6)

    Generates a weeks worth of data
    :param start: Starting date str e.g. 1997-09-26
    :param weeks: Number of weeks to generate
    :param number: Number of random times
    :return: list of datetime.datetime objects
    """

    days_per_week = 7
    hours_per_day = 24
    minutes_per_hour = 60
    seconds_per_minute = 60
    microseconds_per_second = 1000000

    # Convert start to a datetime object and work out the week number
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    logging.debug(f"Start date {start_date} is a {start_date:%A} (i.e. number {start_date.weekday()})")
    # So work out and add the offset such that the start date is a Monday
    offset = (days_per_week - start_date.weekday()) % days_per_week
    start_date = start_date + dt.timedelta(days=offset)
    logging.debug(f"Start date is now {start_date} (i.e. number {start_date.weekday()})")
    for week in range(weeks):
        logging.debug(f"Generating week {week}")
        for i in range(number//weeks):
            # Generate a random day of the week
            day = random.choices(list(range(days_per_week)), weights=[1, 2, 3, 2, 1, 0, 0], k=1)[0]
            # Generate a random hour of the day
            hour = random.choices(list(range(hours_per_day)), weights=[0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 2,
                                                                       1, 1, 3, 4, 3, 2, 1, 0, 0, 0, 0, 0], k=1)[0]
            # Generate a random minute of the hour
            minute = random.randrange(minutes_per_hour)
            # Generate a random second of the minute
            second = random.randrange(seconds_per_minute)
            # Generate a random microsecond of the second
            microsecond = random.randrange(microseconds_per_second)
            # Generate a random time
            time = dt.time(hour=hour, minute=minute, second=second, microsecond=microsecond)
            # Generate a random datetime
            datetime = dt.datetime.combine(start_date + dt.timedelta(days=week*days_per_week+day), time)
            yield datetime

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Play with time group plots')
    ap.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    ap.add_argument('-n', '--number', type=int, default=5000, help='Number of data points')
    ap.add_argument('-s', '--start', type=str, default='2023-01-01', help='Start date')
    ap.add_argument('-w', '--weeks', type=int, default=4, help='Number of weeks to generate')
    args = ap.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    colours = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white']
    sizes = ['small', 'medium', 'large']
    data = sorted([{'time': t, 'colour': random.choice(colours), 'size': random.choice(sizes)}
            for t in GenerateShapedRandoms(args.start, args.weeks, args.number)], key=lambda x: x['time'])
    df = pd.DataFrame(data)
    df['day'] = df['time'].dt.day_name()
    df['hour'] = df['time'].dt.hour
