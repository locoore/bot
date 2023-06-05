from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
# 處理 Line Webhook 請求
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, ImageSendMessage
import openai
import logging



line_bot_api = LineBotApi("ZXhZKlg468GHg9IjnjSEi8BHAPnrsySNFpEbFgBScxAyA0bRS9wJHEfD6lu79twWSOgJbDSYBErsxsP863sxtaJVSVuD4O6+0tzkG6NCPxQdbcO/eIMTPImKzHzLIPwKBdulvhJoSiMp3lfLpJdgaAdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("U1478ec1917735d6f49d3df17dd87b3f4")
openai.api_key = "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"



# Line Bot 的消息處理程序
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    print("Entering handler() function")  # 偵錯
    # 取得用户輸入的 prompt
    user_prompt = event.message.text

    # 使用 OpenAI DALL·E API 生成圖像
    response = openai.Image.create(
        prompt=user_prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']

    # 創建要發送的訊息
    image_message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)

    # 傳送圖像给用户
    line_bot_api.reply_message(event.reply_token, messages=image_message)


# 配置日志紀錄
logging.basicConfig(filename='/home/Ciga/mysite/app.log', level=logging.INFO)


# Flask 應用程序
app = Flask(__name__)





@app.route("/callback", methods=['POST'])
def callback():
    print("Entering callback() function")  # 偵錯句
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    except LineBotApiError as e:
        # 處理、捕捉 Line Bot API 錯誤
        logging.error(f"Line Bot API Error: {str(e)}")
        abort(500)
    except Exception as e:
        # 處理其他未預測到的異常
        logging.error(f"Unexpected error: {str(e)}")
        abort(500)

    return 'OK'



if __name__ == '__main__':
    app.run(debug=True, port=8500)
