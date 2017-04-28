# Note that the main Flask imports are in orm.py
from .orm import *
from flask import render_template, request, redirect
from .fetch_etext import *
from .strip_cruft import *
import logging

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

    return render_template("main.html")


@app.route('/pgsearch', methods=["POST"])
def pg_search():
    if request.method == "POST":

        # TODO parse the form
        # TODO do some stuff with that
        # TODO process output from that

        # TODO render a thing
        pass
    else:
        # We should not access this route by GET
        return redirect("/", code=302)


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
