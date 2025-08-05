import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --------------------------
# Cloudinary 设置
# --------------------------
cloudinary.config(
    cloud_name="dpr0pl2tf",
    api_key="548549517251566",
    api_secret="9o-PlPBRQzQPfuVCQfaGrUV3_IE"
)

# 本地上传文件夹
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/album")
def album():
    folders = []
    for folder_name in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            folders.append(folder_name)
    return render_template("album.html", folders=folders)

@app.route("/album/<album_name>")
def view_album(album_name):
    album_path = os.path.join(UPLOAD_FOLDER, album_name)
    if os.path.exists(album_path):
        image_urls = []
        for filename in os.listdir(album_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                image_urls.append(f"/{UPLOAD_FOLDER}/{album_name}/{filename}")
        return render_template("album_view.html", album_name=album_name, image_urls=image_urls)
    else:
        return "Album not found", 404

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        folder = request.form['folder']

        files = request.files.getlist('photos')
        for file in files:
            if file.filename:
                cloudinary.uploader.upload(file,
                                           folder=f"albums/{folder}",
                                           use_filename=True,
                                           unique_filename=False)
        return redirect(url_for('album'))

    return render_template("upload.html")

# ---- 新增 ----
@app.route("/submit_story", methods=['POST'])
def submit_story():
    story_text = request.form.get('story')
    photo = request.files.get('photo')

    image_url = None

    if photo and photo.filename:
        result = cloudinary.uploader.upload(photo, folder="stories", use_filename=True, unique_filename=False)
        image_url = result['secure_url']

    if not os.path.exists("stories.txt"):
        with open("stories.txt", "w") as f:
            pass

    with open("stories.txt", "a", encoding="utf-8") as f:
        f.write(image_url + "||" + story_text.replace("\n", "\\n") + "\n")

    return redirect(url_for('story'))

@app.route("/story")
def story():
    stories = []
    if os.path.exists("stories.txt"):
        with open("stories.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("||")
                if len(parts) == 2:
                    image_url = parts[0]
                    story_text = parts[1].replace("\\n", "\n")
                    stories.append({"image": image_url, "text": story_text})
    return render_template("story.html", stories=stories)

if __name__ == "__main__":
    app.run(debug=True)









