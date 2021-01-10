"""This file runs the functions in the fpho_setup library"""
import argparse
import sys
import fpho_setup
import yaml
import behavior_setup
import pandas as pd


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

    # Generate the dataframe with data
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
                                              config['exp_desc']),
                                          write_xlsx=(
                                               config['write_xlsx']))
    else:
        fpho_df=pd.read_csv(config['output_filename'] + '_Summary.csv')
    # Plot raw signal if specified
    if config['plot_raw_signal'] is True:
        fpho_df=fpho_setup.raw_signal_trace(fpho_df)

    # Plots fitted exponent if specified
    if config['plot_fit_exp'] is True:
        fpho_data=fpho_setup.plot_fitted_exp(fpho_df,                                   output_filename=config['output_filename'],                         signals=config['all_signals'],                                     references=config['all_references'])

    # Imports behavior data if specified
    behaviorData = pd.DataFrame()
    if config['import_behavior'] is True:
        behaviorData = behavior_setup.import_behavior_data(
                                            config['BORIS_file'],
                                            config['timestamp_file'])

    # Plots z-score analysis of behavior if specified
    if config['plot_zscore'] is True:
        behavior_setup.plot_zscore(behaviorData, config['output_filename'])


if __name__ == '__main__':
    main()
