import requests
import io
import base64
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from flask import render_template
from requests.exceptions import MissingSchema

PER_PAGE = 15
UPDATE_TIME = 30

def get_xml(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        return soup
    except MissingSchema:
        return False


def apology(msg, status=400):
    with Image.open('app/static/img/jotaro.jpg').convert('RGBA') as base:

        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)

        error = f'error {str(status)}'
        font1 = ImageFont.truetype(
            "app/static/fonts/RubikGlitch-Regular.ttf", 72)
        size1 = int(font1.getlength(error))

        px = 48
        while True:
            font2 = ImageFont.truetype(
                "app/static/fonts/RubikGlitch-Regular.ttf", px)
            size2 = int(font2.getlength(msg))
            if size2 < 500:
                break
            px -= 10

        x1 = 250 - size1//2
        x2 = 250 - size2//2

        d.text((x1, 515), error, font=font1, fill=(255, 0, 0, 255))
        d.text((x2, 50), msg, font=font2, fill=(0, 0, 0, 255))

        # convert the image to base64
        out = Image.alpha_composite(base, txt)
        img_byte_arr = io.BytesIO()
        out.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base = base64.b64encode(img_byte_arr)
        img = base.decode()

        return render_template('error.html', img=img)
