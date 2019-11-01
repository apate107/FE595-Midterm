from flask import Flask, request, render_template
import services
from pprint import pprint

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("manual.html")


@app.route("/getPOS", methods=['GET'])
def getPOS():
    input_json = request.json or request.args
    return services.getPOS(input_json)


@app.route("/getSimilarity", methods=['GET'])
def getSimilarity():
    input_json = request.json or request.args
    pprint(input_json)
    return services.getSimilarity(input_json)


if __name__ == '__main__':
    app.run(debug=True)