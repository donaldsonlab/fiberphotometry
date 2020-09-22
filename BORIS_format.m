%% Script to take BORIS .csv output and format it for fiber fluorescence analysis with behavior_driver script
% Written 9/16/20 by Lisa Hiura
% Editted 9/22/20 by Anna McTigue

borisformat_verion = 'v1.3';

%% Imports Data
% Import Raw BORIS Data
prompt = {'Enter the BORIS output file name'};
dlgtitle = 'Input BORIS Data File ';
dims = [1 35];
BORIS_file_name_cell = inputdlg(prompt,dlgtitle,dims);
BORIS_file_name = BORIS_file_name_cell{1,1};
behaviorData = readtable(BORIS_file_name);

% Drop the first 10 lines because they are extraneous
behaviorData(1:10,:) = [];

% Drop columns for media file, total length, FPS, subject, behavioral
% category, and comment
behaviorData(:,[2:5,7:8]) = [];

% Assign meaningful column names
behaviorData.Properties.VariableNames = {'Time_in_Video' 'Behavior' 'Status'};

% Drop rows that have 'STOP' as Status to treat all behaviors as point
% events 
behaviorData(ismember(behaviorData.Status,'STOP'),:)=[];

% Transform time in sec to msec
behaviorData.Time_in_Video = behaviorData.Time_in_Video ./ 1000;
 
% Move the Status column over 1 to the right (should now be column 4)
behaviorData(:,4) = [behaviorData(:,3)];
 
% Prompt time offset to align behavior data with fluorescence data
prompt = {'Enter the timestamp file name'};
dlgtitle = 'Input Timestamp File ';
dims = [1 35];
timestamp_file_name_cell = inputdlg(prompt,dlgtitle,dims);
timestamp_file_name = timestamp_file_name_cell{1,1};
timestamps = readtable(timestamp_file_name);
time_offset = timestamps{1,1};

% Fix column names
behaviorData.Properties.VariableNames = {'Time_in_Video' 'Behavior' 'corrected_time' 'Status'};

% Add offset to the behavioral timestamps
% BehaviorData.Var9 = behaviorData.ObservationId+time_offset;
behaviorData.corrected_time = behaviorData.Time_in_Video+time_offset;

