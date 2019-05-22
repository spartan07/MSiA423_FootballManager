def pre_process(path):

#Remove symbols and convert to nums for Wage,Value and Release Clause
    fifa = pd.read_csv(path+'EA_FIFA19.csv')

    def value_to_int(df_value):
        try:
            value = float(df_value[1:-1])
            suffix = df_value[-1:]

            if suffix == 'M':
                value = value * 1000000
            elif suffix == 'K':
                value = value * 1000
        except ValueError:
            value = 0
        return value

    fifa['Value'] = fifa['Value'].apply(value_to_int)
    fifa['Wage'] = fifa['Wage'].apply(value_to_int)

    fifa['Release Clause'] = fifa['Release Clause'].fillna('0')
    fifa['Release Clause'] = fifa['Release Clause'].apply(value_to_int)

    def check_contract(row):
        month_list=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ref_date = datetime(2018,5,31,0,0,0)
        contract = row['Contract Valid Until']
        try:
            match = re.findall('(\w{3}) \d{1,2}, (\d{4})',contract)
            if len(match)!=0:
                month_str = match[0][0]
                month = month_list.index(month_str)+1
                year = int(match[0][1])
                dt = datetime(year,month,1,0,0,0)
                a = dt- ref_date
                row['contract_days'] = a.days
            else:
                match = re.findall('(\d{4})',contract)
                month = month_list.index('Jun')+1
                year = int(match[0])
                dt = datetime(year,month,1,0,0,0)
                a = dt- ref_date
                row['contract_days'] = a.days
            return row
        except:
            year = 2020
            month = month_list.index('Jun')
            dt = datetime(year,month,1,0,0,0)
            a = dt- ref_date
            row['contract_days'] = a.days
            return row


    fifa = fifa.apply(check_contract,axis=1)


    #Turn Preferred Foot into a binary indicator variable
    def right_footed(df):
        if (df['Preferred Foot'] == 'Right'):
            return 1
        else:
            return 0

    #Create a simplified position varaible to account for all player positions
    def simple_position(df):
        if (df['Position'] == 'GK'):
            return 'GK'
        elif ((df['Position'] == 'RB') | (df['Position'] == 'LB') | (df['Position'] == 'CB') | (df['Position'] == 'LCB') | (df['Position'] == 'RCB') | (df['Position'] == 'RWB') | (df['Position'] == 'LWB') ):
            return 'DF'
        elif ((df['Position'] == 'LDM') | (df['Position'] == 'CDM') | (df['Position'] == 'RDM')):
            return 'DM'
        elif ((df['Position'] == 'LM') | (df['Position'] == 'LCM') | (df['Position'] == 'CM') | (df['Position'] == 'RCM') | (df['Position'] == 'RM')):
            return 'MF'
        elif ((df['Position'] == 'LAM') | (df['Position'] == 'CAM') | (df['Position'] == 'RAM') | (df['Position'] == 'LW') | (df['Position'] == 'RW')):
            return 'AM'
        elif ((df['Position'] == 'RS') | (df['Position'] == 'ST') | (df['Position'] == 'LS') | (df['Position'] == 'CF') | (df['Position'] == 'LF') | (df['Position'] == 'RF')):
            return 'ST'
        else:
            return df.Position


    #Replace Nationality with a binary indicator variable for 'Major Nation'
    def major_nation(df):
        nat_counts = df['Nationality'].value_counts()
        nat_list = nat_counts[nat_counts > 250].index.tolist()
        if (df.Nationality in nat_list):
            return 1
        else:
            return 0


    #Create a copy of the original dataframe to avoid indexing errors
    df1 = fifa.copy()

    #Apply changes to dataset to create new column
    df1['Right_Foot'] = df1.apply(right_footed, axis=1)
    df1['Simple_Position'] = df1.apply(simple_position,axis = 1)
#    df1['Major_Nation'] = df1.apply(major_nation,axis = 1)

    #Split the Work Rate Column in two
    tempwork = df1["Work Rate"].str.split("/ ", n = 1, expand = True)
    #Create new column for first work rate
    df1["WorkRate1"]= tempwork[0]
    #Create new column for second work rate
    df1["WorkRate2"]= tempwork[1]

    adhoc = df1[['Unnamed: 0','ID','Photo','Flag','Club Logo','Jersey Number','Joined','Special','Loaned From','Body Type', 'Release Clause',
                   'Weight','Height','Contract Valid Until','Name','Club']]
    df1.drop(columns=['Unnamed: 0','ID','Photo','Flag','Club Logo','Jersey Number','Joined','Special','Loaned From','Body Type', 'Release Clause',
                   'Weight','Height','Contract Valid Until','Name','Club'],inplace = True)
    df1.drop(columns=['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
           'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
           'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB'],inplace=True)
    df1.drop(['Work Rate','Preferred Foot','Real Face', 'Position','Nationality'], axis=1,inplace=True)
    df2=pd.get_dummies(df1)
    df2.to_csv('./data/processed_data.csv')