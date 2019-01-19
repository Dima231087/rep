import requests
from time import sleep
from constants import token
import datetime

#url = "https://api.telegram.org/bot{}/".format(token)

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            print(len(get_result))
            #last_update = get_result[len(get_result)]
            last_update = 0
        return last_update

greet_bot = BotHandler(token)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')

now = datetime.datetime.now()
today = now.day

def body(last_update, now, hour) :
    global today  
    last_update_id = last_update['update_id']
    last_chat_text = last_update['message']['text']
    last_chat_id = last_update['message']['chat']['id']
    last_chat_name = last_update['message']['chat']['first_name']

    if last_chat_text[0] == '/' :
        last_chat_command = last_update['message']['entities'][0]['type']
    else :
        last_chat_command = ''
        
    if last_chat_text.lower() in greetings and today == now and 6 <= hour < 12:
        greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
        #today += 1

    elif last_chat_text.lower() in greetings and today == now and 12 <= hour < 17:
        greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
        #today += 1

    elif last_chat_text.lower() in greetings and today == now and 17 <= hour < 23:
        greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
        #today += 1

    elif last_chat_command.lower() in ['bot_command'] :
        greet_bot.send_message(last_chat_id, 'Это команда, {}'.format(last_chat_name))

    return last_update_id+1

def main():  
    new_offset = None
    #today = now.day
    hour = now.hour
    global today
    today = now.day
      
    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if not(last_update) == 0 :
            new_offset=body(last_update, now.day, hour)
            print(last_update)

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()


    
