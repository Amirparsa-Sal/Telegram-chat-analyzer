from bs4 import BeautifulSoup
import os
import json
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from wordcloud_fa import WordCloudFa
import re
import codecs
from utils import merge_sort, find_date_number
from word_cloud import delete_extra_characters, show_chat_word_cloud
from stats import plot_chat_diagram
import numpy as np
from PIL import Image
import functools
# finding html files
from tkinter import filedialog,Tk

window = Tk()
window.withdraw()
DIRECTORY = filedialog.askdirectory()
print(listdir(DIRECTORY))
onlyfiles = [f for f in listdir(DIRECTORY) if (
    isfile(join(DIRECTORY, f)) and (f.split(".")[-1] == 'html' or f.split(".")[-1] == 'json'))]

window.destroy()

if len(onlyfiles) == 0:
    print("There is no html file here!")
    exit(-1)

def get_chat_data_html(dir,onlyfiles):
    months = ['January','February','March','April','May','June','July','August','September','October','November']
    # finding messages
    last_date_number = 0
    message = 0
    dates = []
    messages = []
    print("Scanning messages...")
    for file in onlyfiles:
        soup = BeautifulSoup(open(os.path.join(dir,file)), 'html.parser')
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
    print("Sorting data...")
    dates.append(last_date_number)
    messages.append(message)
    dates = dates[1:]
    messages = messages[1:]
    return (dates,messages)

def get_chat_data_json(dir,onlyfiles):
    months = ['January','February','March','April','May','June','July','August','September','October','November']
    # finding messages
    last_date_number = 0
    message_num = 0
    dates = []
    message_nums = []
    print("Scanning messages...")
    for file in onlyfiles:
        with codecs.open(os.path.join(DIRECTORY,file),) as exp_file:
            data = json.load(exp_file)
            messages = data["messages"]
            for message in messages:
                if message["type"] == "message":
                    date = message["date"][0:10]
                    date = date.split("-")
                    date[1] = months[int(date[1])-1]
                    year = date[0]
                    date[0] = date[2]
                    date[2] = year
                    #finding day_number
                    date_number = find_date_number(date)
                    if last_date_number != date_number:
                        if last_date_number not in dates:
                            dates.append(last_date_number)
                            message_nums.append(message_num)
                        else:
                            index = dates.index(last_date_number)
                            message_nums[index] += message_num
                        message_num = 0
                        last_date_number = date_number
                message_num+=1
    print("Sorting data...")
    dates.append(last_date_number)
    message_nums.append(message_num)
    dates = dates[1:]
    message_nums = message_nums[1:]
    return (dates,message_nums)

def save_chats_html(dir):
    with codecs.open(os.path.join(dir,'chats.txt'),'w') as exp_file:
        exp_file.write("")
    with codecs.open(os.path.join(dir,'chats.txt'),'a') as exp_file:
        for file in onlyfiles:
            soup = BeautifulSoup(open(os.path.join(dir,file)), 'html.parser')
            divs = soup.find_all('div')
            for div in divs:
                if div['class'] == ['text']:
                    exp_file.write(div.text + "\n")


print("Select a number\n1)html\n2)JSON")
mode = int(input())
print("Select a number\n1)Word Cloud\n2)Chat Diagram")
n = int(input())
if n==1:
    print("Start making word cloud...")
    print("Start storing chat data...")
    save_chats_html(DIRECTORY)
    print("Chat data stored...")
    show_chat_word_cloud(DIRECTORY)
    print("The word cloud is ready!")
elif n==2:
    print("Start making diagram...")
    dates = None
    messages = None
    if mode == 1:
        dates,messages = get_chat_data_html(DIRECTORY,onlyfiles)
    else:
        dates,messages = get_chat_data_json(DIRECTORY,onlyfiles)
    plot_chat_diagram(dates,messages,DIRECTORY)
    print("The diagram is ready!")
exit(0)


