#!/usr/bin/env python
"""

"""
import os
import json
import requests
import re
import sys
import shutil
import random
import urllib
import urllib.request
from datetime import datetime

from bs4 import BeautifulSoup
import img2pdf
from PIL import Image, ImageDraw, ImageFont

today_date = datetime.now().strftime("%Y-%m-%d")
sys.dont_write_bytecode = True

if not os.path.isdir("pdfs"):
    os.makedirs("pdfs")
if not os.path.isdir("slides"):
    os.makedirs("slides")

Print_result = False

from get_urls import get_slide_urls


def printe(s):
    if Print_result:
        return
    # ---
    print(s)


loggerinfo = printe
username = False


def make_file_and_dir_name(t):
    # get directory from url
    pdfname = t
    pdfname = pdfname.split("slideshare.net/")[1]
    pdfname = pdfname.split("?")[0].split("#")[0]
    pdfname = re.sub(r"[\\/:*?\"\'<>|]", "-", pdfname)
    pdfname = pdfname.replace("\n", "")
    # ---
    dir_name = "slides/" + pdfname
    # ---
    loggerinfo(f"SLIDES dir: {dir_name}")
    # ---
    # create a directory to save the images
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    # ---
    return pdfname, dir_name


def get_title_and_author(soup):
    # j-author-name
    # ---
    title = ""
    titles = soup.find_all("span", class_="j-title-breadcrumb")
    if titles:
        title = titles[0].text
        title = re.sub(r"[\\/:*?\"\'<>|]", "-", title)
        title = title.replace("\n", "")
    # ---
    author = ""
    authors = soup.find_all("a", class_="j-author-name")
    if authors:
        author = authors[0]
        # get span
        author = author.find("span", itemprop="name")
        if author:
            author = author.text
            # loggerinfo("author:" + author)
    # ---
    if author != "":
        title = title.strip() + "-" + author.strip()
    # ---
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"[\\/:*?\"\'<>|]", "-", title)
    title = title.replace("\n", "").replace("-", " ")
    # ---
    return title


def create_image_file(image_path, width, height, numb):
    # edit the previous message
    # create empty image file
    # create an image
    mytext = f"Error downloading slide: {numb}"

    wi = width or 800
    he = height or 600

    out = Image.new("RGB", (wi, he), "white")

    # get a drawing context
    d = ImageDraw.Draw(out)
    # draw multiline text

    font = ImageFont.truetype("arial.ttf", 36)

    d.text((10, he / 2), mytext, fill=(0, 0, 0), font=font)
    # d.multiline_text((10, he/2), mytext, fill=(0, 0, 0), align="center")
    # write @slides_share_bot at right down corner
    font = ImageFont.truetype("arial.ttf", 24)
    d.text((wi - 250, he - 40), "t.me/slides_share_bot", fill=(0, 0, 0), font=font, align="left")
    out.save(image_path)


def get_json_table(jsfile):
    if not os.path.isfile(jsfile):
        with open(jsfile, "w", encoding="utf-8") as f:
            json.dump({"test": {"count": 1}}, f)
    # ---
    with open(jsfile, "r", encoding="utf-8") as f:
        jsonfile = f.read()
    # ---
    tab = {}
    try:
        tab = json.loads(jsonfile)
    except Exception as e:
        tab = {}
    # ---
    return tab


def log_one(jsfile="users.json", val=""):
    # ---
    tab = get_json_table(jsfile)
    # ---
    if not tab.get(val):
        tab[val] = {"count": 1}
    else:
        tab[val]["count"] += 1
    # ---
    with open(jsfile, "w", encoding="utf-8") as f:
        json.dump(tab, f)


def convert_to_pdf(pdf_name, images_dir):
    # ---
    # Get all slides sorted by name
    slides = [os.path.join(images_dir, s) for s in os.listdir(images_dir)]

    # loggerinfo("Generating pdf...")

    # Combine slides into a pdf using img2pdf
    pdf_bytes = img2pdf.convert(slides)
    file1 = f"pdfs/{pdf_name}.pdf"
    file2 = "pdfs/result%s.pdf" % random.randint(0, 99)  # random file name
    file_true = ""
    try:
        with open(file1, "wb") as pd:
            pd.write(pdf_bytes)
            # loggerinfo(f"Generated: {file1}")
        pd.close()
        file_true = file1
    except PermissionError:
        # loggerinfo("PermissionError")
        with open(file2, "wb") as pd2:
            pd2.write(pdf_bytes)
            # loggerinfo(f"saved to : {file2}")
        pd2.close()
        file_true = file2
    except Exception as e:
        # loggerinfo("Exception: %s" % e)
        return "err", "Exception: %s" % e
    # ---
    if file_true != "":
        # Remove "slides" folder
        # remove the folder and all the contents
        # os.rmdir(images_dir)
        shutil.rmtree(images_dir)
        return True, file_true
    # ---
    return "err", ""


def get_urls2(soup):
    """<source srcset="https://image.slidesharecdn.com/random-141018135304-conversion-gate01/85/2-5-320.jpg?cb=1667313207 320w, https://image.slidesharecdn.com/random-141018135304-conversion-gate01/85/2-5-638.jpg?cb=1667313207 638w, https://image.slidesharecdn.com/random-141018135304-conversion-gate01/75/2-5-2048.jpg?cb=1667313207 2048w" sizes="100vw" type="image/webp">

    <div class="slide current" id="slide-0" data-index="0">
        <picture>
            <source srcset="https://image.slidesharecdn.com/mon3m-210120210312/85/-1-320.jpg?cb=1671595783 320w, https://image.slidesharecdn.com/mon3m-210120210312/85/-1-638.jpg?cb=1671595783 638w, https://image.slidesharecdn.com/mon3m-210120210312/75/-1-2048.jpg?cb=1671595783 2048w" sizes="100vw" type="image/webp">
            <img class="slide-image" alt="Sensitivity: Internal" data-index="1" src="https://image.slidesharecdn.com/mon3m-210120210312/85/-1-320.jpg?cb=1671595783" srcset="https://image.slidesharecdn.com/mon3m-210120210312/85/-1-320.jpg?cb=1671595783 320w, https://image.slidesharecdn.com/mon3m-210120210312/85/-1-638.jpg?cb=1671595783 638w" sizes="100vw" id="slide-image-0">
        </picture>
    </div>
    """
    # ---
    urltabs = {}
    # ---
    qualties = []
    # ---
    images2 = soup.find_all("source", attrs={"type": "image/webp"})
    for id2, imageo in enumerate(images2, start=1):
        tests1 = [x.strip() for x in imageo.get("srcset").split(",")]
        tab3 = {}
        # ---
        for x in tests1:
            regex_url = r"(https?:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&;\?\#\/.=]+) (\d+)w"
            uux = re.match(regex_url, x)
            if uux:
                q = int(uux.group(2))
                if q not in qualties:
                    qualties.append(q)
                tab3[q] = uux.group(1).split("?")[0].strip().split("#")[0].strip()
        # ---
        if tab3 == {}:
            tab3[320] = imageo.get("srcset").split(",")[-1].split("?")[0].strip()
        # ---
        # sort tab3 by big key
        tab3 = {k: v for k, v in sorted(tab3.items(), key=lambda item: item[0], reverse=True)}
        # ---
        urltabs[id2] = tab3
    # ---
    key = 320
    if len(qualties) == 3:
        key = qualties[1]
    # ---
    return urltabs, key


def download_images(fa_dir, url):
    # ---
    global username
    # ---
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        html = response.text
    except Exception as e:
        return "err", "Can't read the url, try another one..."
    # ---
    soup = BeautifulSoup(html, "html.parser")
    # ---
    pdfname2 = get_title_and_author(soup)
    # ---
    # urltabs, key = get_urls2(soup)
    key = 320
    urltabs = get_slide_urls(url)
    # ---
    loggerinfo(f"len of urltabs : {len(urltabs)}")
    # ---
    if not urltabs or urltabs == {}:
        return "err", "No slides were found..."
    # ---
    no_of_images = len(urltabs)
    # ---
    width, height = 0, 0
    # ---
    img_errors = 0
    img_success = 0
    # ---
    numb = 0
    # for idx, image in enumerate(urltabs.items(), start=1):
    for idx, image in urltabs.items():
        numb += 1
        # Get image url from srcset attribute (csv of image urls, with last value being the highest res)
        # ---
        # images_d = {}
        # ---
        firstkey = list(image.keys())
        firstkey = list(image.keys())[0]
        # ---
        if username == "Ibrahim_Qasim":
            key = firstkey
        # ---
        image_url = image.get(key) or image.get(firstkey)
        # ---
        loggerinfo(image_url)
        # ---
        # Format image name to include slide index (with leading zeros)
        xx = str(idx).zfill(len(str(no_of_images)))
        # ---
        image_name = f'{xx}-{image_url.split("/")[-1]}'
        # ---
        # Save path of image (cwd/slides/image_name)
        image_path = os.path.join(fa_dir, image_name)
        # ---
        # Check if slide is already downloaded
        if os.path.isfile(image_path):
            loggerinfo(f"Slide: {idx} exists")
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
                loggerinfo(f"Error downloading slide: {image_url}")
                # ---
                create_image_file(image_path, width, height, numb)
    # ---
    # "\x1b[1K" clear to end of line
    message = "%d Slides downloaded quality:%d, %d errors" % (img_success, key, img_errors)
    # ---
    if img_success == 0:
        return "err", "Can't download any slides..."
    # ---
    tab = {"pdfname2": pdfname2, "message": message}
    # ---
    return True, tab


def start_with_url(url, Username, tel_send_message, Loggerinfo, printresult=False):
    # ---
    global loggerinfo, Print_result
    # ---
    Print_result = printresult
    # ---
    if Loggerinfo is False:
        loggerinfo = Loggerinfo
    # ---
    global username
    username = Username
    # ---
    # get directory from url
    pdf_name, imgs_dir = make_file_and_dir_name(url)
    # ---
    if imgs_dir in ["", False]:
        loggerinfo(f"imgs_dir:{imgs_dir}..")
        return "err", "Error imgs_dir"
    # ---
    if not os.path.isdir(imgs_dir):
        return "err", "Error imgs_dir"
    # ---
    _d, tab = download_images(imgs_dir, url)
    # ---
    if _d == "err" or _d is not True:
        return "err", tab
    # ---
    pdfname2 = ""
    # ---
    if isinstance(tab, dict) and _d is True:
        pdfname2 = tab.get("pdfname2", "")
        msg = tab.get("message", "")
        if msg != "" and tel_send_message is False:
            tel_send_message(msg)
    # ---
    _err2, result_file = convert_to_pdf(pdf_name, imgs_dir)
    # ---
    if _err2 == "err":
        return "err", result_file
    # ---
    if not result_file or result_file == "":
        return "err", "Error generating pdf"
    # ---
    log_one(jsfile="users.json", val=username)
    log_one(jsfile="dates.json", val=today_date)
    # ---
    # Send pdf to telegram
    title = f"{pdfname2}.pdf"
    # ---
    tab = {"title": title, "filepath": result_file}
    # ---
    return "file", tab


if __name__ == "__main__":
    url = "https://www.slideshare.net/slideshow/ss-138929641/138929641?from_search=0"
    _co, result = start_with_url(url, "Ibrahim_Qasim", printe, printe)
    print(_co)
    print(result)
