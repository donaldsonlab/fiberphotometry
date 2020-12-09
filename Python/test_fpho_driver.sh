test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

# Basic setup passes with exit code 0
run test_fpho_setup_goodinput python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 3 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver'
assert_exit_code 0
assert_in_stdout 'testing_Summary.csv'
assert_stdout

# # Basic setup passes with exit code 0
run test_fpho_setup_goodinput_2fiber python Python/fpho_ftest_driver.py --input_filename Python/SampleData/2fiberSignal.csv --output_filename testing2 --n_fibers 2 --f1greencol 3 --f2greencol 5 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver'
assert_exit_code 0
assert_in_stdout 'testing2_Summary.csv'
assert_stdout

# Test excel output success
run test_fpho_setup_goodinput python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 3 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver' --write_xlsx True
assert_exit_code 0
assert_in_stdout 'testing_Summary.xlsx'
assert_stdout

# Test bad f1green column  input
run test_fpho_setup_badinput python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 2 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver'
assert_exit_code 1

# Test mismatched input: 2 columns but no f2green
run test_fpho_setup_badinput2 python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 2 --f1greencol 2 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver'
assert_exit_code 1

# Test that exit code = 0 for raw signal
run test_plotrawsig_success python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 3 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver' --plot_raw_signal
assert_exit_code 0

# Test that exit code = 0 for iso
run test_plotiso_success python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 3 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver' --plot_iso_fit
assert_exit_code 0

# Test that exit code = 0 for plotting fitted exp
run test_plotfitexp_success python Python/fpho_ftest_driver.py --input_filename Python/SampleData/1fiberSignal.csv --output_filename testing --n_fibers 1 --f1greencol 3 --animal_ID 1 --exp_date 2020-10-10 --exp_desc 'testing the driver' --plot_fit_exp
assert_exit_code 0

