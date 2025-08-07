from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

app = Flask(__name__)

# 配置 Cloudinary
cloudinary.config(
    cloud_name='dpr0pl2tf',
    api_key='548549517251566',
    api_secret='9o-PlPBRQzQPfuVCQfaGrUV3_IE'
)

# 首页
@app.route("/")
def index():
<<<<<<< HEAD
    image_urls = [
        "https://res.cloudinary.com/dpr0pl2tf/image/upload/v1753816843/WechatIMG2_mzsnw2.jpg",
    ]
    return render_template('index.html', image_urls=image_urls)



@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

if __name__ == "__main__":
    app.run()

=======
    return render_template("index.html")
>>>>>>> 683f55bfdab1562c8cee23ed1dda118305739d20

# About 页面
@app.route("/about")
def about():
    return render_template("about.html")

# Album 页面
@app.route("/album")
def albums():
    try:
        folders = cloudinary.api.root_folders()
        albums = []
        for folder in folders.get('folders', []):
            subfolder_name = folder['name']
            # 获取每个相册的第一张图片作为封面
            resources = cloudinary.api.resources(type="upload", prefix=subfolder_name, max_results=1)
            cover_url = resources['resources'][0]['secure_url'] if resources['resources'] else ""
            albums.append({'name': subfolder_name, 'cover': cover_url})
        return render_template("album.html", albums=albums)
    except Exception as e:
        return f"Error fetching albums: {str(e)}"

# 查看相册内容
@app.route("/album/<album_name>")
def view_album(album_name):
    try:
        resources = cloudinary.api.resources(type="upload", prefix=album_name)
        image_urls = [img["secure_url"] for img in resources["resources"]]
        return render_template("view_album.html", album_name=album_name, image_urls=image_urls)
    except Exception as e:
        return f"Error loading album: {str(e)}"

# ===== Story 页面 =====
stories = []

@app.route("/story", methods=["GET", "POST"])
def story():
    global stories
    if request.method == "POST":
        try:
            image = request.files["image"]
            caption = request.form["caption"]
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result["secure_url"]
            stories.append({"image_url": image_url, "caption": caption})
            return redirect(url_for("story"))
        except Exception as e:
            return f"Upload error: {str(e)}"
    return render_template("story.html", stories=stories)

# ===== Upload 页面（创建文件夹并上传） =====
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        photo = request.files["photo"]
        folder = request.form.get("folder")

        if photo and folder:
            try:
                upload_result = cloudinary.uploader.upload(
                    photo,
                    folder=folder  # Cloudinary will create folder if not exists
                )
                return redirect(url_for("upload"))
            except Exception as e:
                return f"Error uploading file: {str(e)}"

    return render_template("upload.html")



