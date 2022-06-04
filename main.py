import requests as r
import json
import tryagain
import time
import config as cfg

tg_url = 'https://api.telegram.org/bot' + cfg.tg_token + '/sendmessage'
tunnels_old = ''


def checker():
    global tunnels_old
    iteration = 0
    tunnels = (r.get('https://api.ngrok.com/tunnels',
                     headers={'Authorization': 'Bearer ' + cfg.ngrok_token,
                              'Ngrok-Version': '2', 'Cache-Control': 'no-cache'})).text
    if tunnels != tunnels_old:
        if 'public_url' in tunnels:
            tunnels_old = tunnels
            tunnels_json = json.loads(tunnels)['tunnels']
            tunnels_list = [item.get('public_url') for item in tunnels_json]
            while iteration < len(tunnels_list):
                resp = r.get('https://mcstatus.snowdev.com.br/api/query/v3/' + tunnels_list[iteration][6::], timeout=15)
                if 'online' in resp.text:
                    url_new = tunnels_list[iteration][6::]
                    r.post(tg_url, data={'chat_id': cfg.chat_id, 'text': url_new}, timeout=10)
                    break
                else:
                    iteration += 1
        else:
            r.post(tg_url, data={'chat_id': cfg.chat_id, 'text': 'It seems like my server is down. Please wait.'},
                   timeout=10)
    time.sleep(300)
    checker()


try:
    checker()
except Exception as e:
    print(e)
    time.sleep(300)
    tryagain.call(checker)
