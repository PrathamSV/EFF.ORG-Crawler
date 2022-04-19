from urllib.request import Request, urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import datetime
from colorama import Fore
import tkinter.messagebox
from tkinter import *
import urllib.request
import webbrowser
import ssl
import os


# region popup()
def popup(title, msg):
    root = Tk()
    msgbox = tkinter.messagebox.askyesno(title, msg)
    root.mainloop()
    return msgbox
# endregion


# region SSL Handler
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
# endregion

url = Request('https://www.eff.org/')

try:
    response = urlopen(url, context=ctx)

except URLError as e:
    # region Error Handler
    # to give reason/error code, if a URL error occurs
    if hasattr(e, 'reason'):
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
        print("The server couldn't fulfill the request.")
        print('Error code: ', e.code)
    # endregion
else:
    # region Objects
    # datetime
    now = datetime.now()
    date = f'{now.day}-{now.month}-{now.year}'

    count = 0  # for link count

    filename = f'EFF.ORG {date}'  # filename

    # empty list to catch dupes
    dupe_detector = []
    # empty list to store links
    content = []

    # endregion

    # region HTML Retriever
    page = urllib.request.urlopen(url, context=ctx)  # open webpage
    # save html
    file_out = open(filename + '.html', 'w')
    file_out.write(str(page.read()))
    file_out.close()
    # endregion

    # create soup object
    with open(filename + '.html') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # making directory
    path = 'EFF.ORG/'
    if not os.path.exists(path):
        os.makedirs(path)
    name = f'EFF.ORG {date}'
    final_path = os.path.join(path, name)

    # region PARSING HTML
    for tag in soup.find_all('a'):  # find all with 'a' tag
        href = tag.get('href')  # get href

        # all '/deeplinks/' are articles
        # ignoring podcasts
        if (('/deeplinks/' in href and 'https://www.eff.org' in href) and (href not in dupe_detector)) and (
                'podcast' not in href):
            count += 1  # keep up count with number of links
            content.append(href)
        # concatenating root site to incomplete links
        elif (('/deeplinks/' in href and 'https://www.eff.org' not in href) and (href not in dupe_detector)) and (
                'podcast' not in href):
            count += 1
            full_src = 'https://www.eff.org' + href
            content.append(full_src)

        dupe_detector.append(href)  # add URL to dupe list

    print(content)
    print(Fore.LIGHTGREEN_EX + 'Parsing Successful!')
    # endregion

    # if exists, open pages
    if os.path.exists(final_path + '.txt'):
        popup('Summary Already Exists',
              f"EFF.ORG Summary For {date} Already Exists\n\nOpen Links?")
        if msgbox:
            print(Fore.GREEN + 'Opening pages in browser...')
            for article_link in content:
                webbrowser.open_new_tab(article_link)
            root.destroy()
        else:
            print(Fore.LIGHTRED_EX + 'Terminating...')
            root.destroy()
    else:
        print(Fore.GREEN + 'Opening pages in browser...')
        with open(final_path + '.txt', 'w') as file:
            for article_url in content:
                file.write(article_url + '\n')
                webbrowser.open_new_tab(article_url)  # open in browser
