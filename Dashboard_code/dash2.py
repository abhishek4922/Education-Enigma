# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load PTR Data
ptr_data = pd.read_csv('C:/Users/abhis/Desktop/no/LLAMAINDEX_COURSE/Data_set.csv')

# Strip spaces from column names to avoid errors
ptr_data.columns = ptr_data.columns.str.strip()

# Set 'India/State /UT' as the index
ptr_data.set_index('India/State /UT', inplace=True)

# Remove the 'India' row if it exists
ptr_data = ptr_data.drop(index='India', errors='ignore')

# Define lists for states and union territories
indian_states = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa',
    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
    'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
    'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'
]
union_territories = [
    'Andaman and Nicobar', 'Chandigarh', 'Dadra and Daman', 'Delhi',
    'Lakshadweep', 'Puducherry', 'Jammu and Kashmir', 'Ladakh'
]

# Define education levels for the stacked bar chart
education_levels = [
    'Pupil Teacher Ratio (PTR) - Primary (1 to 5)',
    'Pupil Teacher Ratio (PTR) - Upper Primary (6-8)',
    'Pupil Teacher Ratio (PTR) - Secondary (9-10)',
    'Pupil Teacher Ratio (PTR) - Higher Secondary (11-12)'
]

# Function to plot PTR chart
def plot_ptr(data, title):
    fig, ax = plt.subplots(figsize=(12, 8))
    bottoms = pd.Series([0] * len(data.index), index=data.index)
    for level in education_levels:
        ax.bar(data.index, data[level], label=level, bottom=bottoms)
        bottoms += data[level]
    ax.set_xlabel('State/UT', fontsize=12)
    ax.set_ylabel('Pupil Teacher Ratio (PTR)', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.set_xticklabels(data.index, rotation=90, fontsize=10)
    ax.legend(loc='upper right')
    plt.tight_layout()
    return fig

# Load Enrollment Data
enrollment_data = pd.read_csv('enrolment_age_2019_20.csv')
enrollment_data['total_enrollment'] = enrollment_data.filter(regex='class.*').sum(axis=1)

# Group and separate data for enrollment
state_enrollment = enrollment_data.groupby('state_name')['total_enrollment'].sum().reset_index()
state_enrollment = state_enrollment.sort_values(by='total_enrollment', ascending=True)
states_enrollment = state_enrollment[state_enrollment['state_name'].isin(indian_states)]
uts_enrollment = state_enrollment[state_enrollment['state_name'].isin(union_territories)]

# Streamlit app with sidebar navigation
st.title("Education Dashboard")

# Sidebar for selecting the analysis type
analysis_type = st.sidebar.selectbox("Select Analysis Type", ["PTR Analysis", "Enrollment Analysis"])

if analysis_type == "PTR Analysis":
    st.header("Pupil Teacher Ratio (PTR) Analysis")
    region = st.selectbox('Select Region', ['States', 'UTs'])
    if region == 'States':
        filtered_ptr_data = ptr_data[ptr_data.index.isin(indian_states)]
        title = 'PTR Across States by Education Level'
    else:
        filtered_ptr_data = ptr_data[ptr_data.index.isin(union_territories)]
        title = 'PTR Across Union Territories by Education Level'
    if filtered_ptr_data.empty:
        st.write("No data available for the selected region.")
    else:
        fig = plot_ptr(filtered_ptr_data, title)
        st.pyplot(fig)

elif analysis_type == "Enrollment Analysis":
    st.header("Enrollment Analysis")
    st.subheader("Total Enrollment by Indian States")
    fig_states = plt.figure(figsize=(10, 6))
    sns.barplot(data=states_enrollment, y='state_name', x='total_enrollment', color='green')
    plt.title('Total Enrollment by Indian States')
    plt.xlabel('Total Enrollment')
    plt.ylabel('State')
    st.pyplot(fig_states)

    st.subheader("Total Enrollment by Union Territories")
    fig_uts = plt.figure(figsize=(8, 6))
    sns.barplot(data=uts_enrollment, y='state_name', x='total_enrollment', color='red')
    plt.title('Total Enrollment by Union Territories')
    plt.xlabel('Total Enrollment')
    plt.ylabel('Union Territory')
    st.pyplot(fig_uts)

    # st.subheader("Combined Enrollment Distribution")
    # fig_combined = plt.figure(figsize=(12, 8))
    # sns.histplot(enrollment_data['total_enrollment'], kde=True, color='blue', bins=30)
    # plt.title('Enrollment Distribution Across All States and Union Territories')
    # plt.xlabel('Total Enrollment')
    # plt.ylabel('Frequency')
    # st.pyplot(fig_combined)
