import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# --------------------------
# 第二步：Cloudinary 设置
# --------------------------
cloudinary.config(
    cloud_name="dpr0pl2tf",
    api_key="548549517251566",
    api_secret="9o-PlPBRQzQPfuVCQfaGrUV3_IE"
)

# --------------------------
# 原有配置
# --------------------------
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


@app.route("/story")
def story():
    return render_template("story.html")

# --------------------------------
# 第三步：修改 /upload 路由支持 Cloudinary 上传
# --------------------------------
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        folder = request.form['folder']

        files = request.files.getlist('photos')
        for file in files:
            if file.filename:
                # 上传到 Cloudinary，并指定 folder
                cloudinary.uploader.upload(file,
                                           folder=f"albums/{folder}",
                                           use_filename=True,
                                           unique_filename=False)

        return redirect(url_for('album'))

    return render_template("upload.html")

# 原有：查看单个相册（暂时保留本地功能，如果后续迁移到 Cloudinary，可更新此逻辑）
@app.route("/album/<album_name>")
def view_album(album_name):
    album_path = os.path.join(UPLOAD_FOLDER, album_name)
    if os.path.exists(album_path):
        image_urls = []
        for filename in os.listdir(album_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                image_urls.app_








