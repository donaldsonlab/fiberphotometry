"""Library of functions for fpho_driver
    * import_fpho_data - saves data from csv in lists
    * raw_signal_trace - plots raw signal from fpho data
    * fit_exp - finds fitted exponent
    * plot_fitted_exp - plots 1 fiber normalized fitted exponenent
    * plot_isosbestic_norm - plots 1 fiber normalized isosbestic fit
"""

import sys
from statistics import mean
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.optimize import curve_fit
import csv
import plotly.graph_objects as go

driver_version = 'v2.0'


def import_fpho_data(input_filename, output_filename,                          f1greencol, 
                     f1redcol, f2greencol, f2redcol,
                     animal_ID, exp_date, exp_desc,
                     write_xlsx):
    """Takes a file name, returns a dataframe of parsed data

        Parameters
        ----------
        input_filename: string
                The path to the CSV file
        output_filename: string
                name for output file
        f1greencol: integer
                f1green column index
        f1redcol: integer
                f1red column index
        f2greencol: integer or 'none'
                f2green column index
        f2redcol: integer or 'none'
                f2red column index        
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

    # Change None string to None keyword
    if f2greencol == "None":
        f2greencol = None
       
    if f2redcol == "None":
        f2redcol = None

    # Catch error: f1green col entry not integer
    try:
        f1greencol = int(f1greencol)
        f1redcol = int(f1redcol)
    except ValueError:
        print("\nError: f1green or f1red column index not entered as integer")
        sys.exit(1)

    if (f1greencol == f1redcol) or (f1greencol == f2greencol) or (f1greencol == f2redcol) or (f2greencol == f1redcol) or (f2greencol == f2redcol) or (f1redcol == f2redcol):
        print("\nThe same column index has been assigned to two different colors or fibers.\n")
        sys.exit

    if f2greencol is not None:

        # Catch error: f2green col entry not integer
        try:
            f2greencol = int(f2greencol)
        except ValueError:
            print("\nError: f2green column index not entered as integer")
            sys.exit(1)
            
        if f2greencol == f2redcol:
            print("\nThe same column index is listed for f2green and f2red. "
                  + "Input data contains", n_columns, "columns.\n")
            sys.exit(1)
    
        # Open file, catch errors
    try:
        file = pd.read_csv(input_filename)
    except FileNotFoundError:
        print("Could not find file: " + input_filename)
        sys.exit(1)
    except PermissionError:
        print("Could not access file: " + input_filename)
        sys.exit(2)
    
    #start time at zero and converto minutes
    file['Timestamp']=(file['Timestamp']-file['Timestamp'][0])/60000
    length=len(file['Flags'])-1
    extras=length%3
    min=int((length-extras)/3)
    #create a dictionary with parsed data    
    data_dict = { 'animalID': [animal_ID], 'date': [exp_date],
             'description': [exp_desc],
             'fTimeIso': file[file["Flags"] == 17].iloc[0:min, 1].values.tolist(),
             'fTimeRed': file[file["Flags"] == 20].iloc[0:min, 1].values.tolist(),
             'fTimeGreen': file[file["Flags"] == 18].iloc[0:min, 1].values.tolist(),
             'f1GreenGreen': file[file["Flags"] == 18].iloc[0:min, f1greencol].values.tolist(),
             'f1GreenIso': file[file["Flags"] == 17].iloc[0:min, f1greencol].values.tolist(),
             'f1RedRed':file[file["Flags"] == 20].iloc[0:min, f1redcol].values.tolist(),
             'f1RedIso': file[file["Flags"] == 17].iloc[0:min, f1redcol].values.tolist()}
  
    #Add additional columns if 2 fiber
    if f2greencol != None:
        
        data_dict['f2GreenGreen'] = file[file["Flags"] == 18].iloc[0:min, f2greencol].values.tolist()
        data_dict['f2GreenIso'] = file[file["Flags"] == 17].iloc[0:min, f2greencol].values.tolist()
        data_dict['f2RedRed'] = file[file["Flags"] == 20].iloc[0:min, f2redcol].values.tolist()
        data_dict['f2RedIso'] = file[file["Flags"] == 17].iloc[0:min, f2redcol].values.tolist()
   
    fdata=pd.DataFrame(columns=data_dict.keys())
    # Dictionary to dataframe
    for n in data_dict:
        fdata[n]=fdata[n].astype('object')
        fdata.at[0,n]=data_dict[n]
 
    # Dataframe to output csv
    if write_xlsx is True:
        output_csv = output_filename + '_Summary.csv'
        fdata.to_csv(output_csv, index=None, na_rep='')
        print('Output CSV written to ' + output_csv)

    


    return fdata

   
def raw_signal_trace(fdata):
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=2, cols=2)
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata['f1GreenGreen'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            showlegend=False), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'].at[0],
            y=fdata['f1GreenIso'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            showlegend=False), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeRed'].at[0],
            y=fdata['f1RedRed'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Red"),
            showlegend=False), row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'].at[0],
            y=fdata['f1RedIso'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Violet"),
            showlegend=False), row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata['f2GreenGreen'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            showlegend=False), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'].at[0],
            y=fdata['f2GreenIso'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            showlegend=False), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeRed'].at[0],
            y=fdata['f2RedRed'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Red"),
            showlegend=False), row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'].at[0],
            y=fdata['f2RedIso'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Violet"),
            showlegend=False), row=2, col=2
    )
    fig.show()
    return


def plot_fitted_exp(fdata, output_filename, signals, references):
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
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
    # Get coefficients for normalized fit using first guesses
    # for the coefficients - B and D (the second and fourth
    # inputs for p0) must be negative, while A and C (the
    # first and third inputs for p0) must be positive
    
    for i in range(len(signals)):
        popt, pcov = curve_fit(fit_exp, fdata['fTimeGreen'].at[0], fdata[signals[i]].at[0], p0=(1.0, 0, 1.0, 0), bounds=(0,np.inf))

        AS = popt[0]  # A value
        BS = popt[1]  # B value
        CS = popt[2]  # C value
        DS = popt[3]  # D value

        popt, pcov = curve_fit(fit_exp, fdata['fTimeGreen'].at[0], fdata[references[i]].at[0], p0=(1.0, 0, 1.0, 0), bounds=(0,np.inf))

        AR = popt[0]  # A value
        BR = popt[1]  # B value
        CR = popt[2]  # C value
        DR = popt[3]  # D value

        # Generate fit line using calculated coefficients
        fitSig = fit_exp(fdata['fTimeGreen'].at[0], AS, BS, CS, DS)
        fitRef = fit_exp(fdata['fTimeGreen'].at[0], AR, BR, CR, DR)
        normedSig=[k/j for k,j in zip(fdata[signals[i]].at[0], fitSig)]
        normedRef=[k/j for k,j in zip(fdata[references[i]].at[0], fitSig)] 
        
        normedToReference=normalize_to_reference(normedSig, normedRef)
        
        fdata.loc[:,signals[i] + ' expfit']=['na']
        fdata.at[0, signals[i] + ' expfit']=fitSig
        fdata.loc[:,signals[i] + ' expfit parameters']=['na']
        fdata.at[0, signals[i] + ' expfit parameters']=[AS, BS, CS, DS]
        fdata.loc[:,signals[i] + ' normed to exp']=['na']
        fdata.at[0,signals[i] + ' normed to exp']=normedSig
        fdata.loc[:,references[i] + ' expfit']=['na']
        fdata.at[0,references[i] + ' expfit']=fitRef
        fdata.loc[:,references[i] + ' expfit parameters']=['na']
        fdata.at[0,references[i] + ' expfit parameters']=[AR, BR, CR, DR]
        fdata.loc[:,references[i] + ' normed to exp']=['na']
        fdata.at[0,references[i] + ' normed to exp']=normedRef
        fdata.loc[:,references[i] + ' fitted to ' + signals[i]]=['na']
        fdata.at[0,references[i] + ' fitted to ' + signals[i]]=normedToReference[0]
        fdata.loc[:,references[i] + ' linfit parameters']=['na']
        fdata.at[0,references[i] + ' linfit parameters']=normedToReference[2]
        fdata.loc[:,signals[i] + ' final normalized'] = ['na']
        fdata.at[0,signals[i] + ' final normalized'] =normedToReference[1]
        
        fig = make_subplots(rows=3, cols=2, subplot_titles=("Biexponential Fitted to Signal", "Signal Normalized to Biexponential", "Biexponential Fitted to Ref", "Reference Normalized to Biexponential", "Reference Linearly Fitted to Signal", "Final Normalized Signal"))
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[signals[i]].at[0],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            name ='Signal:' + signals[i],
            text = 'Signal',
            showlegend=True), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[signals[i] + ' expfit'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Purple"),
            text='Biexponential fitted to Signal',
            showlegend=False), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[signals[i] + ' normed to exp'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            text = 'Signal Normalized to Biexponential',
            showlegend=False), row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[references[i]].at[0],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            name='Reference:' + references[i],
            text='Reference',
            showlegend=True), row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[references[i] + ' expfit'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Purple"),
            text='Biexponential fit to Reference',
            showlegend=False), row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[references[i] + ' normed to exp'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            text='Reference Normalized to Biexponential',
            showlegend=False), row=2, col=2
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[signals[i] + ' normed to exp'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            text='Signal Normalized to Biexponential',
            showlegend=False), row=3, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[references[i] + ' fitted to ' + signals[i]].at[0],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            text='Reference linearly scaled to signal',
            showlegend=False), row=3, col=1
            
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'].at[0],
            y=fdata[signals[i] + ' final normalized'].at[0],
            mode="lines",
            line=go.scatter.Line(color="Pink"), 
            text='Final Normalized Signal',
            showlegend=False), row=3, col=2
            
        )
        fig.update_layout(
            title="Normalizing " + signals[i],
            xaxis_title='Time',
        )
        fig.show()
    output_xlsx = output_filename + '_Summary.csv'
    fdata.to_csv(output_xlsx, index=False)
    print('Summary file has been updated')
    return fdata


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

    return a * np.exp(-b * values) + c * np.exp(-d * values)


def normalize_to_reference(signal, reference):
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

    regGreen = np.polyfit(reference, signal, 1)
    a = regGreen[0]
    b = regGreen[1]

    # Use the coefficients to create a control fit
    fittedReference = []
    for value in reference:
        fittedReference.append(a * value + b)

    # Normalize the fluorophore data using the control fit
    normalized = []
    for i in range(len(fittedReference)):
        normalized.append((signal[i]/ fittedReference[i]))
                          
    return [fittedReference, normalized, [a,b]]

