#source venv/bin/activate

import pandas as pd
import altair as alt
df = pd.read_csv("oecd-wealth-health-2014.csv")

chart = alt.Chart(df).mark_point().encode(
    x=alt.X('Income:Q', scale=alt.Scale(domain=[0, 80000])),  # Adjust the range as needed
    y=alt.Y('LifeExpectancy:Q', scale=alt.Scale(clamp=True)),  # Clamp ensures the line doesn't leave the axis
    color='Region:N'
)

chart = chart + chart.transform_regression('Income', 'LifeExpectancy', extent=[0, 80000]).mark_line(stroke='RED')
# print(df)

chart.save('oecd_chart.html')


regions = df['Region'].unique()

for region in regions:
    region_df = df[df['Region'] == region]
    region_chart = alt.Chart(region_df).mark_point(strokeWidth=2, shape = 'triangle').encode( 
        x='Income:Q',
        y='LifeExpectancy:Q',
        color=alt.value("#1580A3")
    ).properties(
        title=f'Region: {region}'
    )
    region_chart = region_chart + region_chart.transform_regression('Income', 'LifeExpectancy').mark_line(stroke='RED')
    region_chart.save(f'oecd_chart_{region}.html')
    
    