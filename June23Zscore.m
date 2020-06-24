%% Plots zscores for each behavior occurance - Green channel
% updated: 6/17/20 by Anna McTigue
%Test test. I'm not sure how this works yet.
%% Determines indices of behaviorT, 2sec before, & 5sec after in fTime3

% Initialize arrays
three_start_baseline = zeros(1,length(behaviorT)); % 3 sec before bout
three_start_idx = zeros(1,length(behaviorT));
two_startBaseline = zeros(1,length(behaviorT)); % 2 sec before bout
two_start_idx = zeros(1,length(behaviorT));
ends = zeros(1,length(behaviorT)); 
ends_idx = zeros(1,length(behaviorT));
behaviorIdx = zeros(1,length(behaviorT));

% Sets arrays with respective indices
for i = 1:length(behaviorT)
    %finds index in fTime3 that is closest to behaviorT(i)
    [val,idx1]=min(abs(fTime3-behaviorT(i))); 
    behaviorIdx(i)=idx1;
    % 3sec before bout (index in fTime3)
    three_start_baseline(i) = max(behaviorT(i) - 3000, fTime3(1));
    [val,idx2]=min(abs(fTime3-three_start_baseline(i)));
    three_start_idx(i)=idx2;
    % 2sec before bout (index in fTime3)
    two_startBaseline(i) = max(behaviorT(i) - 2000, fTime3(1)); 
    [val,idx3]=min(abs(fTime3-two_startBaseline(i)));
    two_start_idx(i)=idx3;
    %calculates time 5 seconds after each start bout
    ends(i) = min(fTime3(end),behaviorT(i) + 5000); 
    [val,idx4]=min(abs(fTime3-ends(i)));
    ends_idx(i)=idx4;
end

% std of all fluorescent signal in green channel
std_green = std(fGreenR3); 

% adjusts indices so that they are all the same
minlenB = min(ends_idx-three_start_idx); % looks at range in indices
for i = 1:length(behaviorT)
    if (ends_idx(i)-three_start_idx(i))>minlenB
         ends_idx(i)=three_start_idx(i)+minlenB;
    end
end
minlen=min(behaviorIdx-three_start_idx);

%% Calculate zscores   

% initialize arrays
f_baseline=zeros(1,minlen+1);
entire_range=zeros(length(behaviorT),minlenB+1); 
zscore=zeros(length(behaviorT),minlenB+1);

% calculates z score for each behavior occurance
for i = 1:length(behaviorT)
    % floursence signal from -2sec to 5sec behavior
    entire_range(i,:) = fGreenR3(three_start_idx(i):ends_idx(i)).'; 
    % baseline avg calculated as mean from 3 to 2 seconds before behavior
    zscore(i,:) = (entire_range(i,:) - mean(fGreenR3((three_start_idx(i)):two_start_idx(i)).'))/std_green;       
end

%% Calculates average zscores for each time point in each bout

zscore_green_avg = zeros(1,minlenB+1);
for j = 1:minlenB+1
    zscore_green_avg(j) = mean(zscore(:,j));
end 

%% Standard Error of the Mean 
% calculate standard deviation 
std_zavg = std(zscore);

% calculate standard error
sem_green = std_zavg/sqrt(length(behaviorT(i)));

%plot avg zscore with shaded std/sem
curve1 = zscore_green_avg + sem_green;
curve2 = zscore_green_avg - sem_green;
  
curve1 = curve1.';
curve2 = curve2.';

%% Plotting
x = [-3:(8/(minlenB)):+5];  % holds minlenB points between -2 and 5

figure
% Plots z scores for each behavior bout
for i=1:length(behaviorT)
    hold on
    plot(x,zscore(i,:),'k',0,0.5);
end
% Plots avg z score across all bouts
plot(x,zscore_green_avg,'LineWidth',4)
xlabel('Time (s)')
ylabel('zscore')
title('Side by Side 2020-04-09T152711')
hold on
xline(0,':','LineWidth',2);

% SEM lines
plot(x,curve1,'r',0,0.5,'LineWidth',2);
plot(x,curve2,'r',0,0.5,'LineWidth',2);

