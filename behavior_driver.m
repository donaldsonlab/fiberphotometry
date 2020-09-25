%% Creates Z-score plot for all behaviors 
% updated 9/22/20 by Anna

driver_version = 'v1.4';

%% To Hard code files/behaviors use this
% % Behavior file: 
% behavior_file_name = '2020-04-09T16_04_47.csv';
% behaviorData = readtable(behavior_file_name);
% 
% % Fluoresence file:
% f_file_name = 'Test2020-04-09T16_04_46.csv';
% fData = readtable(f_file_name);
% 
% % Behaviors: 
% behaviors_input = 'Autogroom';
% behaviors = regexp(behaviors_input,', ','split');
% 
% % Animal number:
% animal_num = 'test';

%% Converts BORIS Output to behaviorData variable
dlgTitle    = 'Behavior Data Format';
dlgQuestion = 'Have you already converted BORIS output to behaviorData?';
choice = questdlg(dlgQuestion,dlgTitle,'Yes','No', 'Yes');
tf = strcmp(choice,'Yes');
if tf == 0 % if choice is 'No'
    BORIS_format;
end

%% Imports Data
% Import behavior Data
if ~(exist('behaviorData','var'))
    prompt = {'Enter the behavior data file name'};
    dlgtitle = 'Input Behavior Data File ';
    dims = [1 35];
    behavior_file_name_cell = inputdlg(prompt,dlgtitle,dims);
    behavior_file_name = behavior_file_name_cell{1,1};
    behaviorData = readtable(behavior_file_name);
end

% Import fluoresence Data
    prompt = {'Enter the fluoresence data file name'};
    dlgtitle = 'Input Fluoresence Data File ';
    dims = [1 35];
    f_file_name_cell = inputdlg(prompt,dlgtitle,dims);
    f_file_name = f_file_name_cell{1,1};
    fData = readtable(f_file_name); 

% Import behaviors to analyze
unique_behaviors = unique(table2array(behaviorData(:,2)));
[behavior_indx,ok] = listdlg('Promptstring',{'Pick the behaviors to be ' ...
    'analyzed'}, 'Liststring', unique_behaviors);
if ok == 0 % catch no selection error
    fprintf('**Please make a selection from the behaviors list to continue** \n');
end
behaviors = [];
% puts selected behaviors into behaviors array
for i = 1:(length(behavior_indx))
    behaviors = [behaviors, unique_behaviors(behavior_indx(i))];
end
% Asks for animal number
prompt = {'What is the animal number?'};
dlgtitle = 'Input Animal Number';
dims = [1 35];
animal_num_cell = inputdlg(prompt,dlgtitle,dims);
animal_num = animal_num_cell{1,1};
fData = readtable(f_file_name);

%% Runs behavior_data_twofiber script and z-score script on each behavior
for i = 1:length(behaviors)

    %% Runs behavior plots
    behavior_name = behaviors(i);
    
    % prompts user to select one or two fiber script
    list = {'One fiber','Two fiber'};
    [fiber_indx,tf1] = listdlg('PromptString',{'How many fibers did you use?'}...
        ,'ListString',list);
    if tf1 == 0 % catch no selection error
        error('Error: Make a selection from the channels list to continue')
    end
    if fiber_indx == 1
        behavior_onefiber_wdriver;
    end
    if fiber_indx == 2
        behavior_twofiber_wdriver;
    end
    

    %% Plots Z-score 
    % Asks what channel(s) to analyze
     if fiber_indx == 1
        list = {'fGreenisosbestic','fGreenred','fGreengreen','fRedisosbestic',...
            'fRedred','fRedgreen'};
        [zscore_indx,tf] = listdlg('PromptString',{'Choose one or more channels to' ...
            ' analyze for ' + string(behavior_name)}...
            ,'ListString',list);
        channels = {fGreenisosbestic,fGreenred,fGreengreen,fRedisosbestic,...
            fRedred,fRedgreen};
        if tf == 0 % catch no selection error
            error('Error: make a selection from the channels list to continue');
        end
     end
     
     if fiber_indx == 2
        list = {'fGreenLisosbestic','fGreenLred','fGreenLgreen','fGreenRisosbestic',...
            'fGreenRred','fGreenRgreen','fRedLisosbestic','fRedLred','fRedLgreen',...
            'fRedRisosbestic','fRedRred','fRedRgreen'};
        [zscore_indx,tf] = listdlg('PromptString',{'Choose one or more channels to' ...
            ' analyze for ' + string(behavior_name)}...
            ,'ListString',list);
        channels = {fGreenLisosbestic,fGreenLred,fGreenLgreen,fGreenRisosbestic,...
            fGreenRred,fGreenRgreen,fRedLisosbestic,fRedLred,fRedLgreen,...
            fRedRisosbestic,fRedRred,fRedRgreen};
        if tf == 0 % catch no selection error
            error('Error: make a selection from the channels list to continue');
        end
     end
    
    % Creates z-score plot for each selected channel
    for i = 1:length(zscore_indx)
        % Saves channel array in channel and channel name in channel_name
        channel = cell2mat(channels(zscore_indx(i)));
        channel_name = list(zscore_indx(i));
        % Finds correct time array to use for selected channel
        if zscore_indx(i) == 1||4||7||10 % isosbestic
            fTimeChannel = fTimeIsosbestic;
        elseif zscore_indx(i) == 2||5||8||11 % red
            fTimeChannel = fTimeRed;
        elseif zscore_indx(i) == 3||6||9||12 % green
            fTimeChannel = fTimeGreen;
        else
            error('Error: could not assign time to channel');
        end  
        % Runs script
        Zscore_wdriver;
    end
    
    %% Clears variables for next run
    clearvars -except fData behaviorData behaviors behavior_file_name ...
        animal_num unique_behaviors baseline_start_sec baseline_stop_sec
end
