"""Library of functions for synchrony analysis
    * within_trial_pearsons
"""

import sys
import scipy.stats as ss
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.ndimage.filters import uniform_filter1d


def within_trial_pearsons(df, key, channels):
    results={}
    for channel in channels:
        our_channels = [col for col in df.columns if channel + ' final normalized' in col]
        if len(our_channels) < 1:
            print('data must be normalized before running a correlation')
            sys.exit()
        sig1 = df[our_channels[0]]
        sig2 = df[our_channels[1]]
        time = df['fTimeGreen']
        for i in range(50, 100, 10):
            sig1smooth = ss.zscore(uniform_filter1d(sig1, size=i))
            sig2smooth = ss.zscore(uniform_filter1d(sig2, size=i))
            fig = make_subplots(rows=1, cols=2)
            fig.add_trace(
                go.Scatter(
                x=sig1smooth,
                y=sig2smooth,
                mode="markers",
                name ='correlation',
                showlegend=False), row=1, col=2
            )
            fig.add_trace(
                go.Scatter(
                x=time,
                y=sig2smooth,
                mode="lines",
                name = "sig2",
                showlegend=False), row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                x=time,
                y=sig1smooth,
                mode="lines",
                name='sig1',
                showlegend=False), row=1, col=1
            )
            
        [r, p] = ss.pearsonr(sig1smooth, sig2smooth)
        results[channel]=[r, p]
        
    print('Pearsons')
    return results

def within_trial_crossCorr(df, channels):
    results={}
    for channel in channels:
        our_channels = [col for col in df.columns if channel + ' final normalized' in col]
        if len(our_channels) < 1:
            print('data must be normalized before running a correlation')
            sys.exit()
        sig1 = df[our_channels[0]]
        sig2 = df[our_channels[1]]
        
        
        sig1 = (sig1 - np.mean(sig1)) / (np.std(sig1) * len(sig1))
        sig2 = (sig2 - np.mean(sig2)) /  np.std(sig2)
        
        r = np.correlate(sig1, sig2)
        results[channel]=[r]
        
    print('Cross correlation')
    return results


def behavior_specific_pearsons(df, file, channels, behs):

    results={}
    for channel in channels:
        our_channels = [chan + ' final normalized' for chan in channel ]
        channel_names=channel[0]+ ' vs ' +channel[1]
        if len(our_channels) < 1:
            print('data must be normalized before running a correlation')
            sys.exit()
        results[channel_names]={} 
        sig1=[]
        sig2=[]
        for beh in behs:
            behaviorname=''
            flag=False
            for name in beh:
                behaviorname= behaviorname + ' ,' + name
                if name in df.columns:
                    flag=True
            if flag:
                behaviorSlice=df.loc[:,beh]
                TrueTimes = behaviorSlice.any(axis=1);
                corDf=pd.concat([df['fTimeGreen'], df[our_channels[0]], df[our_channels[1]], TrueTimes], axis=1)
                corDf.columns = ['fTimeGreen', our_channels[0], our_channels[1], 'TrueTimes']
                
                sig1=corDf[corDf.TrueTimes == True][our_channels[0]]
                sig2=corDf[corDf.TrueTimes == True][our_channels[1]]
                sig1=ss.zscore(corDf[corDf.TrueTimes == True][our_channels[0]])
                sig2=ss.zscore(corDf[corDf.TrueTimes == True][our_channels[1]])
                
                #difsig1=[sig1.iloc[i+1]-sig1.iloc[i] for i in range(len(sig1)-1)]
                #difsig2=[sig2.iloc[i+1]-sig2.iloc[i] for i in range(len(sig2)-1)]
                #sig1 = ss.zscore(uniform_filter1d(sig1, size=50))
                #sig2 = ss.zscore(uniform_filter1d(sig2, size=50))

                time=corDf[corDf.TrueTimes == True]['fTimeGreen']
                fig = make_subplots(rows=1, cols=2)
                fig.add_trace(
                    go.Scatter(
                    x=sig1,
                    y=sig2,
                    mode="markers",
                    name =behaviorname,
                    showlegend=False), row=1, col=2
                )
                fig.add_trace(
                    go.Scatter(
                    x=time,
                    y=sig1,
                    mode="lines",
                    line=go.scatter.Line(color='rgb(255,100,150)'),
                    name =channel[0],
                    showlegend=False), row=1, col=1
                )
                fig.add_trace(
                    go.Scatter(
                    x=time,
                    y=sig2,
                    mode="lines",
                    line=go.scatter.Line(color='rgba(100,0,200, .6)'),
                    name = channel[1],
                    showlegend=False), row=1, col=1
                )
                fig.update_yaxes(
                    #title_text = "Interbrain Correlation (PCC)",
                    showgrid=True,
                    #showline=True, linewidth=2, linecolor='black',
                )
                fig.update_layout(
                        title=channel_names + ' while' + behaviorname + ' for ' + file
                        )
                fig.update_xaxes(title_text=channel[0]+ ' zscore')
                fig.update_yaxes(title_text=channel[1] + ' zscore')
                
                fig.update_xaxes(title_text='Time (s)', col=1, row=1)
                fig.update_yaxes(title_text='Zscore', col=1, row=1)

                fig.show()
                #fig.write_image('together_seperate1.pdf')
                [r, p] = ss.pearsonr(sig1, sig2)
            else:
                [r, p]=['na', 'na']
                print(behaviorname + ' not found in this trial')
            results[channel_names][behaviorname]=[r, p]  
    return results
    
def plot_FFT(df, key, channels):
    from scipy.fft import fft, fftfreq
    for channel in channels:
        our_channels = [col for col in df.columns if channel + ' final normalized' in col]
    sig1 = df[our_channels[0]]
    sig2 = df[our_channels[1]]
    time = df['fTimeGreen']
    # Number of sample points
    N = len(sig1)
    # sample spacing
    T = time.iloc[-1]/(N*300)
    y1 = fft(sig1.tolist())
    y1=2.0/N * np.abs(y1[0:N//2]),
    y2 = fft(sig2.tolist())
    y2=2.0/N * np.abs(y2[0:N//2]),
    xf = fftfreq(N, T)[:N//2]
    
    y1binned=np.arange(0, np.floor(xf[-1]))
    y2binned=np.arange(0, np.floor(xf[-1]))
    xbinned=np.arange(0, np.floor(xf[-1]), 1)
    counter = 0
    idx=-1
    y1tot=0
    y2tot=0
    for i in xf:
        idx=idx+1
        if i < counter+1:
            y1tot=y1tot+y1[0][idx]
            y2tot=y2tot+y2[0][idx]
        else:
            y1binned[counter]=y1tot
            y2binned[counter]=y2tot
            counter=counter+1
            y1tot=0
            y2tot=0

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(
        go.Scatter(
        x=xf,
        y=y1[0],
        mode="lines",
        name ='T= ' + str(T),
        showlegend=True), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(
        x=xf,
        y=y2[0],
        mode="lines",
        name ='y2',
        showlegend=True), row=1, col=1
    )
    fig.add_trace(
         go.Scatter(
         x=xbinned,
         y=y1binned,
         mode="lines",
         name ='y1binned',
         showlegend=True), row=1, col=1
     )
    fig.add_trace(
         go.Scatter(
         x=xbinned,
         y=y2binned,
         mode="lines",
         name ='y2binned',
         showlegend=True), row=1, col=1
     ) 
    fig.show()
    