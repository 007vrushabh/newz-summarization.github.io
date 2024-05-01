import streamlit as st #backend purpose 
from PIL import Image #PIL-->Python image Library --> as appln is dealing with images 
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen #fetch the data from the site 
from newspaper import Article #imp library --> for news summarization 
import io
import nltk #to download some packages 
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('corpus')

st.set_page_config(page_title='A Summarised News📰 Portal',page_icon='./Meta/newspaper.ico')


def fetch_news_search_topic(topic):
    site = 'https://news.google.com/rss/search?q={}'.format(topic) #*https://news.google.com/rss/search?q=india-->it will give all the news related to-->india 
    op = urlopen(site)  # Open -->site
    rd = op.read()  # read data --> site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data --> site
    news_list = sp_page.find_all('item')  # finding news
    return news_list


def fetch_top_news():
    site = 'https://news.google.com/news/rss'
    op = urlopen(site)  
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item') 
    return news_list


def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}'.format(topic) #fetch the topics --> topics is laready pre built
    op = urlopen(site)  
    rd = op.read()  
    op.close()  
    sp_page = soup(rd, 'xml')  
    news_list = sp_page.find_all('item')  
    return news_list


def fetch_news_poster(poster_link): #open url-->read data --> it is image--> not text-->io bytes --> in binary
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)  #use_column_width=True--> it will automatically adjust according to mobile, desktop 

    except:
        image = Image.open('./Meta/no_image.jpg')  #if url fails to get image then it will show --> no image found 
        st.image(image, use_column_width=True)  



def display_news(list_of_news, news_quantity):
    c = 0  #initial counter with zero
    
    #iterating through each news --> it should choose the firts counter i.e (1)-->after that title 
    for news in list_of_news:    
        c += 1
        st.write('**({}) {}**'.format(c, news.title.text)) #news.title --> to acces the title --> it should be in a text format

        news_data = Article(news.link.text)  #Article --> external library -->for news summarization --> get the link of the news --> download it -->automatically apply the NLP  --> if something wrong it will give error --> otherwise it will give the summarization 
        try:
            news_data.download()
            news_data.parse()
            news_data.nlp()
        except Exception as e:  
            st.error(e)
        fetch_news_poster(news_data.top_image) #article inbuilt method (top iamge)--> it will automatically find the news poster --> original news --> and it will give the url of a particular poster --> to display the poster we will be using function -->def fetch_news_poster(poster_link):

        with st.expander(news.title.text):  #st.expander-->1 module in streamlit-->firstly title should be visible --> after clicking on it --> summary should be display 
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(news_data.summary),unsafe_allow_html=True)  #it will display the summarize news--->format(news_data.summary)-->this summary is coming from ARTICLE
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text)) #original link of the source --> from source tag--> in the background it will pass the link

        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break


#*main UI Part 
def run():
    st.title("Automated Document Processing Using NLP : A Summarised News📰")
    image = Image.open('./Meta/newspaper.png')

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("") #left half empty

    with col2:
        st.image(image, use_column_width=False)#putting this image into-->center

    with col3:
        st.write("")#right half empty

    category = ['--Select--', 'Trending🔥 News', 'Favourite💙 Topics', 'Search🔍 Topic']

    cat_op = st.selectbox('Select your Category', category) #--> displaying the list into a selection box 

    #category op = category --> selection-->by default selection 
    if cat_op == category[0]: 
        st.warning('Please select Type!!')


    elif cat_op == category[1]:
        st.subheader("✅ Here is the Trending🔥 news for you")  #if car[1]-->then it will a message .....
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1) #step--> it should be increase by 1(5,6,7,..), or decrease by 1..

        news_list = fetch_top_news() #we are getting thi news list from the function -->def fetch_top_news():

        display_news(news_list, no_of_news) #-->require 2 parameter  


    elif cat_op == category[2]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Choose your favourite Topic")
        chosen_topic = st.selectbox("Choose your favourite Topic", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose the Topic")
        else:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(chosen_topic))



    elif cat_op == category[3]:
        user_topic = st.text_input("Enter your Topic🔍")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        #if someone clicking on SEARCH --> it call an API--> this API will require one topics --> def fetch_category_news(topic):topics will be netr by the user 
        if st.button("Search") and user_topic != '':  
            user_topic_pr = user_topic.replace(' ', '') #repalcing sapce with none --> space should not be there --> otherwise it would show an ERROR

            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here are the some {} News for you".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News found for {}".format(user_topic))
        else:
            st.warning("Please write Topic Name to Search🔍")

run()
