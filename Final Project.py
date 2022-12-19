'''
Tyler Steed
Skyscraper Central
December 18, 2022
'''

import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


st.set_page_config(layout="centered")


def load_data(filename):
    global load_data
    skyscraper_data = pd.read_csv(filename)
    return skyscraper_data


def main():
    global sky_data
    sky_data = load_data('Final Project/Skyscrapers2021.csv')
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Select Page to View:", ["Home Page", "Data", "Data Filtered by City", "Data Filtered by Year and Number of Floors", "Map of Skyscrapers", "Skyscraper Distribution by Year of Completion", "Frequency of Cities in Top 100", "Floor Statistics"])
    if page == "Home Page":
        home_page()
    if page == "Data":
        sort_skyscrapers()
    if page == "Data Filtered by City":
        filtered_city()
    if page == "Data Filtered by Year and Number of Floors":
        filtered_comp()
    if page == "Map of Skyscrapers":
        sky_map()
    if page == "Skyscraper Distribution by Year of Completion":
        sky_scatter()
    if page == "Frequency of Cities in Top 100":
        sky_pie()
    if page == "Floor Statistics":
        piv_table()


def home_page():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: center;">Skyscraper Central</p>'
    st.markdown(title, unsafe_allow_html=True)
    image1 = Image.open("Final Project/dubai.png")
    st.image(image1, width=700, caption="Burj Khalifa - the largest skyscraper in the world, located in Dubai")
    about_subheader = '<p style="font-family:Futura; color:Orange; font-size: 25px; text-align: left;">About Skyscraper Central</p>'
    st.markdown(about_subheader, unsafe_allow_html=True)
    about_description = '<p style="font-family:Futura; font-size:15px; text-align:left;">Skyscraper Central is home to pertinent information regarding the one hundred tallest skyscrapers in the world. Find data based on custom search criteria, view these skyscrapers on a map, or view different data shown in various charts. Whatever information you are looking for, find it here on Skyscraper Central.</p>'
    st.markdown(about_description, unsafe_allow_html=True)
    use_subheader = '<p style="font-family:Futura; color:Orange; font-size: 25px; text-align: left;">How to use this database</p>'
    st.markdown(use_subheader, unsafe_allow_html=True)
    use_description = '<p style="font-family:Futura; font-size: 15px; text-align: left;">Skyscraper Central has different page layout options that can be found in the navigation side bar. Select a page to view by choosing from the drop down select box.</p>'
    st.markdown(use_description, unsafe_allow_html=True)


def sort_skyscrapers():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Skyscraper Data</p>'
    st.markdown(title, unsafe_allow_html=True)
    criteria = st.sidebar.selectbox("Sort by:", ["RANK", "NAME", "CITY", "Full Address", "Latitude", "Longitude", "COMPLETION", "Height", "Floors", "MATERIAL", "FUNCTION"])
    df1 = list(sky_data.columns)
    df2 = st.sidebar.multiselect("Select Data to Include:", df1)
    order = st.sidebar.selectbox("Ascending/Descending:", ["", "Ascending", "Descending"])
    if order == "Ascending":
        order = True
    else:
        order = False
    sorted_data = sky_data.sort_values(by=[criteria], ascending=order)
    st.write(sorted_data[df2])


def filtered_city():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Skyscraper Data Filtered by City</p>'
    st.markdown(title, unsafe_allow_html=True)
    city = st.sidebar.selectbox("Select City:", ['Abu Dhabi', 'Beijing', 'Busan', 'Changsha', 'Chicago', 'Chongqing', 'Dalian', 'Dubai', 'Guangzhou', 'Guiyand', 'Ho Chi Minh City', 'Hong Kong', 'Jinan', 'Kaohsiung', 'Kaohsiung', 'Kuala Lumpur', 'Kunming', 'Kuiwait City', 'Los Angeles', 'Mecca', 'Moscow', 'Nanjing', 'Nanning', 'New York City', 'Philadelphia', 'Seoul', 'Shanghai', 'Shenyang', 'Shenzhen', 'St. Petersburg', 'Suzhou', 'Taipei', 'Tianjin', 'Wuhan', 'Wuxi', 'Zhenjiang', 'Zhuhai'])
    data = sky_data[sky_data.CITY == city]
    st.write(data)


def filtered_comp():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Skyscraper Data Filtered by Year and Number of Floors</p>'
    df = pd.DataFrame(sky_data)
    st.markdown(title, unsafe_allow_html=True)
    year = st.sidebar.slider("Select Start Year:", min_value=1930, max_value=2022)
    floors = st.sidebar.slider("Select Minimum Number of Floors:", min_value=50, max_value=200)
    data = df[(df.COMPLETION >= year) & (df.FLOORS >= floors)]
    st.write(data)
    years_ago = [2022 - x for x in sky_data['COMPLETION']]
    header = '<p style="font-family:Futura; color:Orange; font-size: 20px; text-align: left;">How long ago was each skyscraper constructed?</p>'
    st.markdown(header, unsafe_allow_html=True)
    subheader = '<p style="font-family:Futura; font-size: 15px; text-align: left;">This list shows how long ago each skyscraper was constructed, relative to its index. For example, 0:12 means that Burj Khalifa, the tallest skyscraper (rank 1, index 0), was constructed 12 years ago.</p>'
    st.markdown(subheader, unsafe_allow_html=True)
    st.write(years_ago)


def sky_map():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align:left;">Skyscraper Map</p>'
    st.markdown(title, unsafe_allow_html=True)
    df = sky_data[["Latitude", "Longitude", "NAME"]]
    map = folium.Map(location=[df.Latitude.mean(), df.Longitude.mean()], zoom_start=3, tiles='OpenStreetMap')
    for index, location_info in df.iterrows():
        folium.Marker([location_info["Latitude"], location_info["Longitude"]], icon=folium.Icon(icon='building-o', prefix='fa', color='orange'), popup=location_info["NAME"]).add_to(map)
    st_map = st_folium(map, width=700, height=450)


def sky_scatter():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Skyscraper Distribution by Year of Completion</p>'
    st.markdown(title, unsafe_allow_html=True)
    df = pd.DataFrame(sky_data)
    fig, ax = plt.subplots(1,1)
    ax.scatter(x=df['RANK'], y=df['COMPLETION'], color='orange')
    ax.set_xlabel('Rank')
    ax.set_ylabel('Year of Completion')
    ax.set_title('Year of Completion for Each Skyscraper')
    plt.grid(True)
    st.pyplot(fig)


def sky_pie():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Frequency of Cities in Top 100</p>'
    st.markdown(title, unsafe_allow_html=True)
    df = pd.DataFrame(sky_data)
    pivot = df.pivot_table(columns=['CITY'], aggfunc='size')
    pie = df.pivot_table(columns=['CITY'], aggfunc='size').plot(kind='pie')
    plt.title('Frequency of City in Top 100')
    st.pyplot()
    st.write(pivot)


def piv_table():
    title = '<p style="font-family:Futura; color:Orange; font-size: 50px; text-align: left;">Floor Statistics</p>'
    st.markdown(title, unsafe_allow_html=True)
    index = st.sidebar.selectbox("Select Index:", ["Material", "Function"])
    if index == "Material":
        df = pd.DataFrame(sky_data)
        pivot = pd.pivot_table(df, index=['MATERIAL'], values=['FLOORS'], aggfunc={'min', np.mean, 'max', np.median})
        bar = pd.pivot_table(df, index=['MATERIAL'], values=['FLOORS'], aggfunc={'min', np.mean, 'max', np.median}).plot(kind='bar')
        st.write(pivot)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.xlabel('Material')
        plt.ylabel('Floors')
        plt.title('Min, Mean, Max, and Median Floors per Material Type', color='blue')
        plt.legend(loc='upper right')
        st.pyplot()
    else:
        df = pd.DataFrame(sky_data)
        pivot = pd.pivot_table(df, index=['FUNCTION'], values=['FLOORS'], aggfunc={'min', np.mean, 'max', np.median})
        bar = pd.pivot_table(df, index=['FUNCTION'], values=['FLOORS'], aggfunc={'min', np.mean, 'max', np.median}).plot(kind='bar')
        st.write(pivot)
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.xlabel('Function')
        plt.ylabel('Floors')
        plt.title('Min, Mean, Max, and Median Floors per Function', color='blue')
        plt.legend(loc='upper right')
        st.pyplot()


if __name__ == "__main__":
    main()


#References
#https://docs.streamlit.io/
#https://matplotlib.org/stable/tutorials/introductory/pyplot.html
#https://pandas.pydata.org/docs/user_guide/index.html
#https://python-visualization.github.io/folium/
