import simplejson
import flask
import arrow

app = flask.Flask(__name__)


@app.route("/")
def index():
    peers = simplejson.load(open("data.json"))
    return flask.render_template("index.html", peers=peers, arrow=arrow)


app.run(debug=True)
