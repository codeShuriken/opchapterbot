#A program to extract data and display a short summary of a one piece chapter
#Chapter info is extracted from http://onepiece.wikia.com/wiki
#Created by Gowtham Vuppala (/gowtham9999)

from bs4 import BeautifulSoup
from urllib.parse import urlparse

import praw
import time
import re
import requests
import bs4


path = 'C:/Users/ravindra/desktop/opchapterbot/commented.txt'


header = '**Explanation of this onepiece chapter:**\n'
footer = '\n ---This explanation is extracted from [onepiecewiki](http://onepiece.wikia.com/wiki) | Bot created by (u/gowtham9999)'

def authenticate():
    
    print('Authenticating...\n')
    reddit = praw.Reddit('explainbot',user_agent = 'web:op-chapter-bot:v0.1 (by /u/gowtham9999)')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def fetchdata(url):

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    data = soup.find('p').get_text()
    
    #context =  soup.find_all('p')
    #data = data + '\n' + 'Cover Page:' + '\n' + '\t' + context[1].get_text()
    #data = data + '\n' + 'Short Summary:' + '\n' + '\t' + context[2].get_text()

    table = soup.find_all('div',attrs={"mw-content-ltr mw-content-text"})
    for x in table:
        i = 0
        cover_page_mark = 0
        short_summary_mark = 0
        long_summary_mark = 0

        cover_page = ''
        short_summary = ''

        for el in x.find_all(['h2', 'p']):
            if el.name == 'h2':
                if "Cover Page" in el.get_text() and el.name == 'h2':
                    cover_page_mark = i
                if "Short Summary" in el.get_text() and el.name == 'h2':
                    short_summary_mark = i
                if "Long Summary" in el.get_text() and el.name == 'h2':
                    long_summary_mark = i
            i += 1

        i = 0
        for el in x.find_all(['h2', 'p']):
            if el.name == 'p':
                if cover_page_mark < i < short_summary_mark:
                    cover_page += el.get_text()
                if short_summary_mark < i < long_summary_mark:
                    short_summary += el.get_text()
            i += 1

    data = data + '\n' + 'Cover Page:\n\t' + cover_page + '\n' + 'Short Summary:\n\t' + short_summary
    
    ch_num = int(re.search(r'\d+', url).group())
    ch_link =  'https://ww2.mangafever.me/Read1/One_Piece_' + str(ch_num)
    data = data + '\n' + '[Link To Chapter]({})'.format(ch_link)
    
    return data
def run_explainbot(reddit):
    
    print("Getting 100 comments...\n")
    
    for comment in reddit.subreddit('test').comments(limit = 100):
        match = re.findall("[a-z]*[A-Z]*[0-9]*Chapter_[0-9]+", comment.body)
        if match:
            print('Link found in comment with comment ID: ' + comment.id)
            opchp_url = match[0]
            print('Link: ' + opchp_url)    
            myurl = 'http://onepiece.wikia.com/wiki/' + str(opchp_url)
            file_obj_r = open(path,'r')
                        
            try:
                explanation = fetchdata(myurl)
            except:
                print('Exception!!! Possibly incorrect chapter number...\n')
                
            else:
                if comment.id not in file_obj_r.read().splitlines():
                    print('Link is unique...posting explanation\n')
                    comment.reply(header + explanation + footer)
                    
                    file_obj_r.close()

                    file_obj_w = open(path,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                else:
                    print('Already visited link...no reply needed\n')
            
            time.sleep(10)

    print('Waiting 60 seconds...\n')
    time.sleep(60)

def main():
    reddit = authenticate()
    while True:
        run_explainbot(reddit)


if __name__ == '__main__':
    main()
