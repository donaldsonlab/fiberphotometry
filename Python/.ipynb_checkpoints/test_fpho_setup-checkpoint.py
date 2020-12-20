"""Unit testing for functions in fpho_setup

TO DO: Needs documentation and comments

"""
import fpho_setup
import unittest
import random
import sys
import pandas as pd
import os.path
from os import path


class TestFphoSetup(unittest.TestCase):

    def test_import_fpho_data(self):
        df = fpho_setup.import_fpho_data(input_filename='Python/TestData'
                                         '/1FiberTesting.csv',
                                         output_filename='my_file_name',
                                         n_fibers=1, f1greencol=4,
                                         animal_ID='vole1',
                                         exp_date='2020-09-01',
                                         exp_desc="testing",
                                         f2greencol=None,
                                         write_xlsx=False)

        test_green_iso = [1640.48859543818, 1640.90076030412]
        self.assertEqual(df['f1GreenIso'].values[0], test_green_iso)

        test_green_green = [1511.23969587835, 1511.07482993197]
        self.assertEqual(df['f1GreenGreen'].values[0], test_green_green)

        test_red_iso = [1536.2730469085, 1536.54499614098]
        self.assertEqual(df['f1RedIso'].values[0], test_red_iso)

    def test_import_fpho_data_errors(self):
        with self.assertRaises(SystemExit) as cm:
            fpho_setup.import_fpho_data(input_filename='TestData/1Fdlkjf',
                                        output_filename='my_file_name',
                                        n_fibers=1, f1greencol=3,
                                        animal_ID='vole1',
                                        exp_date='2020-09-01',
                                        exp_desc="testing",
                                        f2greencol=None,
                                        write_xlsx=False)
        self.assertEqual(cm.exception.code, 1)

    def test_fit_exp(self):
        fit = fpho_setup.fit_exp([0, 0, 0, 0, 0], 1, 1, 1, 1)
        self.assertEqual(2.0, fit[0])
        self.assertEqual(2.0, fit[3])

        fit = fpho_setup.fit_exp([1, 5, 8, 10], 1, -1, 1, -1)
        self.assertEqual(0.7357588823428847, fit[0])
        self.assertEqual(9.079985952496971e-05, fit[3])

    def test_raw_signal_trace(self):
        df_test = fpho_setup.import_fpho_data(input_filename='Python/TestData'
                                              '/1FiberTesting.csv',
                                              output_filename='my_file_name',
                                              n_fibers=1, f1greencol=3,
                                              animal_ID='vole1',
                                              exp_date='2020-09-01',
                                              exp_desc="testing",
                                              f2greencol=None,
                                              write_xlsx=False)
        # Must use the user input: f1Red
        fpho_setup.raw_signal_trace(fpho_dataframe=df_test,
                                    output_filename='testing_unit',
                                    data_row_index=0)
        self.assertTrue(path.exists('testing_unit_RawSignal_f1Red.png'))

    def test_raw_signal_trace_errors(self):
        df_test = fpho_setup.import_fpho_data(input_filename='Python/TestData'
                                              '/1FiberTesting.csv',
                                              output_filename='my_file_name',
                                              n_fibers=1, f1greencol=3,
                                              animal_ID='vole1',
                                              exp_date='2020-09-01',
                                              exp_desc="testing",
                                              f2greencol=None,
                                              write_xlsx=False)
        with self.assertRaises(SystemExit) as cm:
            # Use the user input: userinputfailure
            fpho_setup.raw_signal_trace(fpho_dataframe=df_test,
                                        output_filename='testing_unit.png',
                                        data_row_index=0)
        self.assertEqual(cm.exception.code, 1)

    def test_plot_isosbestic_norm(self):
        df_test = fpho_setup.import_fpho_data(input_filename='Python/TestData'
                                              '/1FiberTesting.csv',
                                              output_filename='my_file_name',
                                              n_fibers=1, f1greencol=3,
                                              animal_ID='vole1',
                                              exp_date='2020-09-01',
                                              exp_desc="testing",
                                              f2greencol=None,
                                              write_xlsx=False)
        fpho_setup.plot_isosbestic_norm(fpho_dataframe=df_test,
                                        output_filename='my_file_name')
        self.assertTrue(path.exists('my_file_name_f1GreenNormIso.png'))
        self.assertTrue(path.exists('my_file_name_f1RedNormIso.png'))

    def test_plot_fitted_exp(self):
        df_test = fpho_setup.import_fpho_data(input_filename='Python/'
                                              'SampleData/1fiberSignal.csv',
                                              output_filename='my_file_name',
                                              n_fibers=1, f1greencol=3,
                                              animal_ID='vole1',
                                              exp_date='2020-09-01',
                                              exp_desc="testing",
                                              f2greencol=None,
                                              write_xlsx=False)
        fpho_setup.plot_fitted_exp(fpho_dataframe=df_test,
                                   output_filename='my_file_name')
        self.assertTrue(path.exists('my_file_name_f1GreenNormExp.png'))
        self.assertTrue(path.exists('my_file_name_f1RedNormExp.png'))


if __name__ == '__main__':
    unittest.main()
