from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file
from wordcloud import WordCloud


def make_cloud(etext):
    """

    :rtype: Image
    """
    wordcloud = WordCloud(width=400, height=400,
                          colormap='plasma',
                          background_color='white',
                          relative_scaling=0.5).generate(etext)
    return serve_pil_image(wordcloud.to_image())


# https://fadeit.dk/blog/2015/04/30/python3-flask-pil-in-memory-image/
def serve_pil_image(pil_img):
    byte_io = BytesIO()
    pil_img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/png')


