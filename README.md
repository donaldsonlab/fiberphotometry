# Donaldson Lab Fiberphotometry
> This project is for performing analysis on animal fiberphotemetry and behavior data 

In order to use this code you must have collected fiberphotometry data and behavior data collected using the behavior coding software BORIS (https://boris.readthedocs.io/en/latest/#behavioral-observation-research-interactive-software-boris-user-guide). This project currently generates plots marking behavioral occurances on raw fluoresence data (behavior_onefiber_wdriver and behavior_twofiber_wdriver), and produces a Z-score plot (Zscore_wdriver) which graphs average Z-score and SEM for all stacked behavioral occurances. BORIS_format is used to parse and format raw output for use with the rest of the code. The behavior_driver is the only script that must be run by the user (but all scripts must be downloaded). 

## Installation

OS X & Linux:

```sh
git clone https://github.com/donaldsonlab/fiberphotometry.git
```

## To Use the Code
1. Obtain `fiberphotometry data` (msec/day) 
2. Score behavior using BOIRS with the events recorded in `seconds`
3. Download raw data from behavior scoring using BORIS by clicking: `observations -> export events -> tabular events -> select observations -> save as csv`
3. Download all scripts in repository
4. Run the `behavior_driver` which has a user interface that will guide you through the rest of the inputs

## Release History

* v1.0
    * ADD: `behavior_driver.m`
    * ADD: `behavior_twofiber_wdriver.m`
    * ADD: `Zscore_wdriver.m`
* v1.1
    * ADD: `BORIS_format.m`
    * ADD: `behavior_onefiber_wdriver.m`
    * CHANGE: files updated to be compatible with change
* v1.2
    * CHANGE: Error messages added
    * ADD: baseline printed on graph in `Zscore_wdriver.m`
    * CHANGE: baseline selected from menu in `Zscore_wdriver.m`
* v1.3
   * CHANGE: `behavior_driver` runs `BORIS_format` (so they do not need to be run separately) 
   * CHANGE: user inputs now formatted in inputdlg windows
