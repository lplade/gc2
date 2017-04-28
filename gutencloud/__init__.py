# Note that the main Flask imports are in orm.py
from gutencloud.orm import *
from flask import render_template, request, redirect
from gutencloud.fetch_etext import *
from gutencloud.strip_cruft import *
import logging

# How many entries to display in list of top books
TOP_LIST = 20

# Sets the verbosity of console logging
logging.basicConfig(level=logging.DEBUG)

# tell flask where folders are
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


#########
# Routes
#########

@app.route('/', methods=["GET"])
def index():
    # Return the most downloaded books from Project Gutenberg to get users started
    top_books = Ebook.query.order_by(Ebook.downloads.desc()).limit(TOP_LIST).all()
    return render_template("main.html", top_books=top_books)


@app.route('/search_author', methods=["POST"])
def search_author():
    if request.method == "POST":
        result_list = Ebook.query.filter(Ebook.author.like('\%{}\%'.format(
            request.form['author_query']
        )))
        if result_list is None:
            return render_template('notfound.html', type='author', query=request.form['author_query'])
        else:
            return render_template('author_results.html', authors=result_list)
    else:
        # We should not access this route by GET
        return redirect("/", code=302)


@app.route('/search_title', methods=["POST"])
def search_title():
    if request.method == "POST":
        result_list = Ebook.query.filter(Ebook.title.like('\%{}\%'.format(
            request.form['title_query']
        )))
        if result_list is None:
            return render_template('notfound.html', type='author', query=request.form['title_query'])
        else:
            return render_template('title_results.html', titles=result_list)
    else:
        # Should not access this by GET
        return redirect('/', code=302)


@app.route('/wordcloud/<int:ebook_id>', methods=["GET"])
def render_wordcloud(ebook_id):

    ebook = Ebook.query.get(ebook_id)
    if ebook is None:
        return render_template('notfound.html', type='e-book', query=str(ebook_id))
    else:
        # TODO heart of the application. Grab the etext from PG, render a wordcloud
        pass


# Leave this as the last route
@app.route("/<path:path>")
def serve_static(path):
    """
    Assume any request not matching above routes is request for static resource
    :param path:
    :return:
    """
    return app.send_static_file(path)

##################
# Run application
##################

if __name__ == '__main__':
    app.run()
