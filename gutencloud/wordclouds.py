from gutencloud.fetch_etext import load_etext
from gutencloud.strip_cruft import strip_headers
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file
from wordcloud import WordCloud


def get_etext(gutenberg_id):
    raw_text = load_etext(gutenberg_id)
    cleaned_text = strip_headers(raw_text).strip()
    return cleaned_text


def make_cloud(etext,
               width=400, height=400,
               colormap='plasma', background_color='white',
               relative_scaling=0.5):
    """

    :rtype: Image
    """
    wordcloud = WordCloud(width=width, height=height,
                          colormap=colormap,
                          background_color=background_color,
                          relative_scaling=relative_scaling
                          ).generate(etext)
    return serve_pil_image(wordcloud.to_image())


# https://fadeit.dk/blog/2015/04/30/python3-flask-pil-in-memory-image/
def serve_pil_image(pil_img):
    byte_io = BytesIO()
    pil_img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')


