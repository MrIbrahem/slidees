#!/usr/bin/env python
"""Demo Telegram bot on repl.it.

This program is dedicated to the public domain under the MIT License.

http://www.slideshare.net/MrIbrahem/3-40437776

https://www.slideshare.net/MrIbrahem/3-40437776
https://slideshare.net/MrIbrahem/3-40437776

slideshare.net/MrIbrahem/3-40437776

"""
from flask import Flask, request, render_template, Response
from telegram import Bot, ChatAction, Update


import logging
import os
import json
import re
import sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True

try:
    TOKEN = os.environ["TOKEN"]
except Exception as e:
    print("ERROR: Cannot get token from environment:%s" % e)
    # print(os.environ)
    sys.exit(1)

urle = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://3e6d204d-2e36-4978-9b38-08fde9795220-00-1kx1b5ei4dfoq.janeway.replit.dev/"
urle = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://slidees.mribrahem.repl.co/"
# urle = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://slide-tyob.onrender.com"

username = False
update = None
app = Flask(__name__)
# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
# Define global vars and constants
bot = Bot(token=TOKEN)

bot_msg_id = {1: False, "text": ""}

import pdf_uu

def tel_send_message(text, edit=False):
    """Send a message to a chat."""

    # url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    # payload = { 'chat_id': chat_id, 'text': text }
    # r = requests.post(url, json=payload)
    # return r
    if update.message.chat_id and text != "":
        if not edit:
            try:
                mss = bot.send_message(chat_id=update.message.chat_id, text=text)
            except Exception as e:
                print("Error line 77 : %s" % e)
        else:
            if not bot_msg_id[1]:
                # ---
                try:
                    mss = bot.send_message(chat_id=update.message.chat_id, text=text)
                except Exception as e:
                    print("Error line 85 : %s" % e)
                # ---
                mss1 = """{'message_id':460,'date':1660592634,'chat':{'id':1348919584,'type':'private','username':'Ibrahim_Qasim','first_name':'i','last_name':'q'},'text':'37Slidesdownloaded','entities':[],'caption_entities':[],'photo':[],'new_chat_members':[],'new_chat_photo':[],'delete_chat_photo':False,'group_chat_created':False,'supergroup_chat_created':False,'channel_chat_created':False,'from':{'id':5473798898,'first_name':'Slidesharebot','is_bot':True,'username':'slides_share_bot'}}"""
                # ---
                bot_msg_id[1] = mss.message_id
                bot_msg_id["text"] = mss.text
                logger.info(f"Message sent: {mss.message_id}")
            else:
                text2 = bot_msg_id["text"] + "\n" + text
                # ---
                if text.find("Error downloading slide number") == -1:
                    bot_msg_id["text"] = text2
                # ---
                done = False
                try:
                    bot.edit_message_text(chat_id=update.message.chat_id, message_id=bot_msg_id[1], text=text2)
                    done = True
                except Exception as e:
                    print("Error line 102 : %s" % e)
                    done = False
                # ---
                if not done:
                    try:
                        bot.send_message(chat_id=update.effective_chat.id, text=text2)
                    except Exception as e:
                        print("Error line 110 : %s" % e)


def logg(s):
    logger.info(s)


def start_with_url(url):
    # ---
    global username
    # ---
    _co, result = pdf_uu.start_with_url(url, username, tel_send_message, logg)
    # ---
    if _co == "err":
        tel_send_message(result)
        return Response("ok", status=200)
    # ---
    filepath = ""
    title = ""
    # ---
    if _co == "file":
        title = result["title"]
        filepath = result["filepath"]
    # ---
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    except Exception as e:
        print("Error line : %s" % str(e))
    # ---
    # Send pdf to telegram
    try:
        bot.send_document(chat_id=update.message.chat_id, document=open(filepath, "rb"), filename=title)
        # ---
        # delete the pdf file
        os.remove(filepath)
    except Exception as e:
        print("bot_send_message Error : %s" % str(e))
    # ---
    return Response("ok", status=200)


def get_message_age(message):
    """Compute the time since the last message first arrived.
    Args:
        message: a message from the Telegram update.
    Returns:
        message age in milliseconds.
    """
    event_time = message.date
    if message.edit_date:
        event_time = message.edit_date
    event_age = (datetime.now(timezone.utc) - event_time).total_seconds()
    event_age_ms = event_age * 1000
    logger.info(str(event_age_ms))
    return event_age_ms


def bot_send_message(chat_id="", text=""):
    try:
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print("bot_send_message Error : %s" % str(e))


def timeout(message, max=60000):
    try:
        event_age_ms = get_message_age(message)
    except Exception as e:
        logger.info(f"timeout except: {e}")
        return True
    # ---
    # Ignore events that are too old
    if event_age_ms < max:
        return False
    else:
        if update.effective_chat:
            bot_send_message(chat_id=update.effective_chat.id, text="I thought you left. Please use /start command to restart the bot.")
            # ---
        logger.info("\n Dropped {} (age {}ms)".format(update.update_id, event_age_ms))
        return True


@app.route("/users", methods=["GET"])
def users():
    return open("users.json", "r").read()


@app.route("/dates", methods=["GET"])
def dates():
    return open("dates.json", "r").read()


@app.route("/", methods=["POST", "GET"])
def index():
    print(f"method: {request.method} ")
    if request.method != "POST":
        return render_template("x3.html")
    # ---
    msg = request.get_json()
    print("message-->" + str(msg))
    # ---
    Example1 = """{'update_id':492090605,'message':{'message_id':123,'from':{'id':1348919584,'is_bot':False,'first_name':'i','last_name':'q','username':'Ibrahim_Qasim','language_code':'ar'},'chat':{'id':1348919584,'first_name':'i','last_name':'q','username':'Ibrahim_Qasim','type':'private'},'date':1660520083,'text':'https://www.slideshare.net/Nubiagroup/intense-violence-in-middle-east?qid=e0d987a5-5842-473a-8b63-1d5303759c29&v=&b=&from_search=1','entities':[{'offset':0,'length':130,'type':'url'}]}}"""
    # ---
    global update
    # regex to match slideshare.net links like:
    # ---
    print("return POST0....")
    # ---
    update = Update.de_json(msg, bot)
    # ---
    # your bot can receive updates without messages
    if not update.message:
        if update.effective_chat:
            bot_send_message(chat_id=update.effective_chat.id, text="send a valid slideshare.net link")
        return Response("ok", status=200)
    # chat_id = msg['message']['chat']['id']
    # msg_text = msg['message']['text']
    # ---
    global username
    username = update.message.from_user.username
    # ---
    msg_text = update.message.text
    # ---
    if not msg_text or type(msg_text) != str:
        bot_send_message(chat_id=update.message.chat_id, text="send me slideshare.net link")
        return Response("ok", status=200)
    # ---
    if msg_text in ("/start", "/Start"):
        logger.info("\n In start handler.")
        # Example of retrieving the username from an incoming Telegram update.
        user_data = {}
        if update.message.from_user.username:
            user_data["username"] = update.message.from_user.username
            logger.info("\n Username: {}".format(user_data["username"]))
        # ---
        bot_send_message(chat_id=update.message.chat_id, text="send me slideshare.net link")
        # ---
        return Response("ok", status=200)
    # ---
    if timeout(update.message):
        bot_send_message(chat_id=update.message.chat_id, text="Timeout")
        return Response("ok", status=200)
    # ---
    try:
        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    except Exception as e:
        logger.info(f"Exception: {e}")
        # return Response("ok", status=200)
    # ---
    reg = r"^(https?:\/\/)?(www\.)?slideshare.net\/.*$"
    # ---
    if not re.match(reg, msg_text):
        bot_send_message(chat_id=update.message.chat_id, text="send a valid slideshare.net link")
        return Response("ok", status=200)
    # ---
    bot_send_message(chat_id=update.message.chat_id, text="checking the link..")
    bot_send_message(chat_id=update.message.chat_id, text="Pay 350 BTC to use this bot,\njust kidding.. 😂")
    # ---
    return start_with_url(msg_text)
    # ---


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
# ----
