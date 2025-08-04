import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 保证上传路径存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/album")
def album():
    albums = {}
    for folder_name in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            image_urls = [f"/{UPLOAD_FOLDER}/{folder_name}/{file}" for file in os.listdir(folder_path)]
            albums[folder_name] = image_urls
    return render_template("album.html", albums=albums)

@app.route("/story")
def story():
    return render_template("story.html")

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        folder = request.form['folder']
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(folder_path, exist_ok=True)

        files = request.files.getlist('photos')
        for file in files:
            if file.filename:
                file.save(os.path.join(folder_path, file.filename))

        return redirect(url_for('album'))

    return render_template("upload.html")

# 提供静态图片文件服务
@app.route('/static/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)

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









