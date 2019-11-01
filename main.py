from flask import Flask, request, render_template
import services
import inspect

app = Flask(__name__)


def getDocumentation():
    """
    Retrieve the docstrings for each service to show on manual.html
    :return: a dictionary of each service and its docstring
    """
    svcs = inspect.getmembers(services, predicate=inspect.isfunction)
    svcs = [s for s in svcs if s[0] not in ['abort', 'jsonify']]
    return {k: [s.strip() for s in v.__doc__.split('\n') if s.strip()] for k, v in svcs}


@app.route("/")
def home():
    return render_template("manual.html", doc=getDocumentation())


@app.route("/getPOS", methods=['GET'])
def getPOS():
    input_json = request.json or request.args
    return services.getPOS(input_json)


@app.route("/getSimilarity", methods=['GET'])
def getSimilarity():
    input_json = request.json or request.args
    return services.getSimilarity(input_json)


if __name__ == '__main__':
    app.run(debug=True)