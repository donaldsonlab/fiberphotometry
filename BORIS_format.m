%% Script to take BORIS .csv output and format it for fiber fluorescence analysis with behavior_driver script
% Written 9/16/20 by Lisa Hiura
% Editted 9/16/20 by Anna McTigue

borisformat_verion = 'v1.2';

%% Imports Data
% % Import behavior Data
prompt = 'Enter the BORIS output file name \n';
behavior_file_name = input(prompt, 's'); 
behaviorData = readtable(behavior_file_name);

%drop the first 10 lines because they are extraneous
behaviorData(1:10,:) = [];

%drop columns for media file, total length, FPS, subject, behavioral
%category, and comment
behaviorData(:,[2:5,7:8]) = [];

%Assign meaningful column names
behaviorData.Properties.VariableNames = {'Time_in_Video' 'Behavior' 'Status'};

%drop rows that have 'STOP' as Status to treat all behaviors as point
%events 
behaviorData(ismember(behaviorData.Status,'STOP'),:)=[];

%transform time in sec to msec
behaviorData.Time_in_Video = behaviorData.Time_in_Video ./ 1000;
 
%move the Status column over 1 to the right (should now be column 4)
behaviorData(:,4) = [ behaviorData(:,3)];
 
%prompt time offset to align behavior data with fluorescence data
prompt = 'Enter the timestamp file name \n';
timestamp_file_name = input(prompt, 's'); 
timestamps = readtable(timestamp_file_name);
time_offset = timestamps{1,1};

%fix column names
behaviorData.Properties.VariableNames = {'Time_in_Video' 'Behavior' 'corrected_time' 'Status'};

%add offset to the behavioral timestamps
%behaviorData.Var9 = behaviorData.ObservationId+time_offset;
behaviorData.corrected_time = behaviorData.Time_in_Video+time_offset;

