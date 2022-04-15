from hashlib import new
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import telebot

#make bot
bot = telebot.TeleBot("put your bot access token here")

#make fake user agent to avoiding block form site side
ua = UserAgent()
headers = {"user-agent": ua.firefox}

# request to site
main_site = "link on site"
r = requests.get(main_site, headers=headers)
news_list = {}

def make_list_of_news():
    if(r.status_code == 200):
        list_for_news = []
        dict_for_news = {}
        soup = BeautifulSoup(r.text, 'html.parser')
        chapter_table = soup.find("div", class_="new-news-grid__elem__list")
        for item in chapter_table:
            list_for_news.extend(chapter_table.find_all("a", class_="new-news-piece__link"))
        for item in list_for_news:
            text_for_delete = item.find("span").text
            dict_for_news[item["href"]] = item.text.strip(text_for_delete).rstrip()
        return dict_for_news

@bot.message_handler(commands=["news"])
def news(message):
    news_list = make_list_of_news()
    for k, v in news_list.items():
        bot.send_message(message.chat.id, v + " " + "-" + " " + main_site + k + "\n")

bot.polling(none_stop=True, interval=0)
