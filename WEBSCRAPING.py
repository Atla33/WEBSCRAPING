#!/usr/bin/env python
# coding: utf-8

# In[22]:


#%pip install -U selenium
#%pip install webdriver-manager
#!pip install wordcloud


# In[23]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from gettext import find

import time


# In[2]:


options = webdriver.ChromeOptions()
options.add_argument('headless') # O mais importante, não renderiza parte gráfica
options.add_argument('window-size=1920x1080')


# In[44]:


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# In[45]:


def find(driver):
    element = driver.find_element(By.TAG_NAME, 'content')
    if element:
        return element
    else:
        return False


# In[46]:


url_1 = 'https://www.ufrn.br/imprensa/noticias/filtros?text=esporte#&page=1'
driver.get(url_1)
time.sleep(5)

quantPagC = driver.find_elements(By.XPATH, '//*[@id="noticias-paginacao"]/li[5]/a')[0];
quantPag = int(quantPagC.text)
print(quantPag)

text_to_cloud = ''

for j in range(quantPag):
    print('j: ', j) 
    
    #obtém lista de notícias (inclui 2 itens que não são notícias)
    title_news = driver.find_elements(By.CLASS_NAME, 'blue-link');
    n_news = len(title_news) #quantas notícias na página atual + 2
    print('n_news: ', n_news) #valor de fato diminuir 2
    
    #guarda todos os links de notícia da página atual
    title_news_hrefs = []
    for i in range(0, n_news):
        title_news_hrefs.append(title_news[i].get_attribute('href'))
        
    print('Conjunto de notícias desta página...')
    print('------------------------------------')
    for i in title_news_hrefs:
        print(i)
    
    print('-----Vou começar a raspagem de dados em cada notícia------')
    
    for i in range(1, len(title_news_hrefs)):
        link = title_news_hrefs[i]     
        if 'imprensa' in link:
            print(link)
            driver.get(link) #get all links  driver.get("http://www.google.com") https://selenium-python.readthedocs.io/navigating.html
            time.sleep(5)
            news_text = WebDriverWait(driver, 100).until(find)
            text_to_cloud += news_text.text
            driver.back()
            time.sleep(2)
        if i == len(title_news_hrefs) - 1: #se já leu a última notícia da página k, sinalizar para ir para k+1
            print('-------Terminei esta página, vou para a próxima página------')
            try:
                driver.find_element(By.XPATH, '//*[@id="noticias-paginacao"]/li[6]/a').click() #último elemento é o símbolo > de próxima página
                time.sleep(5)
                mudou = True
            except ex.NoSuchElementException:
                driver.refresh()
            
                    
print(text_to_cloud)


# In[61]:


from wordcloud import WordCloud, STOPWORDS

STOPWORDS = ['ver','principal','essa','vez','nas','mas',
             'qual','principal','ele','ter','doença','pois','este',
             'vez','ver principal','artigo principal','já',
             'aos','pode','outro','artigo','desse',
             'alguns','meio','entre','das','podem','esse',
             'seu','também','são','quando','de', 'que','em',
             'os','as','da','como','dos','ou','se','um','uma',
             'para','na','ao','mais','por','não','ainda','muito','sua',
             'a', 'é', 'o', 'e', 'no', 'do', 'com', 'à', 'foi','além', 'pelo', 'pela']


# In[62]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
from PIL import Image


# In[63]:


#dataset = open("sampleWords.txt", "r").read()

def create_word_cloud(string):
   maskArray = np.array(Image.open("Astro.png")) #uso do numpy
   cloud = WordCloud(background_color = "white", max_font_size=200, max_words = 200, mask = maskArray, stopwords = set(STOPWORDS))
   cloud.generate(string)
   cloud.to_file("wordCloud.png")
   plt.figure()
   plt.imshow(cloud, interpolation='bilinear')
   plt.axis('off')
#dataset = dataset.lower()
create_word_cloud(text_to_cloud)


# In[ ]:




