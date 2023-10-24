from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rekomendasi", methods=["GET", "POST"])
def rekomendasi():
    if request.method == "POST":
        return render_template("hasil_rekomendasi.html")
    else:
        return render_template("rekomendasi.html")


if __name__ == "__main__":
    app.run()
