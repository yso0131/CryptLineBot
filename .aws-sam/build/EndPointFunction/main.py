import os
import Output


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage
)


# ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '\
#      'AppleWebKit/537.36 (KHTML, like Gecko) '\
#      'Chrome/67.0.3396.99 Safari/537.36 '


# line botのテンプレ
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))


# API GATEWAYのテンプレ
def lambda_handler(event, context):
    headers = event["headers"]
    body = event["body"]

    # get X-Line-Signature header value
    signature = headers['x-line-signature']

    # handle webhook body
    handler.handle(body, signature)

    return {"statusCode": 200, "body": "OK"}


@handler.add(MessageEvent, message=TextMessage)
def handle_text_nessage(event):
    """ TextMessage handler """
    # 入力されたメッセージのみを取得するためにevent.message.textをtextへ入れる
    text = event.message.text

    # input_textへ通貨名と値段を入れる
    input_text = Output.output.output_value(text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=input_text))
