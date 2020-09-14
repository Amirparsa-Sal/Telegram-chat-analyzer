from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from wordcloud_fa import WordCloudFa
import re
import codecs
from utils import merge_sort
import numpy as np
from PIL import Image
import functools
# finding html files
from tkinter import filedialog
from tkinter import *

window = Tk()
window.withdraw()
folder_selected = filedialog.askdirectory()
onlyfiles = [f for f in listdir(folder_selected) if (
    isfile(join(".", f)) and f.split(".")[-1] == 'html')]

if len(onlyfiles) == 0:
    print("There is no html file here!")
    exit(-1)
else:
    print("Processing...")

def find_date_number(date):
    day = int(date[0])
    year = int(date[2]) 
    months = {
        'January': 31,
        'February': 28 + int(year%4==0),
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30,
        'October': 31,
        'November': 30
    }
    date_number = 0
    for month, days in months.items():
        if month == date[1]:
            break
        date_number += days
    date_number += day + year * 365 + year//4
    return date_number

def show_chat_diagram():
    months = ['January','February','March','April','May','June','July','August','September','October','November']
    # finding messages
    last_date_number = 0
    message = 0
    dates = []
    messages = []
    for file in onlyfiles:
        soup = BeautifulSoup(open(file), 'html.parser')
        divs = soup.find_all('div')
        for div in divs:
            if div['class'] == ['message', 'service']:
                date = div.find('div').text
                date = date.replace('\n', '')
                date = date.split(" ")
                #finding day_number
                if date[1] in months:
                    date_number = find_date_number(date)
                    if last_date_number != date_number:
                        if last_date_number not in dates:
                            dates.append(last_date_number)
                            messages.append(message)
                        else:
                            index = dates.index(last_date_number)
                            messages[index] += message
                        message = 0
                        last_date_number = date_number
            if div['class'] == ['message', 'default', 'clearfix', 'joined'] or div['class'] == ['message', 'default', 'clearfix']:
                message += 1
    dates.append(last_date_number)
    messages.append(message)
    dates = dates[1:]
    messages = messages[1:]
    for date in range (min(dates)+1,max(dates)):
        if date not in dates:
            dates.append(date)
            messages.append(0)
    merge_sort(dates,0,len(dates)-1,messages)
    dates = list(map(lambda date: date-dates[0],dates))
    for i in range(1,len(messages)):
        messages[i] += messages[i-1]
    plt.figure()
    plt.plot(dates, messages, 'b')
    plt.xlim(dates[0], dates[-1])
    plt.xlabel("Day Number(Origin=First message)")
    plt.ylabel("Total messages until that day")
    plt.title(
        f"Total messages: {messages[-1]}")
    plt.savefig("Diagram.png")
    plt.show()
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

def show_chat_word_cloud():
    with codecs.open("chats.txt",'r',encoding='utf8') as file:
        mask_array = np.array(Image.open("telegram.png"))
        wordcloud = WordCloudFa(persian_normalize=True,mask=mask_array)
        wordcloud.add_stop_words(['ama','ba','ta','ra','ro','az','dar','va','ke','be','mn','man','vali','ye','من','یه'])
        text = delete_extra_characters(file.read())
        wc = wordcloud.generate(text)
        image = wc.to_image()
        image.show()
        image.save('wordcloud.png')

def save_chats():
    with codecs.open("chats.txt",'a') as exp_file:
        for file in onlyfiles:
            soup = BeautifulSoup(open(file), 'html.parser')
            divs = soup.find_all('div')
            for div in divs:
                if div['class'] == ['text']:
                    exp_file.write(div.text + "\n")
# save_chats()
# show_chat_word_cloud()
show_chat_diagram()