import pandas as pd
import altair as alt
df = pd.read_csv("university-donations.csv")
df['Gift Date'] = pd.to_datetime(df['Gift Date'], format='%m/%d/%y')
df = df[df['Gift Amount'] <= 50000]  # Optional: filter outliers

# Keep only the top 25 majors by count
major_counts = df['Major'].value_counts().nlargest(50).index

df = df[df['Major'].isin(major_counts)]

# Filter to only include years 2010-2015
df = df[(df['Gift Date'].dt.year >= 2010) & (df['Gift Date'].dt.year <= 2015)]

# Brush selection on the scatter plot (Gift Date)
brush = alt.selection_interval(encodings=['x'])

# Point selection on the bar chart (Major)
major_click = alt.selection_point(fields=['Major'])

# Scatter plot: Gift Amount vs. Year, colored by Major
scatter = alt.Chart(df).mark_circle(size=10).encode(
    x=alt.X('Gift Date:T', title='Year', axis=alt.Axis(format='%Y', values=[
        pd.Timestamp(year, 1, 1) for year in range(2010, 2016)
    ])),
    y=alt.Y('Gift Amount:Q', title='Gift Amount', scale=alt.Scale(domain=[0, 50000])),
    color=alt.Color('Major:N', legend=alt.Legend(title="Major")),
    opacity=alt.condition(major_click, alt.value(1), alt.value(0.2)),
    tooltip=['Gift Date:T', 'Gift Amount:Q', 'Major:N']
).add_params(
    brush, major_click
).transform_filter(
    major_click
)

# Bar chart: Count of donations per Major, filtered by brush
bars = alt.Chart(df).mark_bar().encode(
    x=alt.X('Major:N', title='Major', sort= '-y'),
    y=alt.Y('sum(Gift Amount):Q', title='Total Amount Donated'),
    color=alt.Color('Major:N', legend=None),
    opacity=alt.condition(brush, alt.value(1), alt.value(0.2)),
    tooltip=['Major:N', alt.Tooltip('sum(Gift Amount):Q', title='Total Amount Donated')]
).add_params(
    major_click
).transform_filter(
    brush
)

# Combine the two views vertically
chart = scatter.properties(width=600, height=300) & bars.properties(width=600, height=100)

chart.save('interactive_linked_chart.html')
