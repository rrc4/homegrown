from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def feed():
    return render_template("feed.html")


if __name__ == '__main__':
    app.run()
