import os
import cv2
import base64

import numpy as np

from PIL import Image
from io import BytesIO
from collections import Counter
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename

from flask_bootstrap import Bootstrap5
from flask import Flask, flash, redirect, render_template, request, url_for, session


def extract_colors(img_array, num_colors=10):
    def RGB2HEX(color):
        return f"#{int(color[0]):02x}{int(color[1]):02x}{int(color[2]):02x}"

    image = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
    img_width = image.shape[0]
    img_height = image.shape[1]

    reshaped_image = cv2.resize(image, (img_width // 10, img_height // 10))
    reshaped_image = reshaped_image.reshape(
        reshaped_image.shape[0] * reshaped_image.shape[1], 3
    )

    clf = KMeans(n_clusters=num_colors)
    labels = clf.fit_predict(reshaped_image)
    counts = Counter(labels)
    counts = dict(sorted(counts.items()))
    center_colors = clf.cluster_centers_
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    return hex_colors


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 10
app.config["VALID_EXTENSIONS"] = [".jpg"]
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/upload-image", methods=["GET", "POST"])
def recieve_image():
    session.clear()
    if request.method == "POST":
        image = request.files["image"]
        if image:
            filename = secure_filename(image.filename)
            if filename != "":
                file_ext = os.path.splitext(filename)[1]
                if file_ext in app.config["VALID_EXTENSIONS"]:
                    pillow_image = Image.open(image)
                    image_array = np.array(pillow_image)
                    colors = extract_colors(image_array)
                    
                    buffered = BytesIO()
                    pillow_image.save(buffered, format="JPEG")
                    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    return render_template("colors.html", image=img_base64, colors=colors)
                else:
                    flash("Image must be a .jpg type")
            else:
                flash("Invalid file")
        else:
            flash("This field is required!")
    return render_template("upload_image.html")


if __name__ == "__main__":
    app.run()
