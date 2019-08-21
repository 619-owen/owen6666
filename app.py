from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

# 設定你的Channel Access Token
line_bot_api = LineBotApi('jQsG4of0z7uZE0zHMnV8zc4gU7BYOQCXRJYakROKvJa8B9rCy3d7bqoE/4fFtq0vp2hwMlSmZEFTv65rC5DPaTG1h5s0m01xXFLMGlggumvatmDKrrleGvj7T/k6q8U7QNhVN3OB86bWFEl5N7GpkgdB04t89/1O/w1cDnyilFU=')
# 設定你的Channel Secret
handler = WebhookHandler('868cafd3b46eb2a648690807863670bc')

# 監聽所有來自 /callback 的 Post Request
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

#處理訊息
#當訊息種類為TextMessage時，從event中取出訊息內容，藉由TextSendMessage()包裝成符合格式的物件，並貼上message的標籤方便之後取用。
#接著透過LineBotApi物件中reply_message()方法，回傳相同的訊息內容
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	usersend = event.message.text
	if usersend == '你好':
		message = TextSendMessage(text='Hello，歡迎您加入此群組，我是此群組的管理人Owen，這個群組是要協助大家迅速連結到很多自學網，例如: 下面的三大國旗，會分別連結到英文、德文、西班牙文的文法學習網站，自學網不僅有三大語言學習網，還可以輸入以下數字號碼，連結國際型的英檢線上試題及相關自學資源:1. 多益(TOEIC)線上試題-考尚樂2. 托福(TOEFL)試題練習-考滿分3. 雅思(IELTS) 準備資訊、模板及練習- IELTS-Exam. net 4.英文知識補充- ThoughtCo. 　    　這些學習資訊皆是Owen親自看過挑選出來，也不保證任何效果，只是協助大家更快速取得資源，提升學習效率，Owen也不會在群組回答大家學習上的問題，請見諒!')
	elif usersend=='？':
		message=TextSendMessage(text='Hi,歡迎您的加入,可按選單選取你想學的語言')
	elif usersend=='1':
		message=TextSendMessage(text='多益(TOEIC)線上試題-考尚樂在這裡~   https://quizfun.co/courses/2229')
	elif usersend=='2':
		message=TextSendMessage(text='托福(TOEFL)試題練習-考滿分在這裡~   https://toefl.kmf.com/')
	elif usersend=='3':
		message=TextSendMessage(text='雅思(IELTS) 準備資訊、模板及練習- IELTS - Exam .net在這裡~    https://www.ielts-exam.net/')
	elif usersend=='4':
		message=TextSendMessage(text='英文知識補充- ThoughtCo.在這裡~   https://www.thoughtco.com/')
	else:
		message=TextSendMessage(text='我看不懂您打什麼，您可以直接複製並輸入您想連結的學習網站～')
	line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)