# coding: utf-8
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage 
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

#line token
channel_access_token = 'tJuWQTeKfBKvosEwiSp1FsMIZIAMDy5xcey/AyApceWL+a6pcUIVQHv/Jh2lrGOFyVU0QVF1OuVIsxa/N4NHEOdw27MDuqzWzHXrXMOl4hLl40FzgcZwEEv9qZbME3cJMfA0oKuRqrB16zz8o2V7SAdB04t89/1O/w1cDnyilFU='
channel_secret = '6cab63fefd52211f281bac1827f86e91'
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

configuration = Configuration(channel_access_token)
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
