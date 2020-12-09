"""Library of functions for behavior analysis
    * import_behavior_data - inputs data from BORIS csv
    * plot_zscore - plots z-score for each behavior occurance
"""
import sys
from statistics import mean
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def import_behavior_data(BORIS_filename, timestamp_filename):
    """Takes a file name, returns a dataframe of parsed data

        Parameters
        ----------
        BORIS_filename: string
                        The path to the CSV file

        Returns:
        --------
        behaviorData: pandas dataframe
                contains:
                     Time(total msec), Time(sec), Subject,
                     Behavior, Status
        """
    # Open file, catch errors
    try:
        BORISData = pd.read_csv(BORIS_filename, header=15)  # starts at data
    except FileNotFoundError:
        print("Could not find file: " + BORIS_filename)
        sys.exit(1)
    except PermissionError:
        print("Could not access file: " + BORIS_filename)
        sys.exit(2)

    # Drop unecessary columns
    behaviorData = BORISData.drop(['Media file path', 'Total length', 'FPS',
                                   'Behavioral category', 'Comment'], axis=1)

    # Find timestamp corresponding to time 0sec of video
    try:
        timestamp_df = pd.read_csv(timestamp_filename, nrows=1)
    except FileNotFoundError:
        print("Could not find file: " + timestamp_filename)
        sys.exit(1)
    except PermissionError:
        print("Could not access file: " + timestamp_filename)
        sys.exit(2)
    timestamp = timestamp_df.to_numpy()[0][0]

    # Add time in msec to dataframe
    sec_times = behaviorData['Time'].tolist()
    msec_times_day = []
    # convert to msec, adjust to timestamp
    for sec_time in sec_times:
        msec_time = sec_time*1000
        msec_adjusted = (msec_time + timestamp)
        msec_times_day.append(msec_adjusted)
    behaviorData.insert(0, 'Time (total msec)', msec_times_day)

    return(behaviorData)


def plot_zscore(behaviorData, zplot_filename):
    """Takes a dataframe and creates plot of z-scores for
        each time a select behavior occurs with the avg
        z-score and SEM

        Parameters
        ----------
        behaviorData: pandas dataframe
                contains:
                    Time(total msec), Time(sec), Subject,
                    Behavior, Status
        zplot_filename: string
                name of the output png file

        Returns:
        --------
        zplot_filename: png file
                plot of the avg zscores for behavioral
                occurances
    """
    return
    # built in zscore function?
    # don't pick a baseline, instead use the mean (of the clip) as the baseline
