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
from scipy import stats
import csv
import plotly.graph_objects as go

driver_version = 'v4.0'


def import_fpho_data(input_filename, output_filename, f1greencol, 
                     f1redcol, f2greencol, f2redcol,
                     animal_ID, exp_date, exp_desc):
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
        sys.exit()

    if (f1greencol == f1redcol) or (f1greencol == f2greencol) or (f1greencol == f2redcol) or (f2greencol == f1redcol) or (f2greencol == f2redcol) or (f1redcol == f2redcol):
        print("\nThe same column index has been assigned to two different colors or fibers.\n")
        sys.exit()

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
    
    # Find min data length
    file['Timestamp']=(file['Timestamp']-file['Timestamp'][0])
    length=len(file['Flags'])-1
    extras=length%3
    min=int((length-extras)/3)-1
    
    # Ensures start index is on green (green flagged as 18)
    start_idx=301 # cut off first ~300 entries
    start_is_not_green = True
    while(start_is_not_green):
        if file["Flags"][start_idx] == 18:
            start_is_not_green = False
        if file["Flags"][start_idx] == 20:
            start_is_not_green = True
            start_idx=start_idx+1
        if file["Flags"][start_idx] == 17:
            start_is_not_green = True
            start_idx=start_idx+1
        
    # Create a dictionary with parsed data
#    data_dict = {'animalID': [animal_ID]*(min-start_idx),
#             'date': [exp_date]*(min-start_idx),
#             'description': [exp_desc]*(min-start_idx),
#             'fTimeIso': file[file["Flags"] == 17].iloc[start_idx:min, 1].values.tolist(),
#             'fTimeRed': file[file["Flags"] == 20].iloc[start_idx:min, 1].values.tolist(),
#             'fTimeGreen': file[file["Flags"] == 18].iloc[start_idx:min, 1].values.tolist(),
#             'f1GreenGreen': file[file["Flags"] == 18].iloc[start_idx:min, f1greencol].values.tolist(),
#             'f1GreenIso': file[file["Flags"] == 17].iloc[start_idx:min, f1greencol].values.tolist(),
#             'f1GreenRed': file[file["Flags"] == 20].iloc[start_idx:min, f1greencol].values.tolist(),
#             'f1RedGreen': file[file["Flags"] == 18].iloc[start_idx:min, f1greencol].values.tolist(),
#             'f1RedRed':file[file["Flags"] == 20].iloc[start_idx:min, f1redcol].values.tolist(),
#             'f1RedIso': file[file["Flags"] == 17].iloc[start_idx:min, f1redcol].values.tolist()}
    
    data_dict = {'animalID': [animal_ID]*(min-start_idx),
                 'date': [exp_date]*(min-start_idx),
                 'description': [exp_desc]*(min-start_idx),
                 'fTimeIso': file[start_idx+2::3].iloc[start_idx:min, 1].values.tolist(),
                 'fTimeRed': file[start_idx+1::3].iloc[start_idx:min, 1].values.tolist(),
                 'fTimeGreen': file[start_idx::3].iloc[start_idx:min, 1].values.tolist(),
                 'f1GreenGreen': file[start_idx::3].iloc[start_idx:min, f1greencol].values.tolist(),
                 'f1GreenIso': file[start_idx+2::3].iloc[start_idx:min, f1greencol].values.tolist(),
                 'f1GreenRed': file[start_idx+1::3].iloc[start_idx:min, f1greencol].values.tolist(),
                 'f1RedGreen': file[start_idx::3].iloc[start_idx:min, f1greencol].values.tolist(),
                 'f1RedRed':file[start_idx+1::3].iloc[start_idx:min, f1redcol].values.tolist(),
                 'f1RedIso': file[start_idx+2::3].iloc[start_idx:min, f1redcol].values.tolist()}

    print(data_dict['fTimeIso'])
    
    # Add additional columns if 2 fiber
    if f2greencol != None:
        data_dict['f2GreenGreen'] = file[start_idx::3].iloc[start_idx:min, f2greencol].values.tolist()
        data_dict['f2GreenIso'] = file[start_idx+2::3].iloc[start_idx:min, f2greencol].values.tolist()
        data_dict['f2GreenRed'] = file[start_idx+1::3].iloc[start_idx:min, f2greencol].values.tolist()
        data_dict['f2RedRed'] = file[start_idx+1::3].iloc[start_idx:min, f2redcol].values.tolist()
        data_dict['f2RedIso'] = file[start_idx+2::3].iloc[start_idx:min, f2redcol].values.tolist()
        data_dict['f2RedGreen'] = file[start_idx::3].iloc[start_idx:min, f2redcol].values.tolist()

# FIX: MAKE INTO NEW FUNCTION (dict, number of jumps)

# Frame Drop Correction
    # if: 1 frame drop
        # drop jump idx frame, match the ones before the jump and after the jump idx
        # all lists in dict need to be the same len (be careful when dropping/replacing the frame, out of time, etc)
    # else: 2 frame drop
    for j in range(0):
        i=0
        jump=0
        jumpIdx=-1
        while i < len(data_dict['f1GreenGreen'])-2:
            distanceFromNext=abs(data_dict['f1GreenGreen'][i] - data_dict['f1GreenGreen'][i+1])
            distanceFromIso=abs(data_dict['f1GreenGreen'][i] - data_dict['f1GreenIso'][i+1])
            if distanceFromNext>distanceFromIso and distanceFromNext>jump:
                jump=distanceFromNext
                jumpIdx=i
            i=i+1

        if jump>0:
            
            #DELETE
            print(jumpIdx)
            
            if abs(data_dict['f1GreenGreen'][jumpIdx] - data_dict['f1GreenIso'][jumpIdx+3]) < abs(data_dict['f1GreenIso'][jumpIdx] - data_dict['f1GreenGreen'][jumpIdx+3]):
                
                #DELETE
                print("if")
                
                temp=data_dict['f1GreenGreen'][jumpIdx+1:]
                data_dict['f1GreenGreen'][jumpIdx+1:]=data_dict['f1GreenIso'][jumpIdx+1:]
                data_dict['f1GreenIso'][jumpIdx+1:]=data_dict['f1GreenRed'][jumpIdx+1:]
                data_dict['f1GreenRed'][jumpIdx+1:]=temp

                temp=data_dict['f1RedIso'][jumpIdx+1:]
                data_dict['f1RedIso'][jumpIdx+1:]=data_dict['f1RedRed'][jumpIdx+1:]
                data_dict['f1RedRed'][jumpIdx+1:]=data_dict['f1RedGreen'][jumpIdx+1:]
                data_dict['f1RedGreen'][jumpIdx+1:]=temp
                
                if f2greencol != None:
                    temp=data_dict['f2GreenGreen'][jumpIdx+1:]
                    data_dict['f2GreenGreen'][jumpIdx+1:]=data_dict['f2GreenIso'][jumpIdx+1:]
                    data_dict['f2GreenIso'][jumpIdx+1:]=data_dict['f2GreenRed'][jumpIdx+1:]
                    data_dict['f2GreenRed'][jumpIdx+1:]=temp

                    temp=data_dict['f2RedIso'][jumpIdx+1:]
                    data_dict['f2RedIso'][jumpIdx+1:]=data_dict['f2RedRed'][jumpIdx+1:]
                    data_dict['f2RedRed'][jumpIdx+1:]=data_dict['f2RedGreen'][jumpIdx+1:]
                    data_dict['f2RedGreen'][jumpIdx+1:]=temp
            else:
                
                #DELETE
                print("else")
                
                temp=data_dict['f1GreenIso'][jumpIdx+1:]
                data_dict['f1GreenIso'][jumpIdx+1:]=data_dict['f1GreenGreen'][jumpIdx+1:]
                data_dict['f1GreenGreen'][jumpIdx+1:]=data_dict['f1GreenRed'][jumpIdx+1:]
                data_dict['f1GreenRed'][jumpIdx+1:]=temp

                temp=data_dict['f1RedRed'][jumpIdx+1:]
                data_dict['f1RedRed'][jumpIdx+1:]=data_dict['f1RedIso'][jumpIdx+1:]
                data_dict['f1RedIso'][jumpIdx+1:]=data_dict['f1RedGreen'][jumpIdx+1:]
                data_dict['f1RedGreen'][jumpIdx+1:]=temp
                
                if f2greencol != None:
                    temp=data_dict['f2GreenIso'][jumpIdx+1:]
                    data_dict['f2GreenIso'][jumpIdx+1:]=data_dict['f2GreenGreen'][jumpIdx+1:]
                    data_dict['f2GreenGreen'][jumpIdx+1:]=data_dict['f2GreenRed'][jumpIdx+1:]
                    data_dict['f2GreenRed'][jumpIdx+1:]=temp

                    temp=data_dict['f2RedRed'][jumpIdx+1:]
                    data_dict['f2RedRed'][jumpIdx+1:]=data_dict['f2RedIso'][jumpIdx+1:]
                    data_dict['f2RedIso'][jumpIdx+1:]=data_dict['f2RedGreen'][jumpIdx+1:]
                    data_dict['f2RedGreen'][jumpIdx+1:]=temp

    fdata=pd.DataFrame.from_dict(data_dict)
    return fdata

   
def raw_signal_trace(fdata, file):
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, vertical_spacing=0.02, x_title="Time (s)", y_title="Fluorescence")
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata['f1GreenGreen'],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            name='f1Green',
            text='f1Green',
            showlegend=False), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'],
            y=fdata['f1GreenIso'],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            name='f1GreenIso',
            text='f1GreenIso',
            showlegend=False), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeRed'],
            y=fdata['f1RedRed'],
            mode="lines",
            line=go.scatter.Line(color="Red"),
            name='f1Red',
            text='f1Red',
            showlegend=False), row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'],
            y=fdata['f1RedIso'],
            mode="lines",
            line=go.scatter.Line(color="Violet"),
            name='f1RedIso',
            text='f1RedIso',
            showlegend=False), row=1, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata['f2GreenGreen'],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            name='f2Green',
            text='f2Green',
            showlegend=False), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'],
            y=fdata['f2GreenIso'],
            mode="lines",
            name='f2GreenIso',
            text='f2GreenIso',
            line=go.scatter.Line(color="Cyan"),
            showlegend=False), row=2, col=1
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeRed'],
            y=fdata['f2RedRed'],
            mode="lines",
            name='f2Red',
            text='f2Red',
            line=go.scatter.Line(color="Red"),
            showlegend=False), row=2, col=2
    )
    fig.add_trace(
        go.Scatter(
            x=fdata['fTimeIso'],
            y=fdata['f2RedIso'],
            mode="lines",
            line=go.scatter.Line(color="Violet"),
            name='f2RedIso',
            text='f2RedIso',
            showlegend=False), row=2, col=2
    )
    fig.update_layout(
        title="Raw Traces from all channels for " + file,
    )
    fig.show()
    return


def plot_fitted_exp(fdata, file, signals, references):
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
        popt, pcov = curve_fit(fit_exp, fdata['fTimeGreen'], fdata[signals[i]], p0=(1.0, 0, 1.0, 0, 0), bounds=(0,np.inf))

        AS = popt[0]  # A value
        BS = popt[1]  # B value
        CS = popt[2]  # C value
        DS = popt[3]  # D value
        ES = popt[4]
        
        popt, pcov = curve_fit(fit_exp, fdata['fTimeGreen'], fdata[references[i]], p0=(1.0, 0, 1.0, 0, 0), bounds=(0,np.inf))

        AR = popt[0]  # A value
        BR = popt[1]  # B value
        CR = popt[2]  # C value
        DR = popt[3]  # D value
        ER = popt[4]       

        # Generate fit line using calculated coefficients
        fitSig = fit_exp(fdata['fTimeGreen'], AS, BS, CS, DS, ES)
        fitRef = fit_exp(fdata['fTimeGreen'], AR, BR, CR, DR, ER)
        
        sigRsquare=np.corrcoef(fdata[signals[i]], fitSig)[0,1]**2
        refRsquare=np.corrcoef(fdata[references[i]], fitRef)[0,1]**2
        print('sig r^2 =', sigRsquare ,'ref r^2 =', refRsquare )
        
        if sigRsquare < .01:
            print('sig r^2 =', sigRsquare)
            print('No exponential decay was detected in ', signals[i])
            print(signals[i] + ' expfit is now the median of ', signals[i])
            AS=0
            BS=0
            CS=0
            DS=0
            ES=np.median(fdata[signals[i]])
            fitSig = fit_exp(fdata['fTimeGreen'], AS, BS, CS, DS, ES)
            
        
        if refRsquare < .001:
            print('ref r^2 =', refRsquare)
            print('No exponential decay was detected in ', references[i])
            print(references[i] + ' expfit is now the median  ', references[i])
            AR=0
            BR=0
            CR=0
            DR=0
            ER= np.median(fdata[references[i]])
            fitRef = fit_exp(fdata['fTimeGreen'], AR, BR, CR, DR, ER)
            
            
        normedSig=[(k/j) for k,j in zip(fdata[signals[i]], fitSig)]
        normedRef=[(k/j) for k,j in zip(fdata[references[i]], fitRef)]      
        
        popt, pcov = curve_fit(lin_fit, normedSig, normedRef, bounds=([0, -5],[np.inf, 5]))
        
        AL =popt[0]
        BL =popt[1]
        
        AdjustedRef=[AL* j + BL for j in normedRef]
        normedToReference=[(k/j) for k,j in zip(normedSig, AdjustedRef)]
        
        fdata.loc[:,signals[i] + ' expfit']=fitSig
        fdata.loc[:,signals[i] + ' expfit parameters']=['na']
        fdata.at[0:4, signals[i] + ' expfit parameters']=['A= ' + str(AS), 'B= ' + str(BS), 'C= ' + str(CS), 'D= ' + str(DS), 'E= ' + str(ES)]
        fdata.loc[:,signals[i] + ' normed to exp']=normedSig
        fdata.loc[:,references[i] + ' expfit']=fitRef
        fdata.loc[:,references[i] + ' expfit parameters']=['na']
        fdata.at[0:4,references[i] + ' expfit parameters']=['A= ' + str(AR), 'B= ' + str(BR), 'C= ' + str(CR), 'D= ' + str(DR), 'E= ' + str(ER)]
        fdata.loc[:,references[i] + ' normed to exp']=normedRef
        fdata.loc[:,references[i] + ' fitted to ' + signals[i]]=AdjustedRef
        fdata.loc[:,references[i] + ' linfit parameters']=['na']
        fdata.at[0:1,references[i] + ' linfit parameters']= ['A= ' + str(AL), 'B= ' + str(BL)]
        fdata.loc[:,signals[i] + ' final normalized'] = normedToReference
        
        fig = make_subplots(rows=3, cols=2, x_title='Time(s)', subplot_titles=("Biexponential Fitted to Signal", "Signal Normalized to Biexponential", "Biexponential Fitted to Ref", "Reference Normalized to Biexponential", "Reference Linearly Fitted to Signal", "Final Normalized Signal"), shared_xaxes=True, vertical_spacing=0.1)
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[signals[i]],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            name ='Signal:' + signals[i],
            text = 'Signal',
            showlegend=False), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[signals[i] + ' expfit'],
            mode="lines",
            line=go.scatter.Line(color="Purple"),
            text='Biexponential fitted to Signal',
            showlegend=False), row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[signals[i] + ' normed to exp'],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            text = 'Signal Normalized to Biexponential',
            showlegend=False), row=1, col=2
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[references[i]],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            name='Reference:' + references[i],
            text='Reference',
            showlegend=False), row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[references[i] + ' expfit'],
            mode="lines",
            line=go.scatter.Line(color="Purple"),
            text='Biexponential fit to Reference',
            showlegend=False), row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[references[i] + ' normed to exp'],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            text='Reference Normalized to Biexponential',
            showlegend=False), row=2, col=2
        )
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[signals[i] + ' normed to exp'],
            mode="lines",
            line=go.scatter.Line(color="Green"),
            text='Signal Normalized to Biexponential',
            showlegend=False), row=3, col=1
        )
        
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[references[i] + ' fitted to ' + signals[i]],
            mode="lines",
            line=go.scatter.Line(color="Cyan"),
            text='Reference linearly scaled to signal',
            showlegend=False), row=3, col=1  
        )
        
        fig.add_trace(
            go.Scatter(
            x=fdata['fTimeGreen'],
            y=fdata[signals[i] + ' final normalized'],
            mode="lines",
            line=go.scatter.Line(color="Pink"), 
            text='Final Normalized Signal',
            showlegend=False), row=3, col=2
            
        )
        fig.update_layout(
            title="Normalizing " + signals[i] + ' for ' + file
        )
        fig.show()

    return fdata


def fit_exp(values, a, b, c, d, e):
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

    return a * np.exp(-b * values) + c * np.exp(-d * values) + e

def lin_fit(values, a, b):

    values = np.array(values)
    
    return a * values + b


def fix_frame_shift(n, data_dict, file):
    i=0
    jump=0
    jumpIdx=-1
    for j in range(n):
        while i < len(data_dict['f1GreenGreen'])-2:
            distanceFromNext=abs(data_dict['f1GreenGreen'][i] - data_dict['f1GreenGreen'][i+1])
            distanceFromIso=abs(data_dict['f1GreenGreen'][i] - data_dict['f1GreenIso'][i+1])
            if distanceFromNext>distanceFromIso and distanceFromNext>jump:
                jump=distanceFromNext
                jumpIdx=i
            i=i+1
        if jump>0:
            if abs(data_dict['f1GreenGreen'][jumpIdx] - data_dict['f1GreenIso'][jumpIdx+1]) < abs(data_dict['f1GreenIso'][jumpIdx] - data_dict['f1GreenGreen'][jumpIdx+1]):
                data_dict['f1GreenGreen'][jumpIdx+1:]=data_dict['f1GreenIso'][jumpIdx+1:]
                data_dict['f1GreenIso'][jumpIdx+1:]=file[file["Flags"] == 20].iloc[jumpIdx+start_idx+1:min, f1greencol].values.tolist()

                data_dict['f1RedIso'][jumpIdx+1:]=data_dict['f1RedRed'][jumpIdx+1:]
                data_dict['f1RedRed'][jumpIdx+1:]=file[file["Flags"] == 18].iloc[jumpIdx+start_idx+1:min, f1redcol].values.tolist() 

                if f2greencol != None:
                    data_dict['f2GreenGreen'][jumpIdx+1:]=data_dict['f2GreenIso'][jumpIdx+1:]
                    data_dict['f2GreenIso'][jumpIdx+1:]=file[file["Flags"] == 20].iloc[jumpIdx+start_idx+1:min, f2greencol].values.tolist()

                    data_dict['f2RedIso'][jumpIdx+1:]=data_dict['f2RedRed'][jumpIdx+1:]
                    data_dict['f2RedRed'][jumpIdx+1:]=file[file["Flags"] == 18].iloc[jumpIdx+start_idx+1:min, f2redcol].values.tolist() 
            else:
                data_dict['f1GreenIso'][jumpIdx+1:]=data_dict['f1GreenGreen'][jumpIdx+1:]
                data_dict['f1GreenGreen'][i+1:]=file[file["Flags"] == 20].iloc[jumpIdx+start_idx+1:min, f1greencol].values.tolist()

                data_dict['f1RedRed'][jumpIdx+1:]=data_dict['f1RedIso'][jumpIdx+1:]
                data_dict['f1RedIso'][jumpIdx+1:]=file[file["Flags"] == 18].iloc[jumpIdx+start_idx+1:min, f1redcol].values.tolist()

                if f2greencol != None:
                    data_dict['f2GreenGreen'][jumpIdx+1:]=data_dict['f2GreenIso'][jumpIdx+1:]
                    data_dict['f2GreenIso'][jumpIdx+1:]=file[file["Flags"] == 20].iloc[jumpIdx+start_idx+1:min, f2greencol].values.tolist()

                    data_dict['f2RedIso'][jumpIdx+1:]=data_dict['f2RedRed'][jumpIdx+1:]
                    data_dict['f2RedRed'][jumpIdx+1:]=file[file["Flags"] == 18].iloc[jumpIdx+start_idx+1:min, f2redcol].values.tolist() 
    return(data_dict)
