import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

st.set_page_config(page_title="Pune Real Estate Analytics", layout="wide")

# Custom CSS
st.markdown("""
<style>
body {
    font-family: 'Arial', sans-serif;
}
h1, h2, h3 {
    color: #00FA71;
    text-align: center;
}
.sidebar .sidebar-content {
    background-color: #f0f0f5;
}
.stButton>button {
    background-color: #4CAF50;
    color: black;
    padding: 12px 20px;
    border-radius: 4px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #45a049;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
    <style>
        .gradient-text {
            font-weight: bold;
            font-size: 42px;
            background: linear-gradient(270deg, #4FC3F7, #00BCD4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            color: transparent;
            display: inline;
        }
    </style>

    <h1 style='text-align: center;'>
        🏠 <span class="gradient-text">Pune Real Estate Analytics Dashboard</span> 📊
    </h1>
""", unsafe_allow_html=True)

# Header Image
image_path = "datasets/page_3/data_analysis_image.jpg"
image = Image.open(image_path).resize((1000, 500))
st.image(image)

# Intro
st.markdown("""
Welcome to the **Pune Real Estate Analytics Dashboard**!  
Explore real estate trends, prices, and visual insights from Pune using interactive charts and maps.
""")

# Load data
feature_path = Path('datasets/page_3/feature_text.pkl')
feature_text = pickle.load(open(feature_path, 'rb'))

group_df_median = pd.read_csv('datasets/page_3/median_agg_map_df.xls')
group_df_mean = pd.read_csv('datasets/page_3/avg_agg_map_df.xls')
new_df = pd.read_csv('datasets/page_3/analystics_module_data.xls')

group_df_median.columns = ['Location', 'Price', 'Price Per Sq.Ft.', 'Built Up Area', 'Latitude', 'Longitude']
group_df_mean.columns = ['Location', 'Price', 'Price Per Sq.Ft.', 'Built Up Area', 'Latitude', 'Longitude']

# Section: Map
st.markdown("---")
st.header("📍 Location Price per Sqft Geomap")
agg_method = st.radio("Choose the aggregation method:", ('Mean', 'Median'))

df_to_use = group_df_mean if agg_method == 'Mean' else group_df_median
fig_map = px.scatter_mapbox(
    df_to_use,
    lat="Latitude",
    lon="Longitude",
    color="Price Per Sq.Ft.",
    size='Built Up Area',
    color_continuous_scale=px.colors.cyclical.IceFire,
    zoom=9.7,
    mapbox_style="open-street-map",
    hover_name='Location',
    hover_data={'Price': True},
    width=1600,
    height=550
)

fig_map.update_traces(hovertemplate="""
<b>Location:</b> %{hovertext}<br>
<b>Price per Sq.Ft.:</b> ₹%{marker.color:.2f}<br>
<b>Built Up Area:</b> %{marker.size:,.2f} sq.ft.<br>
<b>Price:</b> ₹%{customdata[0]:,.2f} Crore<br><extra></extra>
""")

st.plotly_chart(fig_map, use_container_width=True)

# Section: Area vs Price
st.markdown("---")
st.header("📏 Area vs Price")

fig_area_price = px.scatter(
    new_df, x="built_up_area", y="price", color="bedrooms", title="Built-Up Area vs Price"
)
fig_area_price.update_layout(width=900, height=600)
fig_area_price.update_traces(hovertemplate="""
<b>Built-up Area:</b> %{x} sq.ft.<br>
<b>Price:</b> ₹%{y:.2f} Crore<br>
<b>Bedrooms:</b> %{marker.color}<br><extra></extra>
""")
fig_area_price.update_yaxes(tickprefix="₹", tickformat=",.2f", ticksuffix=" Crore")
st.plotly_chart(fig_area_price)

# Section: BHK Pie
st.markdown("---")
st.header("🏠 BHK Pie Chart")

location_options = new_df['location'].unique().tolist()
location_options.insert(0, 'overall')
selected_location = st.selectbox('Select Location', location_options)

if selected_location == 'overall':
    fig_pie = px.pie(new_df, names='bedrooms', title='Overall Bedroom Distribution',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
else:
    fig_pie = px.pie(new_df[new_df['location'] == selected_location],
                     names='bedrooms',
                     title=f'Bedroom Distribution in {selected_location}',
                     color_discrete_sequence=px.colors.qualitative.Pastel)

fig_pie.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie)

# Section: Box Plot
st.markdown("---")
st.header("🏢 Side-by-Side BHK Price Comparison")

fig_box = px.box(
    new_df[new_df['bedrooms'] <= 4],
    x='bedrooms',
    y='price',
    title='BHK Price Range'
)
fig_box.update_layout(
    font=dict(family="Arial", size=14, color="white"),
    paper_bgcolor='rgba(0, 0, 0, 0.8)',
    plot_bgcolor='rgba(0, 0, 0, 0.8)',
    title_font=dict(size=20, color='white')
)
fig_box.update_traces(
    hovertemplate="<b>Bedrooms:</b> %{x}<br><b>Price:</b> ₹%{y:.2f} Crore<extra></extra>",
    marker=dict(color='rgba(0, 123, 255, 0.6)', line=dict(color='rgba(0, 123, 255, 1.0)', width=1))
)
st.plotly_chart(fig_box)

# Section: Feature-wise Bar Chart
st.markdown("---")
st.header("📊 Feature-wise Price Comparison")

column_display_names = {
    'bedrooms': 'Bedrooms',
    'bathrooms': 'Bathrooms',
    'balconies': 'Balconies',
    'facing': 'Facing',
    'age_of_property': 'Age of Property',
    'furnishing_status': 'Furnishing Status',
    'flooring_type': 'Flooring Type',
    'parking_space': 'Parking Space',
    'study_room': 'Study Room',
    'servant_room': 'Servant Room',
    'storage_room': 'Storage Room',
    'pooja_room': 'Pooja Room',
    'others': 'Others',
    'location': 'Location',
    'floor_category': 'Floor Category',
    'luxury_category': 'Luxury Category'
}

selected_option = st.selectbox("Select a feature", list(column_display_names.values()))
selected_column = [key for key, value in column_display_names.items() if value == selected_option][0]
calculation_type = st.radio("Select calculation type", ['Mean', 'Median'])

agg_df = new_df.groupby(selected_column)['price'].mean().reset_index() if calculation_type == 'Mean' else new_df.groupby(selected_column)['price'].median().reset_index()

fig_bar = px.bar(
    agg_df,
    x=selected_column,
    y='price',
    title=f"{calculation_type} Price by {selected_option}",
    labels={'price': f'{calculation_type} Price', selected_column: selected_option}
)
fig_bar.update_layout(
    font=dict(family="Arial", size=14, color="white"),
    paper_bgcolor='rgba(0, 0, 0, 0.8)',
    plot_bgcolor='rgba(0, 0, 0, 0.8)',
    title_font=dict(size=20, color='white'),
)
fig_bar.update_traces(
    hovertemplate=f"<b>{selected_option}:</b> %{{x}}<br><b>Price:</b> ₹%{{y:.2f}} Crore<br><extra></extra>"
)
st.plotly_chart(fig_bar)

st.markdown("---")
