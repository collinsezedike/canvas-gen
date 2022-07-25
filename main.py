from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_bootstrap import Bootstrap5
from extract_colors import extract_colors
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config["SECRET_KEY"] = "asecretkey"

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 10
app.config["UPLOAD_EXTENSIONS"] = [".jpg"]
app.config["UPLOAD_PATH"] = "static\\upload"
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
                if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                    flash("Image must be a .jpg type")
                else:
                    filename = f"image{file_ext}"
                    try:
                        image.save(os.path.join(app.config["UPLOAD_PATH"], filename))
                    except FileNotFoundError:
                        os.chdir(
                            ".\\Day 91\\Professional Project - Image Colour Palette Generator"
                        )
                        image.save(os.path.join(app.config["UPLOAD_PATH"], filename))
                    img_file = f"{app.config['UPLOAD_PATH']}\\image.jpg"
                    session["colors"] = extract_colors(img_file)
                    return redirect(url_for("display_palette"))
            else:
                flash("Invalid file")
        else:
            flash("This field is required!")
    return render_template("upload_image.html")


@app.route("/color-palette/")
def display_palette():
    return render_template("colors.html")


if __name__ == "__main__":
    app.run(debug=True)
