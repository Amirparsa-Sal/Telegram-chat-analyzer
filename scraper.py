from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import re
from utils import merge_sort
months = {
    'January': 31,
    'February': 29,
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
# finding html files
onlyfiles = [f for f in listdir(".") if (
    isfile(join(".", f)) and f.split(".")[-1] == 'html')]

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
            date_number = int(date[0])
            for month, days in months.items():
                if month == date[1]:
                    break
                date_number += days
            date_number += int(date[2]) * 365 + int(date[2])//4
            if last_date_number != date_number:
                dates.append(last_date_number)
                messages.append(message)
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

print(dates)
print(messages)
plt.figure()
plt.plot(dates, messages, 'b')
plt.xlim(dates[0], dates[-1])
plt.xlabel("Day Number(Origin=First message)")
plt.ylabel("Number of messages")
plt.title(
    f"Total messages: {sum(messages)}")
plt.show()
