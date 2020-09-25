%% Script to analze behavior fluorescence data (two fiber) 
% written by Katie Gallagher Edited by Kathleen Murphy & Anna McTigue

% UPDATE THIS EACH NEW VERSION (date of update):
twofiberversion = 'v1.4'; 

format long
%% Read Tables

fTime = table2array(fData(:,1)); %time column in fluorescent data

fRedL = table2array(fData(:,3)); %3rd column in fluorescent data = red left 
fGreenL = table2array(fData(:,4)); %4th = green left
fRedR = table2array(fData(:,5)); % red right
fGreenR = table2array(fData(:,6)); % green right

bTime = table2array(behaviorData(:,3)); % time of behavior 
behavior = table2array(behaviorData(:,2)); % actual behavior
bTime = double(bTime);

%% De-interleave (if driver box NOT reset properly)

% determining which row index is red channel
offset1 = fRedR(1:3:end);
offset2 = fRedR(2:3:end);
offset3 = fRedR(3:3:end);
meanoffsets = [mean(offset1), mean(offset2), mean(offset3)];
redIdx = find(meanoffsets == max(meanoffsets(:)));

% assigning correct rows to colors
fGreenLisosbestic = fGreenL(redIdx+2:3:end); %iso
fGreenLred = fGreenL(redIdx:3:end); %red
fGreenLgreen = fGreenL(redIdx+1:3:end);%green

fGreenRisosbestic = fGreenR(redIdx+2:3:end);
fGreenRred = fGreenR(redIdx:3:end);
fGreenRgreen = fGreenR(redIdx+1:3:end);

fRedRisosbestic = fRedR(redIdx+2:3:end);
fRedRred = fRedR(redIdx:3:end);
fRedRgreen = fRedR(redIdx+1:3:end);

fRedLisosbestic = fRedL(redIdx+2:3:end);
fRedLred = fRedL(redIdx:3:end);
fRedLgreen = fRedL(redIdx+1:3:end);

fTimeIsosbestic = fTime(redIdx+2:3:end);
fTimeRed = fTime(redIdx:3:end);
fTimeGreen = fTime(redIdx+1:3:end);

%% De-interleave (if driver box was reset properly)
% should record in following order: 470nm, 560nm, 415nm
% start data collection at row 5 (to eliminate inconsistencies in first 
% 3 rows) for each channel, taking every 3

% %Left Green
% fGreenLisosbestic = fGreenL(5:3:end);
% fGreenLred = fGreenL(6:3:end);
% fGreenLgreen = fGreenL(7:3:end);
% 
% %Left Red
% fRedLisosbestic = fRedL(5:3:end);
% fRedLred = fRedL(6:3:end);
% fRedLgreen = fRedL(7:3:end);
% 
% %Right Green
% fGreenRisosbestic = fGreenR(5:3:end);
% fGreenRred = fGreenR(6:3:end);
% fGreenRgreen = fGreenR(7:3:end);
% 
% %Right Red
% fRedRisosbestic = fRedR(5:3:end);
% fRedRred = fRedR(6:3:end);
% fRedRgreen = fRedR(7:3:end);
% 
% %Time
% fTimeIsosbestic = fTime(5:3:end);
% fTimeRed = fTime(6:3:end);
% fTimeGreen = fTime(7:3:end);

%% Minimize behavior data
%pull out index and time for every time behavior occurs
%initialize matrices to hold indices and corresponding times
behaviorIdx = {}; %will be populated with behavior indices
behaviorT = {};
j=1;

% Select behavior to analyze
% prompt = 'What behavior do you want to analyze? \n';
% behavior_name = input(prompt, 's');
for i = 1:length(behavior)
    if string(behavior(i)) == behavior_name
        behaviorIdx{j} = i;
        behaviorT{j} = bTime(i);
        j=j+1; 
    end 
end 

behaviorT = cell2mat(behaviorT); 
behaviorIdx = cell2mat(behaviorIdx);
 
% if time between licks is greater than threshold seconds then count as 
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

%% plot behavior times on raw data plot as tick marks

%Left Green Plot
lgplot_title = string(behavior_name) + ' Left Green Plot ' + ' Animal no. '+ ... 
    animal_num + ' ' + twofiberversion;
figure('Name', lgplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fGreenLisosbestic)
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
plot(fTimeRed,fGreenLred)
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
plot(fTimeGreen,fGreenLgreen)
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

%Left Red PLot
lrplot_title = string(behavior_name) + ' Left Red Plot' + ' Animal no. '+ ... 
    animal_num + ' ' + twofiberversion;
figure('Name', lrplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fRedLisosbestic)
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
plot(fTimeRed,fRedLred)
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
plot(fTimeGreen,fRedLgreen)
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

% Right Green Plot
rgplot_title = string(behavior_name) + ' Right Green Plot' + ' Animal no. '+ ... 
    animal_num + ' ' + twofiberversion;
figure('Name', rgplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fGreenRisosbestic)
xlabel('Time (ms)')
ylabel('Isosbestic')
for i = 1:length(behaviorT)
    xline(behaviorT(i),'k')
end 
%for i = 1:length(startbout)
%    xline(startbout(i),'g');
%end
%for i = 1:length(finbout)
%    xline(finbout(i),'r');
%end
subplot(3,1,2)
plot(fTimeRed,fGreenRred)
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
plot(fTimeGreen,fGreenRgreen)
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

%Right Red Plot
rrplot_title = string(behavior_name) + ' Right Red Plot' + ' Animal no. '+ ... 
    animal_num + ' ' + twofiberversion;
figure('Name', rrplot_title)
subplot(3,1,1)
plot(fTimeIsosbestic,fRedRisosbestic)
xlabel('Time (ms)')
ylabel('Isospestic')
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
plot(fTimeRed,fRedRred)
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
plot(fTimeGreen,fRedRgreen)
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



