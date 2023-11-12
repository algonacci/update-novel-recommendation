import os
from flask import Flask, render_template, request
import module as md
import pandas as pd

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/rekomendasi", methods=["GET", "POST"])
def rekomendasi():
    return render_template("rekomendasi.html")


@app.route("/hasil_rekomendasi", methods=["POST"])
def hasil_rekomendasi():
    if request.method == "POST":
        input_text = request.form.get("input_text")
        try:
            recommendation = md.rec_pvdbow_by_text(input_text)
            if recommendation is not None and not recommendation.empty:
                return render_template("hasil_rekomendasi.html", recommendation=recommendation, input_text=input_text)
        except KeyError:
            return render_template("rekomendasi.html", error="Data untuk teks yang dimasukkan tidak ditemukan")
    else:
        return render_template("index.html")


@app.route("/list_novel")
def list_novel():
    novels = pd.read_csv("novel_data.csv")
    novels = novels.to_dict(orient="records")

    # Add an ID field to each dictionary
    for i, novel in enumerate(novels):
        novel['id'] = i

    return render_template("list_novel.html", novels=novels)


@app.route("/detail_page/<int:novel_id>")
def detail_page(novel_id):
    novels = pd.read_csv("novel_data.csv")
    novels = novels.to_dict(orient="records")

    # Assign IDs as you did in the list_novel function
    for i, novel in enumerate(novels):
        novel['id'] = i

    # Find the novel with the given 'id'
    selected_novel = None
    for novel in novels:
        if novel['id'] == novel_id:
            selected_novel = novel
            break

    if selected_novel is None:
        return "Novel not found", 404

    recommendations = md.rec_pvdbow_by_text(selected_novel['Title'])[:6]
    recommendations = recommendations.to_dict(orient='records')

    print(recommendations)

    return render_template("detail_page.html", novel=selected_novel, recommendations=recommendations)


@app.route("/data_novel")
def data_novel():
    df = pd.read_csv('novel_data.csv')
    return render_template('data_novel.html', df=df)


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8080)))
