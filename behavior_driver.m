%% Creates Z-score plot for all behaviors 

%% Imports Data
% Import behavior Data
prompt = 'Enter the behavior data file name \n';
behavior_file_name = input(prompt, 's'); 
behaviorData = readtable(behavior_file_name);

% To hard code behavior data use this: 
% behavior_file_name = 
% behaviorData = readtable(behavior_file_name);


% Import fluoresence Data
prompt = 'Enter the fluoresence data file name \n';
f_file_name = input(prompt, 's');
fData = readtable(f_file_name); 

% To hard code flouresence data use this: 
% f_file_name = 'FiberPhoSig2020-06-10T15_09_21.csv';
% fData = readtable(f_file_name);

% Import behaviors to analyze
behaviors_input = input('What behaviors would you like analyzed? \n','s');
behaviors = regexp(behaviors_input,', ','split');

% To hard code behaviors use this:
% behaviors_input = 'Nose to Nose, Side by Side';
% behaviors = regexp(behaviors_input,', ','split');


%% Runs behavior_data_twofiber script on each behavior
for i = 1:length(behaviors)
    behavior_name = behaviors(i);
    behavior_data_twofiber;
    Zscore;
    clearvars -except fData behaviorData behaviors behavior_file_name
end
