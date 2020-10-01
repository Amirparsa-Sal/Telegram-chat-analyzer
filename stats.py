from utils import merge_sort
import matplotlib.pyplot as plt
import os 

def plot_chat_diagram(dates,messages,dir="."):
    for date in range (min(dates)+1,max(dates)):
        if date not in dates:
            dates.append(date)
            messages.append(0)
    merge_sort(dates,0,len(dates)-1,messages)
    dates = list(map(lambda date: date-dates[0],dates))
    print("Almost done...")
    for i in range(1,len(messages)):
        messages[i] += messages[i-1]
    plt.figure()
    plt.plot(dates, messages, 'b')
    plt.xlim(dates[0], dates[-1])
    plt.xlabel("Day Number(Origin=First message)")
    plt.ylabel("Total messages until that day")
    plt.title(
        f"Total messages: {messages[-1]}")
    plt.savefig(os.path.join(dir,'Diagram.png'))
    plt.show()