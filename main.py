import telebot
import html
import requests
import urllib.request
from html.parser import HTMLParser
from lxml import html
from requests_html import HTMLSession
import os
import pandas as pd
from io import StringIO
from urllib.parse import urlparse
from html import escape

api_name = ""
api_key = ""
bot_token = ""

bot = telebot.TeleBot(bot_token)
@bot.message_handler()
def handle_unrestrict(message):
    link = message.text.split()[0]
    if(link.startswith('https://controlc.com')):
        links = get_links(url=link)

        for l in links:
            pLink = get_premium_link(l)

            if(isinstance(pLink, int) == False):
                filename = pLink['filename']
                filename = filename.replace("_", "\_").replace("*", "\*").replace("[", "\[").replace("]", "\]")                
                host = pLink['host']
                unrestricted_link = pLink['link']
                bot.send_message(message.chat.id, '*Archivo:* '+filename+'\n*Host:* '+host+'\n[Descargar]('+unrestricted_link+')', parse_mode='Markdown', disable_web_page_preview=True)
            else:
                bot.send_message(message.chat.id, 'Enlace inválido ♿️', parse_mode='Markdown')

            
    elif is_url(link):
        pLink = get_premium_link(link)
        if(isinstance(pLink, int) == False):
            filename = pLink['filename']
            filename = filename.replace("_", "\_").replace("*", "\*").replace("[", "\[").replace("]", "\]")            
            host = pLink['host']
            unrestricted_link = pLink['link']
            bot.send_message(message.chat.id, '*Archivo:* '+filename+'\n*Host:* '+host+'\n[Descargar]('+unrestricted_link+')', parse_mode='Markdown', disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id, 'Enlace inválido ♿️', parse_mode='Markdown')



    else:
        bot.send_message(message.chat.id, 'Enlace inválido ♿️', parse_mode='Markdown')

def get_premium_link(url):
    response = requests.post('https://api.alldebrid.com/v4/link/unlock?agent='+api_name+'&apikey='+api_key+'&link='+url)
    try:
        if response.json()['error'] in ["hoster_unsupported","unavailable_file"]:
            return response.json()['error_code']
        else:
            pass
    except:
        pass
    if response.status_code in [404,503,16,24]:
        print('ERROR: ' + response.status_code)
        return response.status_code
    else:
        filename = response.json()['data']['filename']
        host = response.json()['data']['host']
        unrestricted_link = response.json()['data']['link']

        return {
            'filename': filename,
            'host': host,
            'link': unrestricted_link
        }

def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False


def get_links(url):
    links = os.popen('python3 LinkParser.py '+url).read()

    links = pd.read_csv(StringIO(links), header=None).values.tolist()
    print(links)
    filtered_links = []
    for link in links:
        filtered_links.append(link[0])
    
    
    return filtered_links
        
bot.polling()
