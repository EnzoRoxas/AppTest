import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from newspaper import Article
import io
import nltk
import spacy
import pytextrank
import torch
from transformers import PegasusForConditionalGeneration 
from transformers import PegasusTokenizer
from transformers import pipeline
import re
import nltk
from nltk.tokenize import sent_tokenize


#nltk.download('punkt')

#model_dir = "\Users\romer\OneDrive\Documents\Angelo\Project_News\pegasus_newstrained"

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe("textrank")


st.set_page_config(page_title='INFONest🇵🇭: Get the News!📰', page_icon='./Meta/newspaper1.ico')

@st.cache_resource
def punkt_load():
    return nltk.download('punkt')

punkt = punkt_load()

@st.cache_resource
def stopwords_load():
    nltk.download('stopwords')
    stop_words = nltk.corpus.stopwords.words("english")#set(stopwords.words('english'))
    stop_words = stop_words + ['hi', 'im', 'hey']
    return stop_words

stop_words = stopwords_load()

@st.cache_resource
def pegasus_tokenizer_load():
    pegasus_tokenizer = PegasusTokenizer.from_pretrained("./pegasus_newstrained")
    return pegasus_tokenizer

#pegasus_tokenizer = pegasus_tokenizer_load()

@st.cache_resource
def pegasus_model_load():
    pegasus_model = PegasusForConditionalGeneration.from_pretrained("./pegasus_newstrained", use_safetensors=True)
    return pegasus_model

#pegasus_model = pegasus_model_load()

def fetch_news_search_topic(topic):
    site = 'https://news.google.com/news/rss/search/section/q/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list

@st.cache_resource
def fetch_top_news():
    site = 'https://news.google.com/news/rss?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_top_news()

def fetch_category_news(topic):
    site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)

    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list

@st.cache_resource
def fetch_category_news_WORLD():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/WORLD?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_WORLD()

@st.cache_resource
def fetch_category_news_NATION():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/NATION?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_NATION()

@st.cache_resource
def fetch_category_news_BUSINESS():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_BUSINESS()

@st.cache_resource
def fetch_category_news_TECHNOLOGY():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/TECHNOLOGY?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_TECHNOLOGY()

@st.cache_resource
def fetch_category_news_ENTERTAINMENT():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/ENTERTAINMENT?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_ENTERTAINMENT()

@st.cache_resource
def fetch_category_news_SPORTS():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/SPORTS?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_SPORTS()

@st.cache_resource
def fetch_category_news_SCIENCE():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/SCIENCE?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_SCIENCE()

@st.cache_resource
def fetch_category_news_HEALTH():
    #site = 'https://news.google.com/news/rss/headlines/section/topic/{}?hl=en&gl=PH&ceid=PH%3Aen'.format(topic)
    site = 'https://news.google.com/news/rss/headlines/section/topic/HEALTH?hl=en&gl=PH&ceid=PH%3Aen'
    op = urlopen(site)  # Open that site
    rd = op.read()  # read data from site
    op.close()  # close the object
    sp_page = soup(rd, 'xml')  # scrapping data from site
    news_list = sp_page.find_all('item')  # finding news
    return news_list
news_list = fetch_category_news_HEALTH()

def fetch_news_poster(poster_link):
    try:
        u = urlopen(poster_link)
        raw_data = u.read()
        image = Image.open(io.BytesIO(raw_data))
        st.image(image, use_column_width=True)
    except:
        image = Image.open('./Meta/no_image.jpg')
        st.image(image, use_column_width=True)

@st.cache_data(ttl=None, max_entries=80)
def txtCleaning(cleanT):
    #cleanT = cleanT.lower()
    #cleanT = re.sub(r'\d+', '', cleanT)#remove digits
    cleanT = re.sub(r"(@\[A-Za-z0-9]+)|(\w+:\/\/\S+)|^rt|http.+?", "", cleanT)#remove links
    cleanT = re.sub(r'[^a-zA-Z0-9\s, .\r\n-]+', '', cleanT)#remove @#$%^&
    #cleanT = re.sub("\s\s+", " ", cleanT)#remove extra spaces

    #sentence tokenization
    sentencetoken = sent_tokenize(cleanT)

    #remove stopwords
    filtered_sentence = [w for w in sentencetoken if not w.lower() in stop_words]
    filtered_sentence = []

    for w in sentencetoken:
        if w not in stop_words:
            filtered_sentence.append(w)

    cleanedtxt = ' '.join([str(elem) for elem in filtered_sentence])
    return cleanedtxt

@st.cache_data(ttl=None, max_entries=80)
def summaryTxtR(sumT):
    txtSum =[]
    doc = nlp(sumT)
    for sent in doc._.textrank.summary(limit_sentences = 6):
        txtSum.append(sent)

    txtSummary = ' '.join([str(elem) for elem in txtSum])

    return txtSummary



@st.cache_data(ttl=None, max_entries=80)
def pegasus(txtR):
    summary = summaryTxtR(txtR)
    tPegasus= pegasus_tokenizer_load()
    pModel = pegasus_model_load()
    tokens = tPegasus(summary, truncation=True, padding="longest", return_tensors="pt")
    encoded_summary = pModel.generate(**tokens)
    decoded_summary = tPegasus.decode(
      encoded_summary[0],
      skip_special_tokens=True)

    return decoded_summary  

#pegasus_tokenizer = pegasus_tokenizer_load()
#pegasus_model = pegasus_model_load()

def display_news(list_of_news, news_quantity):
    c = 0

    for news in list_of_news:
        c += 1
        #st.markdown(f"({c})[ {news.title.text}]({news.link.text})")
        st.write('**({}) {}**'.format(c, news.title.text))
        news_data = Article(news.link.text) #link/url
        
        try:   
            news_data.download()
            news_data.parse()
            news_data.nlp()
            __text = news_data.text
            txtcleaned = txtCleaning(__text)
            sum=summaryTxtR(txtcleaned)
            sumP = pegasus(sum)
                  
        except Exception as e:
            st.error(e)
           
        fetch_news_poster(news_data.top_image)  
        with st.expander(news.title.text):
            st.markdown(
                '''<h6 style='text-align: justify;'>{}"</h6>'''.format(sumP),
                unsafe_allow_html=True)
            st.markdown("[Read more at {}...]({})".format(news.source.text, news.link.text))
        st.success("Published Date: " + news.pubDate.text)
        if c >= news_quantity:
            break

def run():
    st.title("INFONest🇵🇭: Get The News!📰")
    image = Image.open('./Meta/newspaper2.png')

    col1, col2, col3 = st.columns([3, 5, 3])

    with col1:
        st.write("")

    with col2:
        st.image(image, use_column_width=False)

    with col3:
        st.write("")
    category = ['--Select--', 'Top News!🌍', 'Hot Topics!📝', 'Search🔍']
    cat_op = st.selectbox('Please Select:', category)
    if cat_op == category[0]:
        st.warning('Please Select Type!')
    elif cat_op == category[1]:
        st.subheader("✅ Here Are the Top News!🌍 For You")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
        news_list = fetch_top_news()
        display_news(news_list, no_of_news)
    elif cat_op == category[2]:
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE',
                     'HEALTH']
        st.subheader("Choose a Topic!")
        chosen_topic = st.selectbox("Select One!", av_topics)
        if chosen_topic == av_topics[0]:
            st.warning("Please Choose a Category")
        elif chosen_topic == av_topics[1]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_WORLD()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic)) 
        elif chosen_topic == av_topics[2]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_NATION()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[3]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_BUSINESS()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[4]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_TECHNOLOGY()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[5]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_ENTERTAINMENT()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[6]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_SPORTS()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[7]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_SCIENCE()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))
        elif chosen_topic == av_topics[8]:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news_HEALTH()
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))            
        else:
            no_of_news = st.slider('Number of News:', min_value=5, max_value=25, step=1)
            news_list = fetch_category_news(chosen_topic)
            if news_list:
                st.subheader("✅ Here Are The {} News For You".format(chosen_topic))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(chosen_topic))    

    elif cat_op == category[3]:
        user_topic = st.text_input("Enter Your Topic🔍")
        no_of_news = st.slider('Number of News:', min_value=5, max_value=15, step=1)

        if st.button("Search") and user_topic != '':
            user_topic_pr = user_topic.replace(' ', '')
            news_list = fetch_news_search_topic(topic=user_topic_pr)
            if news_list:
                st.subheader("✅ Here The {} News For You".format(user_topic.capitalize()))
                display_news(news_list, no_of_news)
            else:
                st.error("No News Found For {}".format(user_topic))
        else:
            st.warning("Please Write the Topic Name to Search🔍")

run()
#streamlit run appTest.py
