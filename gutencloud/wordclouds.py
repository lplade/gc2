from gutencloud.fetch_etext import load_etext
from gutencloud.strip_cruft import strip_headers
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file
from wordcloud import WordCloud
import base64


def get_etext(gutenberg_id):
    raw_text = load_etext(gutenberg_id)
    assert len(raw_text) > 0
    cleaned_text = strip_headers(raw_text).strip()
    assert len(cleaned_text) > 0
    return cleaned_text


def make_cloud(etext,
               width=400, height=400,
               colormap='plasma', background_color='white',
               relative_scaling=0.5):
    """

    :rtype: Image
    """
    assert len(etext) > 0
    wordcloud = WordCloud(width=width, height=height,
                          colormap=colormap,
                          background_color=background_color,
                          relative_scaling=relative_scaling
                          ).generate(etext)
    return base64_encode_pil_image(wordcloud.to_image())



# https://fadeit.dk/blog/2015/04/30/python3-flask-pil-in-memory-image/
def serve_pil_image(pil_img):
    byte_io = BytesIO()
    pil_img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')


# https://stackoverflow.com/questions/42503995/how-to-get-a-pil-image-as-a-base64-encoded-string
def base64_encode_pil_image(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    buffer.seek(0)
    image_bytes = buffer.read()

    b64_encoded_result_bytes = base64.b64encode(image_bytes)
    b64_encoded_result_str = b64_encoded_result_bytes.decode('ascii')
    return b64_encoded_result_str



