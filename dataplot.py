import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
import matplotlib.ticker as ticker
import argparse
import dateutil.parser
import random


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Play with time group plots')
    ap.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    ap.add_argument('-n', '--number', type=int, default=5000, help='Number of data points')
    ap.add_argument('-s', '--start', type=dateutil.parser.parse, default=dt.datetime(2023, 1, 1), help='Start date')
    ap.add_argument('-e', '--end', type=dateutil.parser.parse, default=dt.datetime.now(), help='End date')
    ap.add_argument('-g', '--group', type=str, default='1H', help='Time grouper string')
    ap.add_argument('-w', '--weeks', type=int, default=4, help='Number of weeks to plot')
    args = ap.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    # Generate random times
    times = np.sort(np.random.uniform(args.start.timestamp(), args.end.timestamp(), size=args.number))
    colours = [random.choice(['red', 'green', 'blue', 'cyan', 'magenta', 'yellow'])
               for _ in range(args.number)]

    df = pd.DataFrame({"times": times, "colours": colours})
    df['times'] = pd.to_datetime(df['times'], unit='s')
    df = df.set_index('times')
    dg = df.groupby(pd.Grouper(freq=args.group))
    groups = dg['colours'].count()

    # Do weekly plots on the same graph
    fig, ax = plt.subplots(nrows=args.weeks, ncols=1, figsize=(20, 28))
    plt.locator_params(axis='x', nbins=4)
    for week in range(args.weeks):
        start = args.end - dt.timedelta(weeks=week)
        end = start - dt.timedelta(weeks=1)
        logging.info(f"Plotting {start} to {end}")
        dfw = df[(df.index > end) & (df.index <= start)]
        dgw = dfw.groupby(pd.Grouper(freq=args.group))
        groupsw = dgw['colours'].count()
        ax[week].plot(groupsw.index, groupsw.values)
        ax[week].xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax[week].xaxis.set_minor_formatter(mdates.DateFormatter('%H'))
        ax[week].xaxis.set_major_locator(ticker.MaxNLocator())
        ax[week].set_title(f"From {end} to {start}")
        ax[week].set_xlabel('Time')
        ax[week].set_ylabel('Count')
        ax[week].grid(True)
    plt.show()
    plt.close()

