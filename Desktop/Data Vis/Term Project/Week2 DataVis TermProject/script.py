import pandas as pd
import altair as alt
import numpy as np

# Load the data
file_path = 'voice-assistant-failures.csv'
df = pd.read_csv(file_path)

# print(f"Before cleaning{df}, size = {df.size}")

# Cleaning portion:
# Standardize and clean categorical columns
for col in ['gender', 'accent', 'Failure_Type', 'Failure_Source']:
    df[col] = df[col].astype(str).str.strip().str.title().replace({'#N/A': 'Unknown', 'Nan': 'Unknown', '': 'Unknown'})

# Replace empty or 'nan' strings with np.nan for easier handling
df.replace({'': np.nan, 'nan': np.nan, '#N/A': np.nan}, inplace=True) #I found this snip of code online -- do not really understand it lol. I guess np.nan is an object you can use the .fillna method on?

# Fill NaNs in key columns with 'Unknown'
df['gender'] = df['gender'].fillna('Unknown')
df['accent'] = df['accent'].fillna('Unknown')
df['Failure_Type'] = df['Failure_Type'].fillna('Unknown')
df['Failure_Source'] = df['Failure_Source'].fillna('Unknown')


# print(f"After Cleaning{df}, size = {df.size}")

# --- 1. Most common failure types and their sources ---
failures_by_type = df.groupby(['Failure_Type', 'Failure_Source']).size().reset_index()
failures_by_type.columns = ['Failure_Type', 'Failure_Source', 'count']

chart1 = alt.Chart(failures_by_type).mark_bar().encode(
    x=alt.X('Failure_Type:N', title='Failure Type'),
    y=alt.Y('count:Q', title='Count'),
    color='Failure_Source:N',
    tooltip=['Failure_Type', 'Failure_Source', 'count']
).properties(
    title='Most Common Voice Assistant Failure Types by Source',
    width=600
)


# Question asked in last slideshow: Are users who perceive themselves 
# as having an accent more likely to experience specific types of failures? 

df['accent'] = df['accent'].fillna('Unknown')
failures_accent = df.groupby(['accent', 'Failure_Type']).size().reset_index()

# print(failures_accent)

# Print percentage of people who have an accent -- show more insights into the accent chart
num_with_accent = (df['accent'] == 'Yes').sum()
total_people = len(df)
percent_with_accent = (num_with_accent / total_people) * 100
print(f"Percentage of people who have an accent: {percent_with_accent}%")


failures_accent.columns = ['accent', 'Failure_Type', 'count']


chart2 = alt.Chart(failures_accent).mark_bar().encode(
    x=alt.X('Failure_Type:N', title='Failure Type'),
    y=alt.Y('count:Q', title='Count'),
    color='accent:N',
    tooltip=['accent', 'Failure_Type', 'count']
).properties(
    title='Failure Types Experienced by Users with/without Accents',
    width=600
)

# Question asked in last slideshow: Are certain genders more inclined to us AI voice assistants compared to others?

df['gender'] = df['gender'].fillna('Unknown')
gender_counts = df['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']

chart3 = alt.Chart(gender_counts).mark_bar().encode(
    x=alt.X('gender:N', title='Gender'),
    y=alt.Y('count:Q', title='Number of Users'),
    color='gender:N',
    tooltip=['gender', 'count']
).properties(
    title='Voice Assistant Usage by Gender',
    width=400
)


chart1.save('failures_by_type_and_source.html')
chart2.save('failures_by_accent.html')
chart3.save('usage_by_gender.html')
