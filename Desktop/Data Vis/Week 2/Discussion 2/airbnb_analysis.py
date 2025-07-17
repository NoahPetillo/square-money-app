import pandas as pd
import altair as alt
import numpy as np

df = pd.read_csv("listings.csv.gz", compression='gzip')

df['price_numeric'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)

df_clean = df[
    (df['price_numeric'] > 0) & 
    (df['price_numeric'] < 1000) &  
    (df['review_scores_rating'].notna()) &  
    (df['review_scores_rating'] > 0)  
].copy()

top_neighborhoods = df_clean['neighbourhood_cleansed'].value_counts().head(10).index.tolist()
df_viz1 = df_clean[df_clean['neighbourhood_cleansed'].isin(top_neighborhoods)]

price_95th_percentile = float(df_viz1['price_numeric'].quantile(0.95))

chart1 = alt.Chart(df_viz1).mark_boxplot().encode(
    x=alt.X('neighbourhood_cleansed:N', sort='-y', title='Neighborhood'),
    y=alt.Y('price_numeric:Q', title='Price per Night ($)', scale=alt.Scale(domain=[0, price_95th_percentile], clamp=True)),
    color=alt.Color('room_type:N', title='Room Type'),
    # tooltip=['neighbourhood_cleansed', 'room_type', 'price_numeric']
).properties(
    title='Price Distribution by Neighborhood and Room Type',
    width=600,
    height=400
)

chart1.save('airbnb_price_distribution.html')

chart2 = alt.Chart(df_clean).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X('price_numeric:Q', title='Price per Night ($)', scale=alt.Scale(domain=[0, 500], clamp=True)),
    y=alt.Y('review_scores_rating:Q', title='Review Score', scale=alt.Scale(domain=[3, 5], clamp=True)),
    color=alt.Color('room_type:N', title='Room Type'),
    # tooltip=['name', 'price_numeric', 'review_scores_rating', 'room_type', 'neighbourhood_cleansed']
).properties(
    title='Price vs Review Score Relationship',
    width=600,
    height=400
)

trend_line = alt.Chart(df_clean).transform_regression(
    'price_numeric', 'review_scores_rating'
).mark_line(color='red', strokeWidth=2).encode(
    x='price_numeric:Q',
    y='review_scores_rating:Q'
)

chart2_with_trend = alt.layer(chart2, trend_line)
chart2_with_trend.save('airbnb_price_vs_rating.html')

top_neighborhoods_viz3 = df_clean['neighbourhood_cleansed'].value_counts().head(8).index.tolist()
top_property_types = df_clean['property_type'].value_counts().head(6).index.tolist()

df_viz3 = df_clean[
    (df_clean['neighbourhood_cleansed'].isin(top_neighborhoods_viz3)) &
    (df_clean['property_type'].isin(top_property_types))
]

chart3 = alt.Chart(df_viz3).mark_rect().encode(
    x=alt.X('neighbourhood_cleansed:N', title='Neighborhood', sort='-y'),
    y=alt.Y('property_type:N', title='Property Type', sort='-x'),
    color=alt.Color('count():Q', title='Number of Listings', scale=alt.Scale(scheme='blues')),
    tooltip=['neighbourhood_cleansed', 'property_type', 'count()']
).properties(
    title='Property Type Distribution by Neighborhood',
    width=600,
    height=400
)

chart3.save('airbnb_property_distribution.html')


