import random
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


# Sample data for random titles, image URLs, and detail URLs
random_titles = ["Novel A", "Novel B", "Novel C", "Novel D", "Novel E"]
random_image_urls = ["novel1.jpg", "novel2.jpg",
                     "novel3.jpg", "novel4.jpg", "novel5.jpg"]
random_detail_urls = ["detail1.html", "detail2.html",
                      "detail3.html", "detail4.html", "detail5.html"]

# Generate 100 random novels
novels = []
for i in range(100):
    novel = {
        'id': i + 1,
        'title': random.choice(random_titles),
        'imageUrl': "https://cn-e-pic.mangatoon.mobi/cartoon-posters/258680736e8.webp-posterup4",
        'detailUrl': random.choice(random_detail_urls),
    }
    novels.append(novel)

# Pass the generated novels to the Flask route


@app.route("/list_novel")
def list_novel():
    return render_template("list_novel.html", novels=novels)


if __name__ == "__main__":
    app.run()
