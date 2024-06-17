import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os
import warnings
warnings.filterwarnings('ignore')



# Dashboard title
st.title(" :bar_chart: Customer Churn Dashboard")
# Add CSS for animation
st.write("""
    <style>
        @keyframes zoom-in {
            0% {
                transform: scale(0);
            }
            100% {
                transform: scale(1);
            }
        }
        .zoom-in-animation {
            animation: zoom-in 1.5s ease-in-out;
        }
    </style>
""", unsafe_allow_html=True)

# Add an animated text
st.write('<div class="zoom-in-animation"><h3>Delve into the comprehensive Customer Churn Insights!</h3></div>', unsafe_allow_html=True)

# # Overview Section
# st.header("Overview")
# st.markdown("""
# This dashboard provides insights into customer churn data, helping you understand the factors influencing churn and make data-driven decisions to improve customer retention.
# """)



# Load your dataset
data = pd.read_csv('Data/train.csv')


# Filters
st.sidebar.subheader(" Dashboard Filters")

# Create for Gender
gender = st.sidebar.multiselect("Pick your Gender", data["gender"].unique())
if not gender:
    filtered_data = data.copy()
else:
    filtered_data = data[data["gender"].isin(gender)]

# Create for payment type
paymentmethod = st.sidebar.multiselect("Pick your Payment Method", data["paymentmethod"].unique())
if paymentmethod:
    filtered_data = filtered_data[filtered_data["paymentmethod"].isin(paymentmethod)]

# Create for Contract type
contract = st.sidebar.multiselect("Pick your Contract", data["contract"].unique())
if contract:
    filtered_data = filtered_data[filtered_data["contract"].isin(contract)]


def eda_dash():
    # Add CSS for EDA title animation
    st.write("""
        <style>
            @keyframes zoom-in {
                0% {
                    transform: scale(0);
                }
                100% {
                    transform: scale(1);
                }
            }
            .zoom-in-animation {
                animation: zoom-in 1.5s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)

    # Add an animated text
    st.write('<div class="zoom-in-animation"><h3>Eploratory Data Analysis!</h3></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        scatter_plot = px.scatter(data, x='tenure', y='monthlycharges', title='Scatter Plot',)
        st. plotly_chart(scatter_plot)

    with col2:
        charges_hist= px.histogram(data, x='monthlycharges')
        st.plotly_chart(charges_hist)

    # Churn by monthly charges
    st.subheader("Churn by Monthly Charges")
    fig = px.histogram(filtered_data, x="monthlycharges", color="churn", marginal="box", nbins=50, title="Churn by Monthly Charges")
    st.plotly_chart(fig)

def kpi_dash():
        # Add CSS for EDA title animation
    st.write("""
        <style>
            @keyframes zoom-in {
                0% {
                    transform: scale(0);
                }
                100% {
                    transform: scale(1);
                }
            }
            .zoom-in-animation {
                animation: zoom-in 1.5s ease-in-out;
            }
        </style>
    """, unsafe_allow_html=True)
    # Add an animated text
    st.write('<div class="zoom-in-animation"><h3>Key Performance Indicators!</h3></div>', unsafe_allow_html=True)

    total_customers = len(filtered_data)
    churned_customers = (filtered_data['churn'] == 'Yes').sum()
    churn_rate = (churned_customers / total_customers) * 100
    avg_monthly_charge = filtered_data['monthlycharges'].mean()
    avg_total_charge = filtered_data['totalcharges'].mean()
    avg_tenure = filtered_data['tenure'].mean()

    # Define CSS for card visuals with background color and drop shadow
    st.write("""
        <style>
            .kpi-card {
                background-color: #ebf7ff; /* Fading sky blue */
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Shadow effect */
                margin-bottom: 20px;
                width: 300px; /* Set a fixed width for consistency */
                display: inline-block;
                margin-right: 20px;
            }
            .kpi-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .kpi-value {
                font-size: 24px;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display KPIs as card visuals with background color and drop shadow
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Customers 👫</div><div class='kpi-value'>{total_customers}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Churned Customers 🏃‍♂️</div><div class='kpi-value'>{churned_customers}</div></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Churn Rate 📈</div><div class='kpi-value'>{churn_rate:.2f}%</div></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Monthly Charge</div><div class='kpi-value'>${avg_monthly_charge:.2f}</div></div>", unsafe_allow_html=True)

    with col5:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Total Charge</div><div class='kpi-value'>${avg_total_charge:.2f}</div></div>", unsafe_allow_html=True)

    with col6:
        st.markdown(f"<div class='kpi-card'><div class='kpi-title'>Avg Tenure (months)</div><div class='kpi-value'>{avg_tenure:.2f}</div></div>", unsafe_allow_html=True)


    # Visualization section
    st.header("Home")

    # Example visualization: Distribution of churn
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution of Churn")
        churn_counts = filtered_data['churn'].value_counts()
        # Create the pie chart
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(churn_counts, labels=churn_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
        st.pyplot(fig)

    with col2:
        st.subheader("Churn by Contract")
        # Create the donut chart
        contract_churn_counts = filtered_data.groupby(['contract', 'churn']).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax.pie(contract_churn_counts.sum(axis=1), labels=contract_churn_counts.index, autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))

        # Create the inner pie chart
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
        st.pyplot(fig)

    # Example visualization: Churn by payment method
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Churn by Payment Method")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="churn", hue="paymentmethod")
        st.pyplot(fig)

    # Example visualization: Churn by contract
    with col2:
        st.subheader("Churn by Contract")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="churn", hue="contract")
        st.pyplot(fig)



    # Comparative Bar Graphs
    st.header("Distribution of Churn by Demography")
    col1, col2 = st.columns(2)
    with col1:
        # Churn by Partner
        st.subheader("Churn by Partner")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="partner", hue="churn")
        st.pyplot(fig)
    
    with col2:
        # Churn by Dependents
        st.subheader("Churn by Dependents")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="dependents", hue="churn")
        st.pyplot(fig)


    # Churn by Senior Citizen
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Churn by Senior Citizen")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="seniorcitizen", hue="churn")
        st.pyplot(fig)

    # Example visualization: Churn by gender
    with col2:
        st.subheader("Churn by Gender")
        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="churn", hue="gender")
        st.pyplot(fig)

    # Additional Comparative Bar Graphs
    st.header("Churn Ditribution by Service Usage")

    col1, col2 = st.columns(2)
    with col1:
        # OnlineBackup vs InternetService vs Churn
        st.subheader("OnlineBackup vs InternetService vs Churn")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="onlinebackup", hue="churn", palette="Set1",
                        order=filtered_data["onlinebackup"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)

    with col2:
        # Phone Service vs MultipleLines vs Churn
        st.subheader("Phone Service vs MultipleLines vs Churn")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="phoneservice", hue="churn", palette="Set2",
                        order=filtered_data["phoneservice"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:    
        # Churn by Streaming Movies
        st.subheader("Churn by Streaming Movies")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="streamingmovies", hue="churn", palette="Set3",
                        order=filtered_data["streamingmovies"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)

    with col2: 
        # Churn by Online Security
        st.subheader("Churn by Online Security & InternetService")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="onlinesecurity", hue="churn", palette="Set1",
                        order=filtered_data["internetservice"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
    # Churn by Paperless Billing
        st.subheader("Churn by Paperless Billing")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="paperlessbilling", hue="churn", palette="Set2",
                        order=filtered_data["paperlessbilling"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)

    with col2:
    # Churn by Streaming TV
        st.subheader("Churn by Streaming TV")
        fig = plt.figure(figsize=(10, 6))
        ax = sns.countplot(data=filtered_data, x="streamingtv", hue="churn", palette="Set3",
                        order=filtered_data["streamingtv"].value_counts().index)
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 1), 
                        textcoords='offset points')
        st.pyplot(fig)



if __name__ == "__main__":
    col1, col2, = st.columns(2)
    with col1:
        # Overview Section
        st.header("Overview")
        st.markdown("""
        This dashboard provides insights into customer churn data, helping you understand the factors influencing churn and make data-driven decisions to improve customer retention.
        """)
    with col2:
        st.selectbox('Select the type of dashboard', options=['EDA', 'KPI'], key='selected_dashboard_type')

    if st.session_state['selected_dashboard_type'] == 'EDA':
        eda_dash()
    else:
        kpi_dash()    