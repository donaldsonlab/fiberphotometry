import pandas as pd
files=['same_sex_3754_3904_Summary.csv', 'same_sex_3739_3784_Summary.csv', 'same_sex_3737_3738_Summary.csv', 'initial_pairings_3784_3904_Summary.csv', 'initial_pairings_3784_3743_Summary.csv', 'initial_pairings_3739_3754_Summary.csv', 'initial_pairings_3738_3754_Summary.csv', 'initial_pairings_3737_3904_Summary.csv', 'initial_pairings_3737_3743_Summary.csv', '2_weeks_3784_3904_Summary.csv', '2_weeks_3784_3904_part2_Summary.csv', '2_weeks_3739_3904_Summary.csv', '2_weeks_3739_3754_Summary.csv', '2_weeks_3738_3743_Summary.csv', '2_weeks_3737_3754_Summary.csv', '2_weeks_3737_3743_Summary.csv']
output_name='PFC_sync_beh.csv'

beh_df = pd.DataFrame(columns=['file'])
beh_dict={}

for file in files:
    file_df = pd.DataFrame(columns=['file'])
    file_df = file_df.append({'file': file}, ignore_index=True)
    #file_df=pd.DataFrame()
    #file_df['file']=file
    fdata=pd.read_csv(file)
    behaviors = fdata.select_dtypes(include=['bool']).columns
    for j, beh in enumerate(behaviors):
        duration=0
        flag = False
        for k in range(len(fdata['fTimeGreen'])):
            if fdata.at[k, beh]== True:
                if flag == False:
                    start = fdata.at[k, 'fTimeGreen']
                    flag=True    
            else:
                if flag == True:
                    end = fdata.at[k-1, 'fTimeGreen'] 
                    duration= duration + (end-start)
                    print(duration)
                flag= False
        file_df[beh]=duration
        
    
    beh_df=pd.concat([beh_df, file_df], sort=False, ignore_index=True)

beh_df.to_csv(output_name, index=False)
