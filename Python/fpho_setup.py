"""Library of functions for fpho_driver
    * import_fpho_data - saves data from csv in lists
    * raw_signal_trace - plots raw signal from fpho data
    * fit_exp - finds fitted exponent
    * plot_fitted_exp - plots 1 fiber normalized fitted exponenent
    * plot_isosbestic_norm - plots 1 fiber normalized isosbestic fit
"""

# Claire to-do: Add warning message when columns are different lengths

import sys
from statistics import mean
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit
import csv

driver_version = 'v2.0'


def import_fpho_data(input_filename, output_filename,
                     n_fibers, f1greencol,
                     animal_ID, exp_date, exp_desc,
                     f2greencol=None,
                     write_xlsx=False):
    """Takes a file name, returns a dataframe of parsed data

        Parameters
        ----------
        input_filename: string
                The path to the CSV file
        output_filename: string
                name for output file
        n_fibers: integer
                indicating 1 or 2 fiber input data
        f1greencol: integer
                f1green column index
        f2greencol: integer
                f2green column index
                default = None
        animal_ID: integer
                unique animal ID #
        exp_date: YYYY_MM_DD
                date data was gathered
        exp_desc: string
                brief description of data

       Returns:
        --------
        twofiber_fdata: pandas dataframe
                containing f1GreenIso, f1GreenRed, f1GreenGreen,
                           f2GreenIso, f2GreenRed, f2GreenGreen,
                           f1RedIso, f1RedRed, f1RedGreen,
                           f2RedIso, f2RedRed, f2RedGreen,
                           fTimeIso, fTimeRed, fTimeGreen,
                           animal_ID, exp_date, exp_desc

        onefiber_fdata: pandas dataframe
                containing f1GreenIso, f1GreenRed, f1GreenGreen,
                           f1RedIso, f1RedRed, f1RedGreen,
                           fTimeIso, fTimeRed, fTimeGreen,
                           animal_ID, exp_date, exp_desc
        * Note: only one of these will be returned, depending
                on if data is for one or two fiber
        """

    # Open file, catch errors
    try:
        file = open(input_filename, 'r')
        header = None
    except FileNotFoundError:
        print("Could not find file: " + input_filename)
        sys.exit(1)
    except PermissionError:
        print("Could not access file: " + input_filename)
        sys.exit(2)

    # Get number of columns in input data
    for line in file:
        if header is None:
            header = line
            continue
        columns = line.rstrip().replace(',', ' ').split(' ')
        break
    n_columns = len(columns)

    # Change None string to None keyword
    if f2greencol == "None":
        f2greencol = None
    else:
        f2greencol = f2greencol

    # Catch error: number of fibers not integer
    try:
        n_fibers = int(n_fibers)
    except ValueError:
        print("Error: Invalid input for number of fibers."
              + "Please use integer input to indicate "
              + "number of fibers represented in input data.\n")
        sys.exit(1)

    # Catch error: number of fibers not integer 1 or 2
    if n_fibers not in [1, 2]:
        print("Error: Integer entered for number of "
              + "fibers represented in dataset <"
              + str(n_fibers) + "> was invalid."
              + " Please enter 1 or 2 in integer format")
        sys.exit(1)

    # Catch error: f1green col entry not integer
    try:
        f1greencol = int(f1greencol)
    except ValueError:
        print("\nError: f1green column index not entered as integer")
        sys.exit(1)

    # Catch error: f1green col entry 3 or 4
    if f1greencol not in [3, 4]:
        print("\nError: Integer entered for f1Green column index <"
              + str(f1greencol) + "> was invalid."
              + " Please enter 3 or 4 in integer format\n")
        sys.exit(1)

    if f1greencol > n_columns:
        print("\nColumn index for f1green is not a valid column index. "
              + "Input data contains ", n_columns, " columns.\n")
        sys.exit

    # Catch error: Mismatched entries - 2 fibers but info for one
    if(n_fibers == 2 and f2greencol is None):
        print("\nError: Indicated 2 fibers in input data "
              + "but did not provide column index for f2Green data. "
              + "Check the config.yml file for mistmatched inputs.\n")
        sys.exit(1)

    # Catch error: Mismatched entries - 1 fiber but info for 2
    if(n_fibers == 1 and f2greencol is not None):
        print("\nError: Indicated 1 fiber in input data "
              + "but provided column index for f2Green data. "
              + "Check config.yml file for mismatched inputs.\n")
        sys.exit(1)

    if f1greencol == 3:
        f1redcol = 4
    else:
        f1redcol = 3

    if f2greencol is not None:

        # Catch error: f2green col entry not integer
        try:
            f2greencol = int(f2greencol)
        except ValueError:
            print("\nError: f2green column index not entered as integer")
            sys.exit(1)

        if f2greencol > n_columns:
            print("\nColumn index for f2green is not a valid column index. "
                  + "Input data contains", n_columns, "columns.\n")
            sys.exit(1)

        # Catch error: f1green col entry 5 or 6
        if f2greencol not in [5, 6]:
            print("\nError: Integer entered for f2Green column index <"
                  + str(f2greencol) + "> was invalid."
                  + " Please enter 5 or 6 in integer format")
            sys.exit(1)

        # Assign f2red column index based on f2green
        if f2greencol == 5:
            f2redcol = 6
        else:
            f2redcol = 5

    fTime = []
    f1Red = []
    f1Green = []
    f2Red = []
    f2Green = []

    for line in file:
        if header is None:
            header = line
            continue
        # Read in each line
        # Must be separated by single space or comma
        columns = line.rstrip().replace(",", " ").split(' ')
        fTime.append(float(columns[0]))
        f1Red.append(float(columns[f1redcol-1]))
        f1Green.append(float(columns[f1greencol-1]))
        if n_fibers == 2:
            f2Red.append(float(columns[f2redcol-1]))
            f2Green.append(float(columns[f2greencol-1]))

    file.close()

    # Trim first ~5sec from data
    f1Green = f1Green[250:]
    f1Red = f1Red[250:]
    f2Green = f2Green[250:]
    f2Red = f2Red[250:]
    fTime = fTime[250:]

    # De-interleave
    offset1 = f1Green[0::3]  # takes every 3rd element starting from 0
    offset2 = f1Green[1::3]
    offset3 = f1Green[2::3]
    meanoffsets = [mean(offset1), mean(offset2), mean(offset3)]

    # Green has highest signal (GcAMP)
    # Order: green(470), red(560), iso(415)
    greenIdX = meanoffsets.index(max(meanoffsets))
    redIdX = greenIdX+1
    isoIdX = greenIdX+2

    # Assigning correct rows to colors
    # First fiber, green
    f1GreenIso = f1Green[greenIdX::3]
    f1GreenRed = f1Green[redIdX::3]
    f1GreenGreen = f1Green[isoIdX::3]

    # First fiber, red
    f1RedIso = f1Red[greenIdX::3]
    f1RedRed = f1Red[redIdX::3]
    f1RedGreen = f1Red[isoIdX::3]

    # Sorting time by color
    fTimeIso = fTime[greenIdX::3]
    fTimeRed = fTime[redIdX::3]
    fTimeGreen = fTime[isoIdX::3]

    if n_fibers == 2:
        # Second fiber, green
        f2GreenIso = f2Green[greenIdX::3]
        f2GreenRed = f2Green[redIdX::3]
        f2GreenGreen = f2Green[isoIdX::3]

        # Second fiber, red
        f2RedIso = f2Red[greenIdX::3]
        f2RedRed = f2Red[redIdX::3]
        f2RedGreen = f2Red[isoIdX::3]

        # Create list of all column names
        colnames = ['f1GreenIso', 'f1GreenRed', 'f1GreenGreen',
                    'f1RedIso', 'f1RedGreen', 'f1RedRed',
                    'f2GreenIso', 'f2GreenRed', 'f2GreenGreen',
                    'f2RedIso', 'f2RedGreen', 'f2RedRed',
                    'fTimeIso', 'fTimeRed', 'fTimeGreen']

        # Set arbitrarily large column length
        collength = 100**10

        # Find minimum column length by comparing
        # last value to length of current column.
        # Use to crop lists in output dataframe

        for name in colnames:
            collength = min(collength, len(eval(name)))

        # Everything into a dictionary
        twofiber_dict = {'f1GreenIso': [f1GreenIso],
                         'f1GreenRed': [f1GreenRed],
                         'f1GreenGreen': [f1GreenGreen],
                         'f2GreenIso': [f2GreenIso],
                         'f2GreenRed': [f2GreenRed],
                         'f2GreenGreen': [f2GreenGreen],
                         'f1RedIso': [f1RedIso],
                         'f1RedRed': [f1RedRed],
                         'f1RedGreen': [f1RedGreen],
                         'f2RedIso': [f2RedIso],
                         'f2RedRed': [f2RedRed],
                         'f2RedGreen': [f2RedGreen],
                         'fTimeIso': [fTimeIso],
                         'fTimeRed': [fTimeRed],
                         'fTimeGreen': [fTimeGreen],
                         'animalID': [animal_ID],
                         'date': [exp_date],
                         'description': [exp_desc]}

        # Dictionary to dataframe
        twofiber_fdata = pd.DataFrame.from_dict(twofiber_dict)

        # Dataframe to output csv
        output_csv = output_filename + '_Summary.csv'
        twofiber_fdata.to_csv(output_csv, index=None, na_rep='')
        print('Output CSV written to ' + output_csv)

        if write_xlsx is True:
            output_xlsx = output_filename + '_Summary.xlsx'
            twofiber_fdata.to_excel(output_xlsx, index=False)
            print('Output excel file written to ' + "output_xlsx")

        return twofiber_fdata

    else:

        # Create list of all column names
        colnames = ['f1GreenIso', 'f1GreenRed', 'f1GreenGreen',
                    'f1RedIso', 'f1RedGreen', 'f1RedRed',
                    'fTimeIso', 'fTimeRed', 'fTimeGreen']

        # Set arbitrarily large column length
        collength = 100**10

        # Find minimum column length. Use to crop lists in output dataframe
        for name in colnames:
            collength = min(collength, len(eval(name)))

        # Everything into a dictionary
        onefiber_dict = {'f1GreenIso': [f1GreenIso[0:collength]],
                         'f1GreenRed': [f1GreenRed[0:collength]],
                         'f1GreenGreen': [f1GreenGreen[0:collength]],
                         'f1RedIso': [f1RedIso[0:collength]],
                         'f1RedRed': [f1RedRed[0:collength]],
                         'f1RedGreen': [f1RedGreen[0:collength]],
                         'fTimeIso': [fTimeIso[0:collength]],
                         'fTimeRed': [fTimeRed[0:collength]],
                         'fTimeGreen': [fTimeGreen[0:collength]],
                         'animalID': [animal_ID],
                         'date': [exp_date],
                         'description': [exp_desc]}

        # Dictionary to dataframe
        onefiber_fdata = pd.DataFrame.from_dict(onefiber_dict)
        print(onefiber_fdata)

        # Dataframe to output csv
        output_csv = output_filename + '_Summary.csv'
        onefiber_fdata.to_csv(output_csv, index=False)
        print('Output CSV written to ' + output_csv)

        if write_xlsx is True:
            output_xlsx = output_filename + '_Summary.xlsx'
            onefiber_fdata.to_excel(output_xlsx, index=False)
            print('Output excel file written to ' + output_xlsx)

        return onefiber_fdata


def raw_signal_trace(fpho_dataframe, output_filename, data_row_index=0):
    """Creates a plot of the raw signal traces
    Parameters
    ----------
    fpho_dataframe: pandas dataframe
                    contains parsed fiberphotometry data
    output_filename: string
                    output png name
    data_row_index: optional integer
                    row containing data to plot

    Returns:
    --------
    output_filename: PNG
                     Plot of data
    """
    # renamed for simplicity
    df = fpho_dataframe

    # Get user input for what to plot
    channel_input = input("----------\n"
                          + "What channel(s) would you like to plot?\n"
                          + "\nOptions are f1Red, f2Red, f1Green, f2Green."
                          + "\n\nIf plotting multiple channels,"
                          + " please separate with a space or comma."
                          + "\n----------\n"
                          + "Selection: ")

    # Make a list of user inputs
    if ',' in channel_input:
        channel_list = channel_input.split(',')
    else:
        channel_list = channel_input.split(' ')

    # quick for loop to catch input error -- input not found in column names
    for channel in channel_list:
        col = df.columns.str.contains(pat=str(channel))
        if not any(col):
            print("Could not find entries for channels you'd like to plot"
                  + " in the dataframe column names."
                  + " You entered <" + channel + "> and the options are "
                  + str(list(df.columns)))
            print('Please restart...\n')
            sys.exit(1)

    # Replace user input with actual column name
    for channel in channel_list:

        if 'f1Red' in str(channel):
            channels = ["f1RedRed"]
            time_col = 'fTimeRed'
            l_color = "r"
        if 'f2Red' in str(channel):
            channels = ["f2RedRed"]
            time_col = 'fTimeRed'
            l_color = "r"
        if 'f1Green' in str(channel):
            channels = ["f1GreenGreen", "f1GreenIso"]
            time_col = 'fTimeGreen'
            l_color = "g"
        if 'f2Green' in str(channel):
            channels = ["f2GreenGreen", "f2GreenIso"]
            time_col = 'fTimeGreen'
            l_color = "g"

        fig = plt.figure(figsize=(7*len(channels), 6),
                         facecolor='w',
                         edgecolor='k',
                         dpi=300)

        for i in range(0, len(channels)):

            channel_data = df[channels[i]].values[data_row_index]
            time_data = df[time_col].values[data_row_index]

            # Initialize plot, add data and title
            ax = fig.add_subplot(1, len(channels), 1+i)
            ax.plot(time_data, channel_data, color=l_color)
            ax.set_title(str(channels[i]))

            # Remove top and right borders
            plt.gca().spines['right'].set_color('none')
            plt.gca().spines['top'].set_color('none')

        # outputs raw sig plot as png file
        rawsig_file_name = output_filename + '_RawSignal_' + channel + '.png'
        plt.savefig(rawsig_file_name, bbox_inches='tight')
        plt.close()


def plot_isosbestic_norm(fpho_dataframe, output_filename):
    """Creates a plot normalizing 1 fiber data to the isosbestic
        Parameters
        ----------
        fpho_dataframe: string
                pandas dataframe
        output_filename: string
                name for output file
        Returns:
        --------
        output_filename_f1GreenNorm.png
        & output_filename_f1RedNorm.png: png files
                containing the normalized plot for each fluorophore
    """

    # Open dataframe
    # Check for Name Error and Permission Error exceptions
    try:
        df = fpho_dataframe
    except NameError:
        print('No ' + fpho_dataframe + ' data frame found')
        sys.exit(1)
    except PermissionError:
        print('Unable to access data frame ' + fpho_dataframe)
        sys.exit(1)

    # Initialize lists for the fluorophores and time
    f1GreenIso = []
    f1GreenGreen = []
    f1GreenTime = []

    f1RedIso = []
    f1RedRed = []
    f1RedTime = []

    # Define columns
    greenIso_col = "f1GreenIso"
    greenGreen_col = "f1GreenGreen"
    greenTime_col = "fTimeGreen"
    redIso_col = "f1RedIso"
    redRed_col = "f1RedRed"
    redTime_col = "fTimeRed"

    # Read through each line of the dataframe
    # Append the isosbectic, fluorophore and time data to their
    # respective vectors, depending on color
    f1GreenIso = df[greenIso_col].values[0]
    f1GreenGreen = df[greenGreen_col].values[0]
    f1GreenTime = df[greenTime_col].values[0]
    f1RedIso = df[redIso_col].values[0]
    f1RedRed = df[redRed_col].values[0]
    f1RedTime = df[redTime_col].values[0]

    # Make sure the iso and color vectors have the same number
    # of values. If not, then trim off the last few values
    # from the longer vector
    if len(f1GreenIso) > len(f1GreenGreen):
        n = len(f1GreenIso) - len(f1GreenGreen)
        del f1GreenIso[-n:]
    elif len(f1GreenIso) < len(f1GreenGreen):
        n = len(f1GreenGreen) - len(f1GreenIso)
        del f1GreenGreen[-n:]

    if len(f1RedIso) > len(f1RedRed):
        n = len(f1RedIso) - len(f1RedRed)
        del f1RedIso[-n:]
    elif len(f1RedIso) < len(f1RedRed):
        n = len(f1RedRed) - len(f1RedIso)
        del f1RedRed[-n:]

    # Get coefficients for normalized fit
    regGreen = np.polyfit(f1GreenIso, f1GreenGreen, 1)
    aGreen = regGreen[0]
    bGreen = regGreen[1]

    regRed = np.polyfit(f1RedIso, f1RedRed, 1)
    aRed = regRed[0]
    bRed = regRed[1]

    # Use the coefficients to create a control fit
    controlFitGreen = []
    for value in f1GreenIso:
        controlFitGreen.append(aGreen * value + bGreen)

    controlFitRed = []
    for value in f1RedIso:
        controlFitRed.append(aRed * value + bRed)

    # Normalize the fluorophore data using the control fit
    normDataGreen = []
    for i in range(len(f1GreenGreen)):
        normDataGreen.append((f1GreenGreen[i]
                              - controlFitGreen[i]) / controlFitGreen[i])

    normDataRed = []
    for i in range(len(f1RedRed)):
        normDataRed.append((f1RedRed[i] - controlFitRed[i]) / controlFitRed[i])

    # Make sure the normalized data vector and the time
    # vector have the same number of values. If not, then
    # trim off the last few values from the longer vector
    if len(f1GreenTime) > len(normDataGreen):
        n = len(f1GreenTime) - len(normDataGreen)
        del f1GreenTime[-n:]
    elif len(f1GreenTime) < len(normDataGreen):
        n = len(normDataGreen) - len(f1GreenTime)
        del normDataGreen[-n:]

    if len(f1RedTime) > len(normDataRed):
        n = len(f1RedTime) - len(normDataRed)
        del f1RedTime[-n:]
    elif len(f1RedTime) < len(normDataRed):
        n = len(normDataRed) - len(f1RedTime)
        del normDataRed[-n:]

    # Plot the data for green
    plt.plot(f1GreenTime, normDataGreen)
    plt.title('Green Normalized to Isosbestic')

    # Save the plot in a png file
    green_iso_plot_name = output_filename + '_f1GreenNormIso.png'
    figGreen = plt.savefig(green_iso_plot_name)
    plt.close(figGreen)

    # Plot the data for red
    plt.plot(f1RedTime, normDataRed)
    plt.title('Red Normalized to Isosbestic')

    # Save the plot in a png file
    red_iso_plot_name = output_filename + '_f1RedNormIso.png'
    figRed = plt.savefig(red_iso_plot_name)
    plt.close(figRed)


def fit_exp(values, a, b, c, d):
    """Transforms data into an exponential function
        of the form y=A*exp(-B*X)+C*exp(-D*x)

        Parameters
        ----------
        values: list
                data
        a, b, c, d: integers or floats
                estimates for the parameter values of
                A, B, C and D
    """

    values = np.array(values)

    return a * np.exp(b * values) + c * np.exp(d * values)


def plot_fitted_exp(fpho_dataframe, output_filename):
    """Creates a plot normalizing 1 fiber data to an
        exponential of the form y=A*exp(-B*X)+C*exp(-D*x)

        Parameters
        ----------
        fpho_dataframe: string
                pandas dataframe
        output_filename: string
                name for output csv
        Returns:
        --------
        output_filename_f1GreenNormExp.png
        & output_filename_f1RedNormExp.png: png files
                containing the normalized plot for each fluorophore
    """

    # Open dataframe
    # Check for Name Error and Permission Error exceptions
    try:
        df = fpho_dataframe
    except NameError:
        print('No ' + fpho_dataframe + ' data frame found')
        sys.exit(1)
    except PermissionError:
        print('Unable to access data frame ' + fpho_dataframe)
        sys.exit(1)

    # Initialize lists for the fluorophores and time
    f1GreenGreen = []
    f1GreenTime = []

    f1RedRed = []
    f1RedTime = []

    # Define columns
    greenGreen_col = "f1GreenGreen"
    greenTime_col = "fTimeGreen"
    redRed_col = "f1RedRed"
    redTime_col = "fTimeRed"

    # Read through each line of the dataframe
    # Append the fluorophore and time data to their
    # respective vectors, depending on color
    f1GreenGreen = df[greenGreen_col].values[0]
    f1GreenTime = df[greenTime_col].values[0]
    f1RedRed = df[redRed_col].values[0]
    f1RedTime = df[redTime_col].values[0]

    # Make sure the time and color vectors have the same number
    # of values. If not, then trim off the last few values
    # from the longer vector
    if len(f1GreenTime) > len(f1GreenGreen):
        n = len(f1GreenTime) - len(f1GreenGreen)
        del f1GreenTime[-n:]
    elif len(f1GreenTime) < len(f1GreenGreen):
        n = len(f1GreenGreen) - len(f1GreenTime)
        del f1GreenGreen[-n:]

    if len(f1RedTime) > len(f1RedRed):
        n = len(f1RedTime) - len(f1RedRed)
        del f1RedTime[-n:]
    elif len(f1RedTime) < len(f1RedRed):
        n = len(f1RedRed) - len(f1RedTime)
        del f1RedRed[-n:]

    # Initialize the time data to 0 by subracting each value
    # by the first value
    timeG = []
    for i in range(len(f1GreenTime)):
        timeG.append(f1GreenTime[i] - f1GreenTime[0])

    timeR = []
    for i in range(len(f1RedTime)):
        timeR.append(f1RedTime[i] - f1RedTime[0])

    # Get coefficients for normalized fit using first guesses
    # for the coefficients - B and D (the second and fourth
    # inputs for p0) must be negative, while A and C (the
    # first and third inputs for p0) must be positive
    popt, pcov = curve_fit(fit_exp, timeG, f1GreenGreen,
                           p0=(1.0, -0.001, 1.0, -0.001), maxfev=500000)

    AG = popt[0]  # A value
    BG = popt[1]  # B value
    CG = popt[2]  # C value
    DG = popt[3]  # D value

    popt, pcov = curve_fit(fit_exp, timeR, f1RedRed,
                           p0=(1.0, -0.001, 1.0, -0.001), maxfev=500000)

    AR = popt[0]  # A value
    BR = popt[1]  # B value
    CR = popt[2]  # C value
    DR = popt[3]  # D value

    # Generate fit line using calculated coefficients
    fitGreen = fit_exp(timeG, AG, BG, CG, DG)
    fitRed = fit_exp(timeR, AR, BR, CR, DR)

    # Plot the data for green
    plt.plot(timeG, f1GreenGreen)
    plt.plot(timeG, fitGreen)
    plt.xlabel('Time')
    plt.ylabel('Fluorescence')
    plt.title('Green Normalized to Exponential')

    # Save the plot in a png file
    green_exp_plot_name = output_filename + '_f1GreenNormExp.png'
    figGreen = plt.savefig(green_exp_plot_name)
    plt.close(figGreen)

    # Plot the data for red
    plt.plot(timeR, f1RedRed)
    plt.plot(timeR, fitRed)
    plt.xlabel('Time')
    plt.ylabel('Fluorescence')
    plt.title('Red Normalized to Exponential')

    # Save the plot in a png file
    red_exp_plot_name = output_filename + '_f1RedNormExp.png'
    figRed = plt.savefig(red_exp_plot_name)
    plt.close(figRed)
