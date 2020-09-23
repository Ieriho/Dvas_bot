#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from time import sleep
import datetime

#url = "https://api.telegram.org/bot1370260612:AAEUjMN4eVV5civSbj4t-AUugASg9TRuEA8/"

class BotHandler():
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"


    def get_updates(self, offset=None, timeout=30):
        methods = 'getUpdates'
        params = {'timeout':timeout, 'offset':offset}
        response = requests.get(self.api_url+'getUpdates', data=params)
        result_json = response.json()['result']
        return result_json
    
    def send_message(self, chat, text):
        method = 'sendMessage'
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.api_url, data=params)
        return response

    def get_last_update(self):
        get_result = self.get_updates()
        
        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = len(get_result)
        
        return last_update

my_bot = BotHandler('1370260612:AAEUjMN4eVV5civSbj4t-AUugASg9TRuEA8')
now = datetime.datetime.now()
greetengs = ('hello', 'hi', 'привет')

def main():  
    new_offset = None
    today = now.day
    hour = now.hour
    
    while True:
        my_bot.get_updates(new_offset)
        last_update = my_bot.get_last_update()
        
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, f'Доброе утро, {last_chat_name}')
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, f'Добрый день, {last_chat_name}')
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, f'Добрый вечер, {last_chat_name}')
            today += 1

        new_offset = last_update_id += 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
    


# In[ ]:




