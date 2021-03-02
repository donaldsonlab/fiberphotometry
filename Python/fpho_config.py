"""This file runs the functions in the fpho_setup library"""
import argparse
import sys
import yaml
import pandas as pd
import fpho_setup
import behavior_setup
import correlation_setup
from os import path


def main():
    """Runs functions in fpho_setup, processes config.yml

    Parameters
    ----------
    config.yml
        To use this driver, update the config.yml file, then
        run the following bash command:
        python fpho_config.py --config config.yml

    Returns
    -------
        Pandas dataframe of parsed fiber photometry data
        Writes an output CSV/XLXS to specified file name
        Outputs specified plots and analysis
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()

    # Opens and reads config file to process
    f = open(args.config, 'r')
    config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    
    #initializes a dictionary, that will hold a dataframe for each fiberphotometry file
    all_data={}
      
    # Generate the dataframe with new data
    if config['import_new'] is True:
        fpho_df = fpho_setup.import_fpho_data(input_filename=(
                                              config['input_filename']),
                                          output_filename=(
                                              config['output_filename']),
                                          f1greencol=(
                                              config['f1greencol']),
                                          f1redcol=(
                                              config['f1redcol']),
                                          f2greencol=(
                                              config['f2greencol']),
                                          f2redcol=(
                                              config['f2redcol']),
                                          animal_ID=(
                                              config['animal_ID']),
                                          exp_date=(
                                              config['exp_date']),
                                          exp_desc=(
                                              config['exp_desc']))
        if config['write_xlsx'] is True:          
            output_xlsx = config['output_filename'] + '_Summary.csv'
            if path.exists(output_xlsx):
                answer=input('Are you sure you want to overwrite'+output_xlsx+'(y or n)')
                if answer != 'y':
                    print('Did not overwrite' + output_xlsx)
                    print('Change output_filename or write_xlsx value and rerun')
                    sys.exit()
            
            fpho_df.to_csv(output_xlsx, index=False)
            print('Summary CSV file has been saved to ' + config['output_filename'] + '_Summary.csv')
        
        #Imports behavior data associated with the newly imported file if specified
        if config['import_behavior'] is True:
            fpho_df = behavior_setup.import_behavior_data(
                                                config['BORIS_file'],
                                                fpho_df)
            if config['write_xlsx'] is True:
                output_xlsx = key
                if path.exists(output_xlsx):
                    answer=input('Are you sure you want to overwrite'+output_xlsx+'(y or n)')
                    if answer != 'y':
                            print('Did not overwrite' + output_xlsx)
                            print('Change output_filename or write_xlsx value and rerun')
                            sys.exit()
                else:
                    fpho_df.to_csv(output_xlsx, index=False)
                    print('Behavior data has been added to the summary file')
        
        all_data['output_xlsx']=fpho_df
        
    #reads in one or more dataframes and assigns them to a dictionary using the file name as the key    
    if config['reload_data'] is True:
        for file in config['reload_filenames']:
            fpho_df=pd.read_csv(file) 
            all_data[file]=fpho_df
            print('data was reloaded from', file)

    #Runs plots and analyses as specified on all fiberpho data sets
    for key in all_data:
        fpho_df= all_data[key]
        output_xlsx = key
        # Plot raw signal if specified
        if config['plot_raw_signal'] is True:
            fpho_setup.raw_signal_trace(fpho_df, key)

        # Normalizes signals of interest and plots normalization process
        if config['normalize_data'] is True:
            fpho_df=fpho_setup.plot_fitted_exp(fpho_df, key,                      
                                                 signals=config['all_signals'],                                    
                                                 references=config['all_references'])
            if config['write_xlsx'] is True:
                fpho_df.to_csv(output_xlsx, index=False)
                print(key, 'has been updated to include normalized data')

        if config['plot_behavior'] is True:
            behavior_setup.plot_behavior(fpho_df, key, config['all_signals'])

        #Plot the discrete fourier transform of you're channels of interest 
        if config['fourier_transform'] is True:
            correlation_setup.plot_FFT(fpho_df, key, config['channels'])

        # Plots z-score analysis of behavior if specified
        if config['plot_zscore'] is True:
            behavior_setup.plot_zscore(fpho_df, key, config['all_signals'], config['zscore_behs'])

        if config['within_trial_pearsons'] is True:
            print(correlation_setup.within_trial_pearsons(fpho_df, key, config['channels']))

        if config['behavior_specific_pearsons'] is True:
            print(correlation_setup.behavior_specific_pearsons(fpho_df, key, config['channels'], config['behaviors'])) 
        
        all_data[key]=fpho_df

if __name__ == '__main__':
    main()
