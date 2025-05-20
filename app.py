import json
import sqlite3
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import(
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    FlexMessage,
    FlexContainer,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import(
    MessageEvent,
    TextMessageContent
)
from model import init_db, insert_order
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
init_db()

configuration = Configuration(access_token= os.environ.get("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        handler.handle(body, signature)
    except Exception as e:
        app.logger.error(f"Error: {e}")
        abort(500)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    user_id = event.source.user_id
    my_id = 'Uaf352c8032451e4509229410992f13ad'
    her_id = "Ua19c4c7500e0e3edabcddc7e8dce005c"
    text = event.message.text
    reply_text =""
    # print(text)
    with ApiClient(configuration=configuration) as api_client:
         line_bot_api = MessagingApi(api_client)
    if '*' in text:
        try:
            # 預設三個產品數量為 0
            cheese = financier_original = financier_choco = financier_tea = pudding = 0
            payment = pickup_date = pickup_time = pickup_location = ''
            # text = text.replace('\n', ' ')
            # items = text.split()
            items = text.strip().splitlines()
            for item in items:
                item = item.strip()
                # print(item)
                if '*' in item:
                    name, qty = item.split('*')
                    qty = int(qty)
                    if '巴斯克' in name:
                        cheese += qty
                    elif '原味費南雪' in name:
                        financier_original += qty
                    elif '法芙娜可可費南雪' in name:
                        financier_choco += qty
                    elif '麵茶費南雪' in name:
                        financier_tea += qty
                    elif '舒肥布丁' in name:
                        pudding += qty
                
                elif item.startswith('付款方式'):
                    payment = item.split(':', 1)[-1].strip()
                elif item.startswith('日期'):
                    pickup_date = item.split(':', 1)[-1].strip()
                elif item.startswith('時間'):
                    pickup_time = item.split(':', 1)[-1].strip()
                elif item.startswith('面交地點'):
                    pickup_location = item.split(':', 1)[-1].strip()
            # 取得使用者名稱
            profile = line_bot_api.get_profile(user_id)
            user_name = profile.display_name

            insert_order(
                user_id, user_name,
                cheese, financier_original, financier_choco, financier_tea, pudding,
                payment, pickup_date, pickup_time, pickup_location
            )
            total = cheese*60 + financier_original*35 + financier_choco*40 + financier_tea*40 + pudding*65
            reply_text_cash = f"""✅ 訂單完成：
原味費南雪*{financier_original}
法芙娜可可費南雪*{financier_choco}
麵茶費南雪*{financier_tea}
舒肥布丁*{pudding}
付款方式: {payment}
日期: {pickup_date}
時間: {pickup_time}
地點: {pickup_location}
總金額: {total} 元"""
            reply_text_credict = f"""✅ 訂單完成：
原味費南雪*{financier_original}
法芙娜可可費南雪*{financier_choco}
麵茶費南雪*{financier_tea}
舒肥布丁*{pudding}
付款方式: {payment}
日期: {pickup_date}
時間: {pickup_time}
地點: {pickup_location}
總金額: {total} 元
請提供您的轉帳末五碼(現金可忽略)"""
            if payment == "現金":
                reply_text = reply_text_cash
            else: 
                reply_text = reply_text_credict
        except Exception as e:
            reply_text = f"""輸入格式錯誤，請參考以下範例
原味費南雪*0
法芙娜可可費南雪*2
麵茶費南雪*4
舒肥布丁*6
付款方式(超過300請先轉帳):現金
日期:5/13 
時間:1032
地點:台南7-11忠孝門市"""

    elif text == "費南雪":
        financier_json = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                    },
                    {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Time",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "10:00 - 23:00",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "CALL",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
            }
        financier_json = json.dumps(financier_json)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[FlexMessage(altText="詳細說明", contents=FlexContainer.from_json(financier_json))]
            )
        )
    elif text == "舒肥布丁":
        pudding_json = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                    },
                    {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Time",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "10:00 - 23:00",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "CALL",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
            }
        pudding_json = json.dumps(pudding_json)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[FlexMessage(altText="詳細說明", contents=FlexContainer.from_json(pudding_json))]
            )
        )
    elif text == "巴斯克":
        cheese_json = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://developers-resource.landpress.line.me/fx/img/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "https://line.me/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png"
                    },
                    {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://developers-resource.landpress.line.me/fx/img/review_gray_star_28.png"
                    },
                    {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "Flex Tower, 7-7-4 Midori-ku, Tokyo",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Time",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": "10:00 - 23:00",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "CALL",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": "https://line.me/"
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
            }
        cheese_json = json.dumps(cheese_json)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[FlexMessage(altText="詳細說明", contents=FlexContainer.from_json(cheese_json))]
            )
        )
    elif text == "菜單":
        menu_url = "https://i.ibb.co/b9pW2jL/line-oa-chat-250521-002139.jpg"
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[ImageMessage(originalContentUrl=menu_url, previewImageUrl=menu_url)]
            )
        )
    elif text == "訂購方式":
       orderway = f"原味費南雪*數量\n法芙娜可可費南雪*數量\n麵茶費南雪*數量\n舒肥布丁*數量\n \n付款方式(超過300請先轉帳):\n日期:\n時間:\n面交地點:台南7-11忠孝門市"
       payment_info = f"""轉帳資訊
銀行:012
帳號:0081680011444411
亦可輸入手機號碼:0911881603
或是掃描下面的QRcode"""
       payment_account_url = "https://i.ibb.co/xKpm6Yg8/1747756769737.png"
       line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text=orderway), TextMessage(text=payment_info), ImageMessage(originalContentUrl=payment_account_url, previewImageUrl=payment_account_url)]
            )
        )
    elif text == "當月製作時間表":
            month_make_time_url = "https://i.ibb.co/JjsqwdbH/1747756769595-1.jpg"
            line_bot_api.reply_message(
                 ReplyMessageRequest(
                     replyToken=event.reply_token,
                     messages=[ImageMessage(originalContentUrl=month_make_time_url, previewImageUrl=month_make_time_url)]
                )
            )
    elif text == "查看訂單" and (user_id == my_id or user_id == her_id):
        conn = sqlite3.connect('orders_0520.db')
        c = conn.cursor()
        c.execute("SELECT * FROM orders ORDER BY ROWID DESC LIMIT 5")  # 最新5筆
        rows = c.fetchall()
        conn.close()

        msg = "📦 最新訂單：\n"
        for row in rows:
            msg += f"{row[2]}：巴斯克{row[3]} 原味{row[4]} 可可{row[5]} 麵茶{row[6]} 布丁{row[7]} 日期{row[9]} 時間{row[10]} \n"

        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )
    else:
        reply_text = f"請稍後，闆娘會為您服務"
    if reply_text:  # 有需要回覆文字時才執行
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )




if __name__ == "__main__":
    app.run()