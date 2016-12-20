# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import os
import sys
import requests
import simplejson as json
from datetime import datetime

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    is_wx_or = u"天氣"
    if(is_wx_or not in event.message.text):
       line_bot_api.reply_message(event.reply_token,TextMessage(text=event.message.text))
       return
    check = u"市縣"
    if event.message.text.find(check[0])>0:
        index = event.message.text.find(check[0])
    else :
        index = event.message.text.find(check[1])

    location = event.message.text[index-2:index+1]
    url="http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName="+event.message.text[index-2:index+1]+"&elementName=Wx"
    header = {"Authorization":os.getenv('APIKEY', None)}
    origin = requests.get(url,headers=header)
    body = json.loads(origin.content)
    #check current time 
    try:
        time_pre = body['records']['location'][0]['weatherElement'][0]['time']
        for expect in time_pre:
            H_time = datetime.strptime(expect['startTime'],"%Y-%m-%d %H:%M:%S")
            if(datetime > H_time):
                out = expect['parameter']['paramterName']
        reply= location + u"的天氣為" + out
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    except:
        line_bot_api.reply_message(event.reply_token,TextMessage(text="yo~台灣沒這個地方～或是請愛用繁體「臺」ex「臺南市」"))

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
