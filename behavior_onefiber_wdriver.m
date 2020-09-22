%% Script to analze behavior fluorescence data (one fiber)
% written by Katie Gallagher Edited by Kathleen Murphy & Anna McTigue

% UPDATE THIS EACH NEW VERSION (date of update):
onefiberversion = 'v1.2'; 

format long
%% Read Tables

fTime = table2array(fData(:,1)); %time column in fluorescent data

fRed = table2array(fData(:,3)); %3rd column (red)
fGreen = table2array(fData(:,4)); %4th column (green)

bTime = table2array(behaviorData(:,3)); % time of behavior 
behavior = table2array(behaviorData(:,2)); % actual behavior
bTime = double(bTime);

%% De-interleave

% determining which row index is red channel
offset1 = fRed(1:3:end);
offset2 = fRed(2:3:end);
offset3 = fRed(3:3:end);
meanoffsets = [mean(offset1), mean(offset2), mean(offset3)];
redIdx = find(meanoffsets == max(meanoffsets(:)));

% assigning correct rows to colors
fGreenisosbestic = fGreen(redIdx+2:3:end); %iso
fGreenred = fGreen(redIdx:3:end); %red
fGreengreen = fGreen(redIdx+1:3:end);%green

fRedisosbestic = fRed(redIdx+2:3:end);
fRedred = fRed(redIdx:3:end);
fRedgreen = fRed(redIdx+1:3:end);

fTimeIsosbestic = fTime(redIdx+2:3:end);
fTimeRed = fTime(redIdx:3:end);
fTimeGreen = fTime(redIdx+1:3:end);

%% Minimize behavior data
%pull out index and time for every time behavior occurs
%initialize matrices to hold indices and corresponding times
behaviorIdx = {}; %will be populated with behavior indices
behaviorT = {};
j=1;
for i = 1:length(behavior)
    if string(behavior(i)) == behavior_name
        behaviorIdx{j} = i;
        behaviorT{j} = bTime(i);
        j=j+1; 
    end 
end 

behaviorT = cell2mat(behaviorT); 
behaviorIdx = cell2mat(behaviorIdx);
 
% if time between behaviors sis greater than threshold seconds then count as 
% one bout
Thres=200;
startbout = {}; %start of first bout is the first time it licks
startboutIdx = {}; %index of start bout
finbout = {};
finboutIdx = {}; %index of end bout
% i=1;
% startbout{i}=behaviorT(i);
% startboutIdx{i} = behaviorIdx(i);
% j=1;
% % seeing if diff in time btwn licks is great enough to consider it as 
% % about5
% while i < length(behaviorT)
%    if abs(behaviorT(i+1)-behaviorT(i))>=Thres 
%        endTime=behaviorT(i);
%        endTimeIdx = behaviorIdx(i);
%        startTime=behaviorT(i+1);
%        startTimeIdx = behaviorIdx(i+1);
%        finbout{j} = endTime;
%        finboutIdx{j} = endTimeIdx;
%        startbout{j+1} = startTime;
%        startboutIdx{j+1} = startTimeIdx;
%  
%        j=j+1;
%    end
%      i=i+1;
% end
% finbout{j} = behaviorT(end);
% finboutIdx{j}=behaviorIdx(end);
% finbout{length(startbout)} = behaviorT(length(behaviorT));
% finbout = cell2mat(finbout); 
% startbout = cell2mat(startbout);
% finboutIdx = cell2mat(finboutIdx);
% startboutIdx = cell2mat(startboutIdx);
% %seeing if number of licks within each bout is great enough to consider it
% %as a bout
% % threshold on how many licks constitute a bout
% numLicksThres = 0; %must have 10 licks in order to be considered a bout
% i=1;
% j=1;
% while i < length(startbout)
%    if (finboutIdx(i) - startboutIdx(i)) < numLicksThres
%        finbout(i) = [];
%        startbout(i) = [];
%         j=j+1;
%    end 
%    i=i+1;
% end 

%% Plot behavior times on raw data plot as tick marks

%Green Plot
gplot_title = string(behavior_name) + ' Green Plot ' + ' Animal no. '+ ... 
    animal_num + ' ' + onefiberversion;
figure('Name', gplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fGreenisosbestic)
xlabel('Time (ms)')
ylabel('Isosbestic')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
    xline(startbout(i),'g');
end
for i = 1:length(finbout)
    xline(finbout(i),'r');
end
subplot(3,1,2)
plot(fTimeRed,fGreenred)
xlabel('Time (ms)')
ylabel('Red')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
     xline(startbout(i),'g');
 end
for i = 1:length(finbout)
     xline(finbout(i),'r');
end
subplot(3,1,3)
plot(fTimeGreen,fGreengreen)
xlabel('Time (ms)')
ylabel('Green')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
    xline(startbout(i),'g');
end
for i = 1:length(finbout)
    xline(finbout(i),'r');
end

%Red PLot
rplot_title = string(behavior_name) + ' Red Plot' + ' Animal no. '+ ... 
    animal_num + ' ' + onefiberversion;
figure('Name', rplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fRedisosbestic)
xlabel('Time (ms)')
ylabel('Isosbestic')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
    xline(startbout(i),'g');
end
for i = 1:length(finbout)
    xline(finbout(i),'r');
end
subplot(3,1,2)
plot(fTimeRed,fRedred)
xlabel('Time (ms)')
ylabel('Red')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
     xline(startbout(i),'g');
 end
for i = 1:length(finbout)
     xline(finbout(i),'r');
end
subplot(3,1,3)
plot(fTimeGreen,fRedgreen)
xlabel('Time (ms)')
ylabel('Green')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
for i = 1:length(startbout)
    xline(startbout(i),'g');
end
for i = 1:length(finbout)
    xline(finbout(i),'r');
end
