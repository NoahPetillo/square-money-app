import pandas as pd
import altair as alt
import streamlit as st
#use streamlit run streamlit_new_orleans.py
#Load data and clean
df = pd.read_csv("listings.csv.gz", compression='gzip')
df['price_numeric'] = df['price'].str.replace('$', '').str.replace(',', '').astype(float)
df_clean = df[
    (df['price_numeric'] > 0) & 
    (df['price_numeric'] < 1000) &  
    (df['review_scores_rating'].notna()) &  
    (df['review_scores_rating'] > 0)  
].copy()

#Sidebar
st.sidebar.header("Filters")
neighborhoods = df_clean['neighbourhood_cleansed'].value_counts().head(10).index.tolist()
selected_neighborhoods = st.sidebar.multiselect("Neighborhood", neighborhoods, default=neighborhoods)
room_types = df_clean['room_type'].unique().tolist()
selected_room_types = st.sidebar.multiselect("Room Type", room_types, default=room_types)
price_range = st.sidebar.slider("Price Range", 0, 1000, (0, 500))
review_range = st.sidebar.slider("Review Score Range", 0.0, 5.0, (3.0, 5.0), step=0.1)

# Filter data
filtered = df_clean[
    df_clean['neighbourhood_cleansed'].isin(selected_neighborhoods) &
    df_clean['room_type'].isin(selected_room_types) &
    (df_clean['price_numeric'] >= price_range[0]) &
    (df_clean['price_numeric'] <= price_range[1]) &
    (df_clean['review_scores_rating'] >= review_range[0]) &
    (df_clean['review_scores_rating'] <= review_range[1])
]

# Main dashboard
st.title("New Orleans Airbnb Data Dashboard")

# Box Plot
st.subheader("Price Distribution by Neighborhood and Room Type")
if not filtered.empty:
    price_95th = float(filtered['price_numeric'].quantile(0.95))
    box = alt.Chart(filtered).mark_boxplot().encode(
        x=alt.X('neighbourhood_cleansed:N', sort='-y', title='Neighborhood'),
        y=alt.Y('price_numeric:Q', title='Price per Night ($)', scale=alt.Scale(domain=[0, price_95th], clamp=True)),
        color=alt.Color('room_type:N', title='Room Type'),
        tooltip=['neighbourhood_cleansed', 'room_type', 'price_numeric']
    ).properties(width=600, height=400)
    st.altair_chart(box, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# Scatter Plot with Brushing
st.subheader("Price vs Review Score")
if not filtered.empty:
    brush = alt.selection_interval()
    scatter = alt.Chart(filtered).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X('price_numeric:Q', title='Price per Night ($)', scale=alt.Scale(domain=[0, 500], clamp=True)),
        y=alt.Y('review_scores_rating:Q', title='Review Score', scale=alt.Scale(domain=[3, 5], clamp=True)),
        color=alt.Color('room_type:N', title='Room Type'),
        tooltip=['name', 'price_numeric', 'review_scores_rating', 'room_type', 'neighbourhood_cleansed']
    ).add_selection(brush).properties(width=600, height=400)

    trend = alt.Chart(filtered).transform_regression(
        'price_numeric', 'review_scores_rating'
    ).mark_line(color='red', strokeWidth=2).encode(
        x='price_numeric:Q',
        y='review_scores_rating:Q'
    )

    st.altair_chart(scatter + trend, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# Heat Map
st.subheader("Property Type Distribution by Neighborhood")
top_property_types = df_clean['property_type'].value_counts().head(6).index.tolist()
filtered_heat = filtered[filtered['property_type'].isin(top_property_types)]
if not filtered_heat.empty:
    heat = alt.Chart(filtered_heat).mark_rect().encode(
        x=alt.X('neighbourhood_cleansed:N', title='Neighborhood', sort='-y'),
        y=alt.Y('property_type:N', title='Property Type', sort='-x'),
        color=alt.Color('count():Q', title='Number of Listings', scale=alt.Scale(scheme='blues')),
        tooltip=['neighbourhood_cleansed', 'property_type', 'count()']
    ).properties(width=600, height=400)
    st.altair_chart(heat, use_container_width=True)
else:
    st.info("No data available for selected filters.")


