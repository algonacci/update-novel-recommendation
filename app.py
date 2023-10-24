import random
from flask import Flask, render_template, request
import module as md

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
        judul = request.form["judul"]
        recommendation = md.rec_pvdbow(title=judul)
        if recommendation is not None and not recommendation.empty:
            return render_template("hasil_rekomendasi.html", recommendation=recommendation, judul=judul)
        else:
            return render_template("rekomendasi.html", error="Judul novel yang dicari tidak ada")
    else:
        return render_template("index.html")


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


@app.route("/detail_page/<int:novel_id>")
def detail_page(novel_id):
    # Fetch the details of the novel with the given novel_id from your data source (e.g., database)
    # You can use the novel_id to retrieve specific novel details

    # Example: Fetch novel details from a database (replace with your data retrieval logic)
    # novel = fetch_novel_details(novel_id)

    # Render the detail_page.html template and pass the novel details to it
    # Example: return render_template("detail_page.html", novel=novel)

    # For demonstration purposes, we'll use a sample novel object
    sample_novel = {
        'id': novel_id,
        'title': 'Sample Novel',
        'author': 'John Doe',
        'description': 'This is a sample novel description.',
        'image_url': 'sample_novel.jpg',
    }

    return render_template("detail_page.html", novel=sample_novel)


if __name__ == "__main__":
    app.run()
