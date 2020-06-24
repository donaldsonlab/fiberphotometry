%% Script to analze behavior fluorescence data
% written by Katie Gallagher Edited by Kathleen Murphy & Anna McTigue
% 1/29/2020
% 5/30/2020
% 6/11/2020

format long

% load in datasets
behaviorData = T152711; %time stamps corresponding to vole behavior
fData = Test20200409T152711; %fluorescent data

% separate columns
fTime = table2array(fData(:,1)); %time column in fluorescent data

fRedL = table2array(fData(:,3)); %3rd column in fluorescent data = red left 
fGreenL = table2array(fData(:,4)); %4th = green right
fRedR = table2array(fData(:,5)); % red right
fGreenR = table2array(fData(:,6)); % green left

bTime = table2array(behaviorData(:,3)); % time of behavior 
behavior = table2array(behaviorData(:,2)); % actual behavior
bTime = double(bTime);

%% De-interleave (if driver box NOT reset properly)

% determining which row index is red channel
offset1 = fGreenR(1:3:end);
offset2 = fGreenR(2:3:end);
offset3 = fGreenR(3:3:end);
stdoffsets = [std(offset1), std(offset2), std(offset3)];
redIdx = find(stdoffsets == min(stdoffsets(:)));

% assigning correct rows to colors
fGreenL1 = fGreenL(redIdx+2:3:end);
fGreenL2 = fGreenL(redIdx:3:end);
fGreenL3 = fGreenL(redIdx+1:3:end);

fGreenR1 = fGreenR(redIdx+2:3:end);
fGreenR2 = fGreenR(redIdx:3:end);
fGreenR3 = fGreenR(redIdx+1:3:end);

fRedR1 = fRedR(redIdx+2:3:end);
fRedR2 = fRedR(redIdx:3:end);
fRedR3 = fRedR(redIdx+1:3:end);

fRedL1 = fRedL(redIdx+2:3:end);
fRedL2 = fRedL(redIdx:3:end);
fRedL3 = fRedL(redIdx+1:3:end);

fTime1 = fTime(redIdx+2:3:end);
fTime2 = fTime(redIdx:3:end);
fTime3 = fTime(redIdx+1:3:end);

%% De-interleave (if driver box was reset properly)
% should record in following order: 470nm, 560nm, 415nm
% start data collection at row 5 (to eliminate inconsistencies in first 
% 3 rows) for each channel, taking every 3

% %Left Green
% fGreenL1 = fGreenL(5:3:end);
% fGreenL2 = fGreenL(6:3:end);
% fGreenL3 = fGreenL(7:3:end);
% 
% %Left Red
% fRedL1 = fRedL(5:3:end);
% fRedL2 = fRedL(6:3:end);
% fRedL3 = fRedL(7:3:end);
% 
% %Right Green
% fGreenR1 = fGreenR(5:3:end);
% fGreenR2 = fGreenR(6:3:end);
% fGreenR3 = fGreenR(7:3:end);
% 
% %Right Red
% fRedR1 = fRedR(5:3:end);
% fRedR2 = fRedR(6:3:end);
% fRedR3 = fRedR(7:3:end);
% 
% %Time
% fTime1 = fTime(5:3:end);
% fTime2 = fTime(6:3:end);
% fTime3 = fTime(7:3:end);



%% Minimize behavior data
%pull out index and time for every time behavior occurs
%initialize matrices to hold indices and corresponding times
behaviorIdx = {}; %will be populated with licking indices
behaviorT = {};
j=1;

for i = 1:length(behavior)
    if behavior(i)=='Side by Side'
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
figure('Name', 'Left Green Plot')
subplot(3,1,1)
plot(fTime1,fGreenL1)
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
plot(fTime2,fGreenL2)
xlabel('Time (ms)')
ylabel('Red')
for i = 1:length(startbout)
     xline(startbout(i),'g');
 end
for i = 1:length(finbout)
     xline(finbout(i),'r');
end
subplot(3,1,3)
plot(fTime3,fGreenL3)
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
figure('Name', 'Left Red Plot')
subplot(3,1,1)
plot(fTime1,fRedL1)
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
plot(fTime2,fRedL2)
xlabel('Time (ms)')
ylabel('Red')
for i = 1:length(startbout)
     xline(startbout(i),'g');
 end
for i = 1:length(finbout)
     xline(finbout(i),'r');
end
subplot(3,1,3)
plot(fTime3,fRedL3)
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
figure('Name', 'Right Green Plot')
subplot(3,1,1)
plot(fTime1,fGreenR1)
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
plot(fTime2,fGreenR2)
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
plot(fTime3,fGreenR3)
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
figure('Name', 'Right Red Plot')
subplot(3,1,1)
plot(fTime1,fRedR1)
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
plot(fTime2,fRedR2)
xlabel('Time (ms)')
ylabel('Red')
for i = 1:length(startbout)
     xline(startbout(i),'g');
 end
for i = 1:length(finbout)
     xline(finbout(i),'r');
end
subplot(3,1,3)
plot(fTime3,fRedR3)
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
