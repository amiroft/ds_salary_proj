import pandas as pd

# read in the data
df = pd.read_csv('glassdoor_jobs.csv')

# remove rows with invalid salary estimates
df = df[df['Salary Estimate'] != '-1']

# parse salary information
df['hourly'] = df['Salary Estimate'].str.lower().str.contains('per hour').astype(int)
df['employer_provided'] = df['Salary Estimate'].str.lower().str.contains('employer provided salary:').astype(int)
salary = df['Salary Estimate'].str.split('(')[0].str.replace('K','').str.replace('$','')
df['min_salary'] = salary.str.split('-').str[0].str.lower().str.replace('per hour','').str.replace('employer provided salary:','').astype(int)
df['max_salary'] = salary.str.split('-').str[1].str.lower().str.replace('per hour','').str.replace('employer provided salary:','').astype(int)
df['avg_salary'] = (df['min_salary'] + df['max_salary']) / 2

# parse company name information
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)

# parse job location information
df['job_state'] = df['Location'].str.split(',').str[1]
df['same_state'] = (df['Location'] == df['Headquarters']).astype(int)

# parse company age information
df['age'] = df['Founded'].apply(lambda x: 2020 - x if x > 0 else 0)

# parse job description information
df['python_yn'] = df['Job Description'].str.lower().str.contains('python').astype(int)
df['R_yn'] = df['Job Description'].str.lower().str.contains('r studio|r-studio').astype(int)
df['spark'] = df['Job Description'].str.lower().str.contains('spark').astype(int)
df['aws'] = df['Job Description'].str.lower().str.contains('aws').astype(int)
df['excel'] = df['Job Description'].str.lower().str.contains('excel').astype(int)

# drop unnecessary columns
df_out = df.drop(['Unnamed: 0'], axis=1)

# save cleaned data to CSV file
df_out.to_csv('salary_data_cleaned.csv', index=False)
