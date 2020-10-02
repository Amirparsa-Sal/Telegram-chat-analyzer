from wordcloud_fa import WordCloudFa
import os
import codecs
import numpy as np
from PIL import Image
import re

def show_chat_word_cloud(directory):
    with codecs.open(os.path.join(directory,'chats.txt'),'r',encoding='utf8') as file:
        print("Start putting words in picture")
        mask_array = np.array(Image.open("telegram.png"))
        wordcloud = WordCloudFa(persian_normalize=True,mask=mask_array,collocations=False)
        stop_words = []
        with codecs.open("stop_words.txt",'r',encoding='utf8') as words:
          for word in words:
            stop_words.append(word[:-2])
        wordcloud.add_stop_words(stop_words)
        text = delete_extra_characters(file.read())
        wc = wordcloud.generate(text)
        image = wc.to_image()
        image.show()
        image.save(os.path.join(directory,'wordcloud.png'))

def delete_extra_characters(text):
    weridPatterns = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)
    return weridPatterns.sub(r'', text)