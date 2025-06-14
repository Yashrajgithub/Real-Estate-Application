import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path

# Load data
path_1 = Path('datasets/page_2/Recomendation_system_final_data.xls')
joined_df = pd.read_csv(path_1)

path_2 = Path('datasets/page_2/cosine_sim_by_near_by_locations.pkl')
cosine_sim_by_near_by_locations = pd.read_pickle(path_2)

path_3 = Path('datasets/page_2/cosine_sim_facility_based.pkl')
cosine_sim_facility_based = pd.read_pickle(path_3)

path_4 = Path('datasets/page_2/cosine_sim_property_inof_based.pkl')
cosine_sim_property_inof_based = pd.read_pickle(path_4)

# Prepare property list and image
unique_properties = joined_df['society_name'].unique()
image_path = Path("datasets/page_2/img.jpg")
image = Image.open(image_path)

# Custom CSS Styling
st.markdown("""
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #2E8B57;
}
.sidebar .sidebar-content {
    background-color: #f5f5f5;
    padding: 10px;
}
.stButton>button {
    background-color: #2E8B57;
    color: white;
    font-size: 16px;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
}
.stButton>button:hover {
    background-color: #267347;
}
.reset-button {
    background-color: #FFFFFF;
    color: #2E8B57;
    border: 1px solid #2E8B57;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    padding: 0;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.write("<span style='color:#FFD700'><strong>ℹ️ Use the dropdown above to switch pages</strong></span>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.header("🔍 System Info")
st.sidebar.markdown("""
- **How It Works:** Recommendations are based on cosine similarity.
- **Sources:** Property data from dataset.
- **Verification:** Cross-check details below for accuracy.
""")

# Header
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
        🏠 <span class="gradient-text">Property Recommendation System</span>
    </h1>
""", unsafe_allow_html=True)
st.image(image.resize((750, 400)))

# Guidelines
st.markdown("### 📌 How to Use")
st.markdown("""
1. Choose a society name from the list.
2. Select the type of recommendation:
   - **Nearby Locations** – Based on geography.
   - **Facility Based** – Amenities and features.
   - **Property Info Based** – Price, size, etc.
   - **Combined** – Uses all above factors.
3. Click **Recommend** to get results.
4. See detailed data of the results below.
""")

# Inputs
unique_properties_title_case = [prop.title() for prop in unique_properties]
property_name = st.selectbox("🏠 Select Society Name", unique_properties_title_case, index=1)

option_display = {
    "nearby_locations": "Nearby Locations",
    "facility_based": "Facility Based",
    "property_info_based": "Property Info Based",
    "auto": "Combined"
}
option_choice = st.selectbox("📊 Recommendation Type", list(option_display.values()), index=0)
option = [key for key, value in option_display.items() if value == option_choice][0]

# Recommendation Function
def recommend_properties(property_name, option, n=5):
    idx = joined_df.index[joined_df['society_name'] == property_name.lower()].tolist()[0]

    if option == "nearby_locations":
        cosine_sim_matrix = cosine_sim_by_near_by_locations
    elif option == "facility_based":
        cosine_sim_matrix = cosine_sim_facility_based
    elif option == "property_info_based":
        cosine_sim_matrix = cosine_sim_property_inof_based
    else:
        cosine_sim_matrix = (
            0.8 * cosine_sim_property_inof_based +
            0.6 * cosine_sim_facility_based +
            1.0 * cosine_sim_by_near_by_locations
        )

    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
    property_indices = [i[0] for i in sim_scores]

    recommendations_df = pd.DataFrame({
        '🏢 Property': joined_df['society_name'].iloc[property_indices],
        '🔗 Similarity (%)': [round(score[1]*100, 2) for score in sim_scores]
    })

    return recommendations_df, property_indices

# Recommend Button
if st.button("🔍 Recommend"):
    recommendations, indices = recommend_properties(property_name, option)
    st.success("Here are the top recommendations:")
    st.dataframe(recommendations, use_container_width=True)

    # Detailed Info
    st.subheader("📄 Property Details")
    if option == "facility_based":
        cols = ['society_name', 'property_name', 'features', 'link']
    elif option == "nearby_locations":
        cols = ['society_name', 'property_name', 'place', 'nearby_locations', 'link']
    elif option == "property_info_based":
        cols = ['society_name', 'property_name', 'property_type', 'price', 'bedrooms', 'built_up_area',
                'bathrooms', 'balconies', 'age_possession', 'furnish_label', 'parking_availability',
                'luxury_score', 'link']
    else:
        cols = ['society_name', 'place', 'property_name', 'price', 'bedrooms', 'price_per_sqft',
                'property_type', 'age_possession', 'furnish_label', 'features', 'link']

    details_df = joined_df.iloc[indices][cols]
    st.dataframe(details_df, use_container_width=True)

# Reset Button
reset_placeholder = st.empty()
if reset_placeholder.button('↺ Reset'):
    st.rerun()
