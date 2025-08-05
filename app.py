import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
import traceback

app = Flask(__name__)

# Cloudinary 设置
cloudinary.config(
    cloud_name="dpr0pl2tf",
    api_key="548549517251566",
    api_secret="9o-PlPBRQzQPfuVCQfaGrUV3_IE"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/story")
def story():
    try:
        stories = [
            {"text": "First story!", "image": "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1754343393/pexels-caio-69969_aq5kzz.jpg"},
            {"text": "Another story.", "image": "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1754343392/pexels-samuel-walker-15032-569098_wm1kxg.jpg"}
        ]
        return render_template("story.html", stories=stories)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Error rendering story page: {str(e)}"

@app.route("/submit_story", methods=["POST"])
def submit_story():
    text = request.form.get("text")
    image_url = request.form.get("image_url")
    # 暂时先简单处理，后续可以存储
    return redirect(url_for("story"))

# 上传页面（支持上传到 Cloudinary）
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        folder = request.form['folder']
        files = request.files.getlist('photos')
        for file in files:
            if file.filename:
                cloudinary.uploader.upload(
                    file,
                    folder=f"albums/{folder}",
                    use_filename=True,
                    unique_filename=False
                )
        return redirect(url_for('album'))
    return render_template("upload.html")

# ✅ 获取所有相册（Cloudinary 文件夹）
@app.route("/album")
def album():
    try:
        result = cloudinary.api.subfolders("albums")
        folders = result.get("subfolders", [])

        # 每个相册显示一张封面图（获取该文件夹中最新一张图）
        albums = []
        for folder in folders:
            folder_name = folder["name"]
            resources = cloudinary.api.resources(
                type="upload",
                prefix=f"albums/{folder_name}/",
                max_results=1,
                direction="desc"
            )
            cover_url = None
            if resources["resources"]:
                cover_url = resources["resources"][0]["secure_url"]

            albums.append({
                "name": folder_name,
                "cover": cover_url
            })

        return render_template("album.html", albums=albums)

    except Exception as e:
        traceback.print_exc()  # 打印详细错误信息
        return f"Error fetching albums: {str(e)}"

# ✅ 查看某个相册的所有图片（Cloudinary 查询）
@app.route("/album/<album_name>")
def view_album(album_name):
    try:
        response = cloudinary.api.resources(
            type="upload",
            prefix=f"albums/{album_name}/",
            max_results=100
        )
        image_urls = [item["secure_url"] for item in response.get("resources", [])]
        return render_template("view_album.html", album_name=album_name, image_urls=image_urls)

    except Exception as e:
        return f"Error fetching album '{album_name}': {str(e)}"

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        album_name = request.form["album"]
        result = cloudinary.uploader.upload(
            file,
            folder=f"albums/{album_name}/"
        )
        return redirect(url_for("album"))
    return render_template("upload.html")









