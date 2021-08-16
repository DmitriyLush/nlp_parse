from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import re
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from io import BytesIO
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'
config = Config()  # Используем config, чтобы избежать ошибки 403.
config.browser_user_agent = user_agent

# Получаем DataFrame по заданным параметрам, который будет содержать дату, название, источник, описание,
# ссылку на статью и ссылку на изображение
google_news = GoogleNews(lang='en', region='US')
google_news = GoogleNews(start='07/14/2021', end='08/14/2021')
google_news.search('Russia')
result = google_news.result()
df = pd.DataFrame(result)

# т.к. максимальное кол-во ссылок, которое мы можем собрать - 10, будем объодить это при помощи цикла,
# задав в range нужное нам кол-во страниц, цикл будет работать, пока не соберет все статьи в данном промежутке времени.
for i in range(2, 16):
    google_news.getpage(i)
    result = google_news.result()
    df = pd.DataFrame(result)
# т.к. при помощи googlenews мы не можем достать всю статью, используем модуль newspaper,
# достав из ссылок по индексам весь текст каждой статьи и поместим его dataframe.

spisok = []

for ind in df.index:
    dictionary = {}
    article = Article(df['link'][ind], config=config)
    article.download()
    article.html
    article.parse()
    article.nlp()
    dictionary['Date'] = df['date'][ind]
    dictionary['Media'] = df['media'][ind]
    # dictionary['Title'] = article.title
    dictionary['Article'] = article.text
    # dictionary['Summary'] = article.summary
    spisok.append(dictionary)

news_df = pd.DataFrame(spisok)  # здесь наш итоговый df с текстом.


# Регулярные выражения для вычистки текста от лишних знаков
def clean(text):
    text = text.lower()
    text = re.sub(r'http\S+', " ", text)
    text = re.sub(r'@\w+', ' ', text)
    text = re.sub(r'#\w+', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'<.*?>', ' ', text)
    return text


text = news_df['Article']

# Применяем нашу функцию с регулярными выражениями, чтобы почистить текст
text = text.apply(clean)

# тут задаем переменную, которая будет отвечать за лемматизацию.
wn_lemmatizer = WordNetLemmatizer()

# здесь мы применяем эту лемматизацию
lemmatized_text = []
for i in text:
    lemmatized_text.append(' '.join([wn_lemmatizer.lemmatize(word) for word in i.split()]))

# Здесь мы применяем токенайзер, объект у нас - слово
reg_tokenizer = RegexpTokenizer('\w+')

# здесь мы  применяем этот токенайзер
tokenized_text = reg_tokenizer.tokenize_sents(lemmatized_text)

# выгружаем стоп слова для английского языка
sw = stopwords.words()

# вычищаем наш текст от этих стоп слов
clean_tokenized_articles = []
for i, element in enumerate(tokenized_text):
    if i % 10 == 0:
        clean_tokenized_articles.append(' '.join([word for word in element if word not in sw]))


# создаем Трампа.
def plot_wordcloud(clean_tokenized_articles, mask=None, max_words=10000000, max_font_size=100, figure_size=(8.0, 8.0),
                   title=None, title_size=24, image_color=False):
    stopwords = set(STOPWORDS)
    more_stopwords = {'one', 'br', 'Po', 'th', 'sayi', 'fo', 'Unknown', 'title', 'object', 'dtype', 'might', 'bef',
                      'name', 'will', 'two', 'goog', 'logo', 'e', 'Article', 'S', 'cos', 'eye', 't', 'inc', 'seen',
                      'kimmage', 'poli', 'reg', 'c'}
    stopwords = stopwords.union(more_stopwords)
    url = 'https://www.wpclipart.com/dl.php?img=/American_History/presidents/additional_images/Donald_Trump/Trump_silhouette.png'
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    trump = np.array(img)

    wordcloud = WordCloud(background_color='white',
                          mask=trump,
                          stopwords=stopwords,
                          max_words=max_words,
                          max_font_size=max_font_size,
                          random_state=500,
                          contour_width=4,
                          contour_color='black',
                          width=800,
                          height=400,
                          )
    wordcloud.generate(str(text))

    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask)
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.title(title, fontdict={'size': title_size,
                                   'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud)
        plt.title(title, fontdict={'size': title_size, 'color': 'black',
                                   'verticalalignment': 'bottom'})
    plt.axis('off')

    plt.tight_layout()
    plt.show()


plot_wordcloud(clean_tokenized_articles, title="Donald Trump's thoughts")
