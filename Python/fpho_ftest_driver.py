"""This file runs the functions in the fpho_setup library """

import argparse
import sys
import fpho_setup

def main():
    """Runs functions in fpho_setup, asks for what analysis to perform

    Parameters
    ----------
    input_filename: string
            Name of input file containing fiber photometry data

    output_filename: string
            Name you'd like for the output CSV file. Should include
            file path if different than current file

    animal_ID: int
               Number of the animal corresponding to fluoresence data

    exp_date: YYYY-MM-DD
              Date of exp/date data was gathered

    exp_desc: string
              Brief explantation of experiment/what
              type of information data contains

    plot_raw_signal: boolean
                     optional plot of raw data for a
                     particular fiber and color

    plot_iso_fit: boolean
                  optional isosbestic plot

    plot_fit_exp: boolean
                  optional fitted exponent plot

    Returns
    -------
    Pandas dataframe of parsed fiber photometry data
    Writes an output CSV to specified file name
    """
    # use with config.txt
    # run bash command: python fpho_driver.py @config.txt
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')

    parser = argparse.ArgumentParser(description=('Parse fiber photometry data'
                                                  + 'to prepare for analyses'))

    parser.add_argument('--input_filename',
                        dest='input_filename',
                        type=str,
                        required=True,
                        help='Name of input file as string')

    parser.add_argument('--output_filename',
                        dest='output_filename',
                        type=str,
                        required=True,
                        help='Name for output file as string')

    parser.add_argument('--n_fibers',
                        dest='n_fibers',
                        type=int,
                        required=True,
                        help='Number of fibers in input data')

    parser.add_argument('--f1greencol',
                        dest='f1greencol',
                        type=int,
                        required=True,
                        help='column index of f1green')

    parser.add_argument('--f2greencol',
                        dest='f2greencol',
                        type=int,
                        default=None,
                        required=False,
                        help='column index of f1green')                        

    parser.add_argument('--animal_ID',
                        dest='animal_ID',
                        type=int,
                        required=True,
                        help='Animal number for fluroesence data')

    parser.add_argument('--exp_date',
                        dest='exp_date',
                        type=str,
                        required=True,
                        help='Date of experiment as YYYY-MM-DD')

    parser.add_argument('--exp_desc',
                        dest='exp_desc',
                        type=str,
                        required=True,
                        help='Brief description for context')

    parser.add_argument('--write_xlsx',
                        dest='write_xlsx',
                        type=bool,
                        default=False,
                        help="add --write_xlsx to command line")

    parser.add_argument('--plot_raw_signal',
                        dest='plot_raw_signal',
                        action='store_true',
                        help='add --plot_raw_signal to command line')

    parser.add_argument('--plot_iso_fit',
                        dest='plot_iso_fit',
                        action='store_true',
                        help='add --plot_iso_fit to command line')

    parser.add_argument('--plot_fit_exp',
                        dest='plot_fit_exp',
                        action='store_true',
                        help='add --plot_fit_exp to command line')

    args = parser.parse_args()

    # Generate the dataframe with data
    fpho_df = fpho_setup.import_fpho_data(input_filename=args.input_filename,
                                          output_filename=args.output_filename,
                                          write_xlsx=args.write_xlsx,
                                          n_fibers=args.n_fibers,
                                          f1greencol=args.f1greencol,
                                          f2greencol=args.f2greencol,
                                          animal_ID=args.animal_ID,
                                          exp_date=args.exp_date,
                                          exp_desc=args.exp_desc)

    # Plot raw signal if specified in commandline
    if args.plot_raw_signal:
        sys.stdin = open("Python/ftests_fpho_setup.txt")
        fpho_setup.raw_signal_trace(fpho_dataframe=fpho_df,
                                    output_filename=args.output_filename)
        

    # Prints isosbestic fit if specified
    if args.plot_iso_fit:
        sys.stdin = open("Python/ftests_fpho_setup.txt")
        fpho_setup.plot_isosbestic_norm(fpho_dataframe=fpho_df,
                                        output_filename=args.output_filename)

    # Prints fitted exponent if specified
    if args.plot_fit_exp:
        sys.stdin = open("Python/ftests_fpho_setup.txt")
        fpho_setup.plot_fitted_exp(fpho_dataframe=fpho_df,
                                   output_filename=args.output_filename)


if __name__ == '__main__':
    main()
