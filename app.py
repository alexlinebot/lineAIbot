from flask import Flask
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage, ImageSendMessage, StickerSendMessage,LocationSendMessage, QuickReply, QuickReplyButton, MessageAction

import chatwithpdf

line_bot_api = LineBotApi('tJuWQTeKfBKvosEwiSp1FsMIZIAMDy5xcey/AyApceWL+a6pcUIVQHv/Jh2lrGOFyVU0QVF1OuVIsxa/N4NHEOdw27MDuqzWzHXrXMOl4hLl40FzgcZwEEv9qZbME3cJMfA0oKuRqrB16zz8o2V7SAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6cab63fefd52211f281bac1827f86e91')

@app.route("/callback", methods=['POST'])
def callback():
   signature = request.headers['X-Line-Signature']
   body = request.get_data(as_text=True)
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   mtext = event.message.text
   print(mtext)
   if  mtext.startswith('@小仙僮'):
       try:
           reply = chatwithpdf.chatpdf(mtext)
           message = TextSendMessage(
               text = reply
           )
           line_bot_api.reply_message(event.reply_token, message)
       except:
           line_bot_api.reply_message(event.reply_token,
               TextSendMessage(text= 'Sorry 故障囉！'))

if __name__ == '__main__':
   app.run()