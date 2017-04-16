from flask import Flask, render_template
import logging

# Sets the verbosity of console logging
logging.basicConfig(level=logging.DEBUG)

# Any needed Flask configuration can be passed as arguments to this
app = Flask(__name__)


#########
# Routes
#########

@app.route('/', methods=["GET"])
def index():
    return render_template("main.html")


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
