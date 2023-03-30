import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plost
import requests
from bs4 import BeautifulSoup


st.set_page_config(layout='wide',initial_sidebar_state='expanded')

# Hide hurmburger Menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style',unsafe_allow_html=True)

st.sidebar.markdown("""---""")
st.sidebar.subheader('Dashboard ')

# 1. Sidebar Menu
with st.sidebar:
    selected=option_menu(
        menu_title="Main Menu",
        options=["Dashboard","Web Scrapping","Analytics"],
        default_index=0,
    )
if selected=="Dashboard":
    #st.title(f"Welcome To {selected} Page")
    st.sidebar.markdown("""---""")
    #st.markdown("""---""")
    st.sidebar.subheader('Heat map parameter')
    time_hist_color=st.sidebar.selectbox('Color by',('temp_min','temp_max'))

    st.sidebar.subheader('Donut chart parameter')
    donut_theta=st.sidebar.selectbox('Select data',('q2','q3'))

    st.sidebar.subheader('Line chart parameter')
    plot_data=st.sidebar.multiselect('Select data',['temp_min','temp_max'],['temp_min', 'temp_max'])
    plot_height=st.sidebar.slider('Specify plot height',-200,500,250)
    
    st.sidebar.markdown("<br>",unsafe_allow_html=True)

    #Row A
    st.markdown("<h3 style='text-align: center; color: #ff8c00;'>Metrics</h3>", unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    col1.metric("Temperature","80 °F","5°F")
    col2.metric("Wind","9 mph","-8%")
    col3.metric("Humidity","86%","4%")

    # Row B
    seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
    stocks = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/data/master/stocks_toy.csv')
    
    c1,c2=st.columns((7,3))
    with c1:
        st.markdown("<h3 style='text-align: center; color: #ff8c00;'>Heatmap</h3>", unsafe_allow_html=True)
        plost.time_hist(
            data=seattle_weather,
            date='date',
            x_unit='week',
            y_unit='day',
            color=time_hist_color,
            aggregate='median',
            legend=None,
            height=345,
            use_container_width=True
        )
    with c2:
        st.markdown("<h3 style='text-align: center; color: #ff8c00;'>Donut Chart</h3>", unsafe_allow_html=True)
        plost.donut_chart(
            data=stocks,
            theta=donut_theta,
            color='company',
            legend='button',
            use_container_width=True
        )
    
    # Row C
    st.markdown("<h3 style='text-align: center; color: #ff8c00;'>Line Chart</h3>", unsafe_allow_html=True)
    st.line_chart(seattle_weather,x='date',y=plot_data,height=plot_height)
elif selected=="Analytics":
    st.title(f"Welcome To {selected} Page")
else :
    st.markdown("<h1 style='text-align: center; color: #ff8c00;'>Web Scrapping</h1>", unsafe_allow_html=True)
    tag=st.selectbox('Choose a topic',['love','humor','life','books','inspirational','reading','friendship','friends','truth'])

    #BUTTON TO GENERATE CSV
    #generate = st.button('Download CSV')
    st.markdown("<h3 style='text-align: center; color: #ff8c00;'>Quotes</h3>", unsafe_allow_html=True)

   #ACCESS THE URL 
    url =f"https://quotes.toscrape.com/tag/{tag}/"
    res = requests.get(url)

    # USE BEAUTIFUL SOUP TO ACCESS THE CONTENT ON THE REQUESTED URL
    content =  BeautifulSoup(res.content,'html.parser')
    quotes = content.find_all('div',class_='quote')

    quote_file = []
    for quote in quotes:
        text = quote.find('span',class_ ='text').text
        author = quote.find('small',class_ = 'author').text
        link =  quote.find('a')
        st.markdown("""---""")
        st.success(text)
        st.markdown(f"<a href=https://quotes.toscrape.com{link['href']}>{author}</a>",unsafe_allow_html=True)
        st.code(f"https://quotes.toscrape.com{link['href']}")
        quote_file.append([text,author,link['href']])
    
    #if generate:
        try:
            df = pd.DataFrame(quote_file)
            df.to_csv('Quotes.csv',index=False,header=['Quote','Author','Link'],encoding='cp1252')  
        except: 
            st.write('Loading ...')
   
    def convert_df(data):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return data.to_csv(index=False).encode('cp1252')
    
    df = pd.DataFrame(quote_file)
    df.columns=['Quote','Author','Link']
    csv = convert_df(df)
    
    #df.to_csv('Quotes.csv',index=False,header=['Quote','Author','Link'],encoding='cp1252')  
    st.markdown("""---""")
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='Quotes.csv',
        mime='text/csv',
        )
    
    
st.sidebar.markdown('''Created by Khulekani Matsebula''')