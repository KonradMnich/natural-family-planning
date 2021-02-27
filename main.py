import flask
import backend_code


app = flask.Flask(__name__)


@app.route("/home")
@app.route("/")
def home():
    return flask.render_template("home.html")


@app.route("/measurement")
def measurement():
    return flask.render_template("measurement.html")


@app.route("/mucus")
def mucus():
    return flask.render_template("mucus.html")


@app.route("/summary", methods=["post", "get"])
def summary():
    # get value from the form
    temperature = flask.request.form.get("temp")
    # adjust the message
    message, temperature = backend_code.asses_temperature(temperature)

    # save results if appropriate
    if isinstance(temperature, (float, int)):
        backend_code.save_temperature(temperature)

    return flask.render_template("summary.html", message=message)


@app.route("/summary_mucus", methods=["post", "get"])
def summary_mucus():
    return flask.render_template("summary_mucus.html")


@app.route("/visualisation")
def visualisation():
    image_path = backend_code.create_plot()
    return flask.render_template("visualisation.html", image=image_path)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
