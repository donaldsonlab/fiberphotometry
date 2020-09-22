%% Plots zscores for each behavior occurance (Asks for channel)
% UPDATE THIS EACH NEW VERSION (date of update):
zversion = 'v1.2'; 


%% Determines indices of behaviorT, 2sec before, & 5sec after in fTimeChannel

% Determining Baseline
if ~(exist('baseline_start_sec','var')) || ~(exist('baseline_stop_sec','var'))
    baselinelist = {'4-3 seconds before behavior','3-2 seconds before behavior',...
    '2-1 seconds before behavior', '1-0 seconds before behavior'};
    [baseline_indx,tf] = listdlg('PromptString',{'What baseline range would you like to use?'}...
        ,'ListString',baselinelist);
    if tf == 0 % catch no selection error
        error('Error: make a selection of baseline range to continue /n');
    end
    if baseline_indx == 1
        baseline_start_sec = 4;
        baseline_stop_sec = 3; 
    elseif baseline_indx == 2
        baseline_start_sec = 3;
        baseline_stop_sec = 2; 
    elseif baseline_indx == 3
        baseline_start_sec = 2;
        baseline_stop_sec = 1; 
    elseif baseline_indx == 4
        baseline_start_sec = 1;
        baseline_stop_sec = 0; 
    end
end

% Initialize arrays
baseline_start = zeros(1,length(behaviorT)); % # sec before bout (start baseline)
baseline_start_idx = zeros(1,length(behaviorT));
baseline_stop = zeros(1,length(behaviorT)); % # sec before bout (stop baseline)
baseline_stop_idx = zeros(1,length(behaviorT));
ends = zeros(1,length(behaviorT)); 
ends_idx = zeros(1,length(behaviorT));
behaviorIdx = zeros(1,length(behaviorT));

% Sets arrays with respective indices
for i = 1:length(behaviorT)
    %finds index in fTimeChannel that is closest to behaviorT(i)
    [val,idx1]=min(abs(fTimeChannel-behaviorT(i))); 
    behaviorIdx(i)=idx1;
    % start baseline secs before bout (index in fTimeChannel)
    baseline_start(i) = max(behaviorT(i) - (1000 * baseline_start_sec), fTimeChannel(1));
    [val,idx2]=min(abs(fTimeChannel-baseline_start(i)));
    baseline_start_idx(i)=idx2;
    % stop baseline secs before bout (index in fTimeChannel)
    baseline_stop(i) = max(behaviorT(i) - (1000 * baseline_stop_sec), fTimeChannel(1)); 
    [val,idx3]=min(abs(fTimeChannel-baseline_stop(i)));
    baseline_stop_idx(i)=idx3;
    %calculates time 5 seconds after each start bout
    ends(i) = min(fTimeChannel(end),behaviorT(i) + 5000); 
    [val,idx4]=min(abs(fTimeChannel-ends(i)));
    ends_idx(i)=idx4;
end

% std of all fluorescent signal in channel
std_channel = std(channel); 

% adjusts indices so that they are all the same
minlenB = min(ends_idx-baseline_start_idx); % looks at range in indices
for i = 1:length(behaviorT)
    if (ends_idx(i)-baseline_start_idx(i))>minlenB
         ends_idx(i)=baseline_start_idx(i)+minlenB;
    end
end
minlen=min(behaviorIdx-baseline_start_idx);

%% Calculate zscores   

% initialize arrays
f_baseline=zeros(1,minlen+1);
entire_range=zeros(length(behaviorT),minlenB+1); 
zscore=zeros(length(behaviorT),minlenB+1);

% calculates z score for each behavior occurance
for i = 1:length(behaviorT)
    % floursence signal from -2sec to 5sec behavior
    entire_range(i,:) = channel(baseline_start_idx(i):ends_idx(i)).'; 
    % baseline avg calculated as mean from 3 to 2 seconds before behavior
    zscore(i,:) = (entire_range(i,:) - mean(channel((baseline_start_idx(i)):baseline_stop_idx(i)).'))/std_channel;       
end

%% Calculates average zscores for each time point in each bout

zscore_channel_avg = zeros(1,minlenB+1);
for j = 1:minlenB+1
    zscore_channel_avg(j) = mean(zscore(:,j));
end 

%% Standard Error of the Mean 
% calculate standard deviation 
std_zavg = std(zscore);

% calculate standard error
sem_channel = std_zavg/sqrt(length(behaviorT(i)));

%plot avg zscore with shaded std/sem
curve1 = zscore_channel_avg + sem_channel;
curve2 = zscore_channel_avg - sem_channel;
  
curve1 = curve1.';
curve2 = curve2.';

%% Plotting
x = [-3:(8/(minlenB)):+5];  % holds minlenB points between -2 and 5

% prompt = 'What would you like to title your graph? \n';
% graph_title = input(prompt,'s');
graph_title = string(behavior_name) + ' Animal no. '+ animal_num + ...
    ' Channel: ' + channel_name + ' ' + zversion;

figure
% Plots z scores for each behavior bout
for i=1:length(behaviorT)
    hold on
    plot(x,zscore(i,:),'k',0,0.5);
end
% Plots avg z score across all bouts
plot(x,zscore_channel_avg,'LineWidth',4)
xlabel('Time (s)')
ylabel('zscore')
title(graph_title)
hold on
xline(0,':','LineWidth',2);

% SEM lines
plot(x,curve1,'r',0,0.5,'LineWidth',2);
plot(x,curve2,'r',0,0.5,'LineWidth',2);

% Marks baseline range with grey bar
if baseline_start_sec < 4
    basline_range = patch([-baseline_stop_sec -baseline_start_sec -baseline_start_sec ...
        -baseline_stop_sec],[min(ylim) min(ylim) max(ylim) max(ylim)],[17 17 17]/255);
    alpha(.01)
    basline_range.FaceAlpha = 0.2;
end


%% Print Z-score Summary Values
max_zscore = num2str(max(zscore_channel_avg));
min_zscore = num2str(min(zscore_channel_avg));
avg_zscore = num2str(mean(zscore_channel_avg));
disp('--------------------------------------------------------------')
disp('Z-SCORE SUMMMARY VALUES:')
disp('Behavior: ')
disp(behavior_name{1})
disp('Animal Number:')
disp(animal_num)
disp('Maximum Z-score: ')
disp(max_zscore)
disp('Minimum Z-score: ')
disp(min_zscore)
disp('Average Z-score: ')
disp(avg_zscore)
disp('Z-score Script zversion:')
disp(zversion)
disp('--------------------------------------------------------------')
