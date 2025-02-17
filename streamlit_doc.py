import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv('Startup_cleaned.csv')
def load_investor_details(investor):
    st.title(investor)
    last_5_df=df[df['investors'].str.contains(investor)].head()[['Date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last_5_df)
    col1,col2=st.columns(2)
    with col1:
        big_series=df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Big Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series=df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested in')
        fig1,ax1=plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    col3,col4=st.columns(2)
    with col3:
        round_series=df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Rounds Invested in')
        fig2,ax2=plt.subplots()
        ax2.pie(round_series,labels=round_series.index,autopct="%0.01f%%")
        st.pyplot(fig2)
    with col4:
        city_series=df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('Rounds Invested in')
        fig3,ax3=plt.subplots()
        ax3.pie(city_series,labels=city_series.index,autopct="%0.01f%%")
        st.pyplot(fig3)
    df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    st.dataframe(df.info())
    df['year']=df['Date'].dt.year
    year_series=df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    
    st.subheader('Year on Year sum')
    fig4,ax4=plt.subplots()
    ax4.plot(year_series)
    st.pyplot(fig4)
st.sidebar.title('Startup Funding Analysis')
bt=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

def load_overall_analysis():
    st.title('Overall Analysis')
    total=round(df['amount'].sum())
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric('Total',str(total),'Cr')
    with col2:
        max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max Funding',str(max_funding),'Cr')
    with col3:
        avg_funding=df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Funding',str(round(avg_funding)),'Cr')
    with col4:
        st.metric('Funded Startups',num_startups)
    df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    df['year']=df['Date'].dt.year
    df['month']=df['Date'].dt.month
    st.header('MOM Graph')
    selected_option=st.selectbox('Select Type',['Total','Count'])
    if selected_option=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    elif selected_option=='Count':
       temp_df=df.groupby(['year','month'])['amount'].count().reset_index() 
    
    temp_df['x_axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')

    fig5,ax5=plt.subplots()
    ax5.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig5)

if bt=='Overall Analysis':
   load_overall_analysis()
elif bt=='Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
    
elif bt=='Investor':
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
