#!/usr/bin/env python
"""Demo Telegram bot on repl.it.

This program is dedicated to the public domain under the MIT License.

http://www.slideshare.net/MrIbrahem/3-40437776

https://www.slideshare.net/MrIbrahem/3-40437776
https://slideshare.net/MrIbrahem/3-40437776

slideshare.net/MrIbrahem/3-40437776

"""
print(__file__)
import logging
import os
import json
from datetime import datetime, timezone
# import requests
import re
from telegram import (
    Bot,
    ChatAction,
    # KeyboardButton,
    # ParseMode,
    # ReplyKeyboardMarkup,
    Update,
)
import img2pdf
import sys
sys.path.append(os.path.abspath(__dir__))
sys.dont_write_bytecode = True
import shutil
import urllib
import urllib.request
from bs4 import BeautifulSoup
import random
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

today_date = datetime.now().strftime("%Y-%b-%d")
try:
    TOKEN = os.environ['TOKEN']
except Exception as e:
    print("ERROR: Cannot get token from environment:%s" % e)
    #print(os.environ)
    sys.exit(1) 
'''
# urle = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://slidees.mribrahem.repl.co/"
# urle = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url=https://slide-tyob.onrender.com"
'''
#r = requests.get(urle)
#print(r.text)
#---
from flask import Flask, request, render_template, Response
username = False
#---
if not os.path.isdir('pdfs'): os.makedirs("pdfs")
if not os.path.isdir('slides'): os.makedirs("slides")
#---
app = Flask(__name__)
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)
# Define global vars and constants
bot = Bot(token=TOKEN)
#---
bot_msg_id = {1: False, "text": ""}


#---
def tel_send_message(text, edit=False):
    """Send a message to a chat."""
    #payload = { 'chat_id': chat_id, 'text': text }
    #r = requests.post(url, json=payload)
    #return r
    if update.message.chat_id and text != "":
        if not edit:
            try:
                mss = bot.send_message(chat_id=update.message.chat_id,
                                       text=text)
            except Exception as e:
                print('Error line 77 : %s' % e)
        else:
            if not bot_msg_id[1]:
                #---
                try:
                    mss = bot.send_message(chat_id=update.message.chat_id,
                                           text=text)
                except Exception as e:
                    print('Error line 85 : %s' % e)
                #---
                mss1 = '''{'message_id':460,'date':1660592634,'chat':{'id':1348919584,'type':'private','username':'Ibrahim_Qasim','first_name':'i','last_name':'q'},'text':'37Slidesdownloaded','entities':[],'caption_entities':[],'photo':[],'new_chat_members':[],'new_chat_photo':[],'delete_chat_photo':False,'group_chat_created':False,'supergroup_chat_created':False,'channel_chat_created':False,'from':{'id':5473798898,'first_name':'Slidesharebot','is_bot':True,'username':'slides_share_bot'}}'''
                #---
                bot_msg_id[1] = mss.message_id
                bot_msg_id["text"] = mss.text
                logger.info("Message sent:" + mss.message_id)
            else:
                text2 = bot_msg_id["text"] + "\n" + text
                #---
                if text.find("Error downloading slide number") == -1:
                    bot_msg_id["text"] = text2
                #---
                done = False
                try:
                    bot.edit_message_text(chat_id=update.message.chat_id,
                                          message_id=bot_msg_id[1],
                                          text=text2)
                    done = True
                except Exception as e:
                    print('Error line 102 : %s' % e)
                    done = False
                #---
                if not done:
                    try:
                        bot.send_message(chat_id=update.effective_chat.id,
                                         text=text2)
                    except Exception as e:
                        print('Error line 110 : %s' % e)


#---
SLIDES_FOLDER = {
    "dir": os.path.join(os.getcwd(), "slides"),
    "pdfname": "",
    "pdfname2": ""
}
#---
def make_dir_name(t):
    # get directory from url
    pdfname = t
    pdfname = pdfname.split("slideshare.net/")[1]
    pdfname = pdfname.split("?")[0].split("#")[0]
    pdfname = re.sub(r"[\\/:*?\"\'<>|]", "-", pdfname)
    pdfname = pdfname.replace("\n", "")
    #---
    SLIDES_FOLDER["pdfname"] = pdfname
    #---
    dir_name = "slides/" + pdfname
    #---
    logger.info("SLIDES_FOLDER dir:" + dir_name)
    #---
    # create a directory to save the images
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    #---
    return dir_name


#---
def get_title_and_author(soup):
    # j-author-name
    #---
    title = ""
    titles = soup.find_all("span", class_="j-title-breadcrumb")
    if titles:
        title = titles[0].text
        title = re.sub(r"[\\/:*?\"\'<>|]", "-", title)
        title = title.replace("\n", "")
    #---
    author = ""
    authors = soup.find_all("a", class_="j-author-name")
    if authors:
        author = authors[0]
        # get span
        author = author.find("span", itemprop="name")
        if author:
            author = author.text
            #print("author:" + author)
    #---
    if author != "":
        title = title + "-" + author
    #---
    title = re.sub(r"[\\/:*?\"\'<>|]", "-", title)
    title = title.replace("\n", "")
    #---
    SLIDES_FOLDER["pdfname2"] = title
    #print("title:" + title)


#---
def create_image_file(image_path, width, height, numb):
    # edit the previous message
    # create empty image file
    # create an image
    mytext = "Error downloading slide:" + numb

    wi = width or 800
    he = height or 600

    out = Image.new("RGB", (wi, he), "white")

    # get a drawing context
    d = ImageDraw.Draw(out)
    # draw multiline text

    font = ImageFont.truetype("arial.ttf", 36)

    d.text((10, he / 2), mytext, fill=(0, 0, 0), font=font)
    #d.multiline_text((10, he/2), mytext, fill=(0, 0, 0), align="center")
    # write @slides_share_bot at right down corner
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((wi - 250, he - 40),
           "t.me/slides_share_bot",
           fill=(0, 0, 0),
           font=font,
           align="left")
    out.save(image_path)


#---
def download_images(url):
    #---
    url = url
    # Exit if url does not belong to slideshare
    if "slideshare.net" not in url:
        tel_send_message("Invalid link...")
        return False
    #---
    #print("read the url...")
    #print(url)
    #---
    try:
        html = urllib.request.urlopen(url)
    except Exception as e:
        tel_send_message("Can't read the url, try another one...")
        return False
    soup = BeautifulSoup(html, "html.parser")
    #---
    get_title_and_author(soup)
    #---
    '''<source srcset="https://image.slidesharecdn.com/random-141018135304-conversion-gate01/85/2-5-320.jpg?cb=1667313207 320w, https://image.slidesharecdn.com/random-141018135304-conversion-gate01/85/2-5-638.jpg?cb=1667313207 638w, https://image.slidesharecdn.com/random-141018135304-conversion-gate01/75/2-5-2048.jpg?cb=1667313207 2048w" sizes="100vw" type="image/webp">'''
    #---
    images = soup.find_all("source", attrs={"type": "image/webp"})
    #---
    if not images:
        # print("No images found")
        images = soup.find_all("img", class_="slide-image")
    #---
    # Exit if presentation not found
    if not images:
        tel_send_message("No slides were found...")
        return False
    #---
    # get directory from url
    SLIDES_FOLDER["dir"] = make_dir_name(url)
    #---
    no_of_images = len(images)
    #---
    line = "Slides to download:" + no_of_images
    # tel_send_message(line, edit=True)
    #---
    # get image hight and width
    width, height = 0, 0
    #---
    img_errors = 0
    img_success = 0
    #---
    # Parallelize slide downloading
    numb = 0
    for idx, image in enumerate(images, start=1):
        numb += 1
        # Get image url from srcset attribute (csv of image urls, with last value being the highest res)
        image_url = image.get("srcset").split(",")[-1].split("?")[0]
        # Format image name to include slide index (with leading zeros)
        image_name = str(idx).zfill(len(str(no_of_images))) + "-" + image_url.split("/")[-1]
        # Save path of image (cwd/slides/image_name)
        image_path = os.path.join(SLIDES_FOLDER["dir"], image_name)

        # Check if slide is already downloaded
        if os.path.isfile(image_path):
            print("Slide: %s exists" % str(idx) )
            img_success += 1
        else:
            try:
                urllib.request.urlretrieve(image_url, image_path)
                img_success += 1
                # get image hight and width
                if not width and not height:
                    im = Image.open(image_path)
                    width, height = im.size
            except Exception as e:
                img_errors += 1
                logger.info("Error downloading slide:" + image_url)
                tel_send_message("Error downloading slide number %d " % numb,
                                 edit=True)
                create_image_file(image_path, width, height, numb)

    # "\x1b[1K" clear to end of line
    tel_send_message("%d Slides downloaded with best quality, %d errors" %
                     (img_success, img_errors))
    if img_success == 0:
        tel_send_message("Can't download any slides...")
        return False
    return SLIDES_FOLDER["dir"]


#---
def get_json_table(jsfile):
    if not os.path.isfile(jsfile):
        with open(jsfile, 'w') as f:
            json.dump({'test': {"count": 1}}, f)
    #---
    jsonfile = open(jsfile, 'r').read()
    #---
    tab = {}
    try:
        tab = json.loads(jsonfile)
    except Exception as e:
        tab = {}
    #---
    return tab


#---
def log_one(jsfile='users.json', val=''):
    #---
    tab = get_json_table(jsfile)
    #---
    if not tab.get(val):
        tab[val] = {"count": 1}
    else:
        tab[val]["count"] += 1
    #---
    with open(jsfile, 'w') as f:
        json.dump(tab, f)


#---
def convert_to_pdf(pdf_name, images_dir):
    if not os.path.isdir(images_dir) : return False
    # Get all slides sorted by name
    slides = [os.path.join(images_dir, s) for s in os.listdir(images_dir)]

    print("Generating pdf...")

    # Combine slides into a pdf using img2pdf
    pdf_bytes = img2pdf.convert(slides)
    file1 = "pdfs/" + pdf_name + ".pdf"
    file2 = "pdfs/result%s.pdf" % random.randint(0, 99)  # random file name
    file_true = ""
    try:
        with open(file1, "wb") as pd:
            pd.write(pdf_bytes)
            print("Generated: " + file1)
        pd.close()
        file_true = file1
    except PermissionError:
        print("PermissionError")
        with open(file2, "wb") as pd2:
            pd2.write(pdf_bytes)
            print("saved to :" + file2)
        pd2.close()
        file_true = file2
    except Exception as e:
        print("Exception: %s" % e)
        tel_send_message("Exception: %s" % e)
        return ""
    #---
    if file_true != "":
        # Remove "slides" folder
        # remove the folder and all the contents
        #os.rmdir(images_dir)
        shutil.rmtree(images_dir)
    return file_true


#---
def start_with_url(url):
    bot.send_chat_action(chat_id=update.message.chat_id,
                         action=ChatAction.UPLOAD_DOCUMENT)
    images_dir = download_images(url)
    if not images_dir:
        return Response("ok", status=200)
    pdf_name = SLIDES_FOLDER["pdfname"]


    result_file = convert_to_pdf(pdf_name, images_dir)
    if not result_file or result_file == "":
        tel_send_message("Error generating pdf")
        return Response("ok", status=200)
    #---
    log_one(jsfile='users.json', val=username)
    log_one(jsfile='dates.json', val=today_date)
    #---
    # Send pdf to telegram
    filename2 = SLIDES_FOLDER['pdfname2'] + ".pdf"
    bot.send_document(
        chat_id=update.message.chat_id,
        document=open(result_file, "rb"),
        #caption=f"{SLIDES_FOLDER['pdfname2']}",
        filename=filename2)
    #---
    # delete the pdf file
    os.remove(result_file)
    #---
    return Response("ok", status=200)


#---
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


#---
def timeout(message, max=60000):
    try:
        event_age_ms = get_message_age(message)
    except Exception as e:
        logger.info( 'timeout except: ' + e )
    # Ignore events that are too old
    if event_age_ms < max:
        return False
    else:
        if update.effective_chat:
            try:
                bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=
                    'I thought you left. Please use /start command to restart the bot.'
                )
            except Exception as e:
                print('Error line 416 : %s' % e)
        logger.info('\n Dropped {} (age {}ms)'.format(update.update_id,
                                                      event_age_ms))
        return True


#---
def returnwebsite():
    print('returnwebsite111.')
    #---
    text = '''
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
<h1>Welcome223!</h1>
'''
    text += "<table><tr><td>"
    #---
    tab = get_json_table('users.json')
    text += "<table class='sortable table table-striped alignleft'><tr><th>user</th><th>count</th></tr>"
    #---
    for user, count in tab.items():
        text += '<tr><td>' + user + '</td><td>' + count + '</td></tr>'
    #---
    text += "</table>"
    #---
    text += "</td>"
    text += "<td>"
    #---
    tab2 = get_json_table('dates.json')
    text += "<table class='sortable table table-striped alignleft'><tr><th>date</th><th>count</th></tr>"
    #---
    for date, count in tab2.items():
        text += '<tr><td>' + date + '</td><td>' + count + '</td></tr>'
    #---
    text += "</table>"
    #---
    text += "</td>"
    #---
    text += "</table>"
    #---
    return text


#---
@app.route('/users', methods=['GET'])
def users():
    return open('users.json', 'r').read()


#---
@app.route('/dates', methods=['GET'])
def dates():
    return open('dates.json', 'r').read()


#---
@app.route('/', methods=['POST', 'GET'])
#---
def index():
    print( 'method: ' + request.method)
    if request.method != "POST":
        return render_template('x3.html')
    #---
    msg = request.get_json()
    print("message-->" + str(msg))
    #---
    Example1 = '''{'update_id':492090605,'message':{'message_id':123,'from':{'id':1348919584,'is_bot':False,'first_name':'i','last_name':'q','username':'Ibrahim_Qasim','language_code':'ar'},'chat':{'id':1348919584,'first_name':'i','last_name':'q','username':'Ibrahim_Qasim','type':'private'},'date':1660520083,'text':'https://www.slideshare.net/Nubiagroup/intense-violence-in-middle-east?qid=e0d987a5-5842-473a-8b63-1d5303759c29&v=&b=&from_search=1','entities':[{'offset':0,'length':130,'type':'url'}]}}'''
    #---
    global update
    # regex to match slideshare.net links like:
    #---
    print('return POST0....')
    #---
    update = Update.de_json(msg, bot)
    #---
    # your bot can receive updates without messages
    if not update.message:
        if update.effective_chat:
            try:
                bot.send_message(chat_id=update.effective_chat.id,
                                 text='send a valid slideshare.net link')
            except Exception as e:
                print('Error line 496 : %s' % e)
        return Response("ok", status=200)
    # chat_id = msg['message']['chat']['id']
    # msg_text = msg['message']['text']
    #---
    global username
    username = update.message.from_user.username
    #---
    msg_text = update.message.text
    #---
    if not msg_text or type(msg_text) != str:
        try:
            bot.send_message(chat_id=update.message.chat_id,
                             text='send me slideshare.net link')
        except Exception as e:
            print('Error line 498 : %s' % e)
        return Response("ok", status=200)
    #---
    if msg_text in ("/start", "/Start"):
        logger.info("\n In start handler.")
        # Example of retrieving the username from an incoming Telegram update.
        user_data = {}
        if update.message.from_user.username:
            user_data['username'] = update.message.from_user.username
            logger.info('\n Username: {}'.format(user_data['username']))
        try:
            bot.send_message(chat_id=update.message.chat_id,
                             text='send me slideshare.net link')
        except Exception as e:
            print('Error line 511 : %s' % str(e))
        return Response("ok", status=200)
    #---
    #if timeout(update.message):
    #bot.send_message(chat_id=update.message.chat_id, text="Timeout")
    #return
    #---
    try:
        bot.send_chat_action(chat_id=update.message.chat_id,
                             action=ChatAction.TYPING)
    except Exception as e:
        logger.info('Exception: {e}' + str(e) )
        return Response("ok", status=200)
    #---
    reg = r'^(https?:\/\/)?(www\.)?slideshare.net\/.*$'
    #---
    valid_link = False
    #---
    if re.match(reg, msg_text):
        valid_link = True
        texts = "checking the link"
    else:
        texts = 'send a valid slideshare.net link'
    #---
    try:
        bot.send_message(chat_id=update.message.chat_id, text=texts)
    except Exception as e:
        print('Error line 550 : %s' % e)
    #---
    if valid_link:
        return start_with_url(msg_text)
    else:
        return Response("ok", status=200)
    #---
    #return Response("ok", status=200)


#---
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=8080)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
#----S
