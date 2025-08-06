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
    return render_template("index.html")

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

# 上传图片
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        folder = request.form.get("folder")
        image = request.files.get("image")
        if folder and image:
            cloudinary.uploader.upload(image, folder=folder)
            return redirect(url_for("upload"))
        else:
            return "Missing folder or image", 400
    return render_template("upload.html")

# Story 页面展示
@app.route("/story", methods=["GET"])
def story():
    try:
        stories = cloudinary.api.resources(type="upload", prefix="story")
        story_list = []
        for s in stories["resources"]:
            story_list.append({
                "url": s["secure_url"],
                "caption": s.get("context", {}).get("custom", {}).get("caption", "")
            })
        return render_template("story.html", stories=story_list)
    except Exception as e:
        return f"Error loading stories: {str(e)}"

# Post Story 逻辑
@app.route("/post_story", methods=["POST"])
def post_story():
    try:
        image = request.files["image"]
        caption = request.form["caption"]
        if not image or not caption:
            return "Missing image or caption", 400
        cloudinary.uploader.upload(
            image,
            folder="story",
            context={"caption": caption}
        )
        return redirect(url_for("story"))
    except Exception as e:
        return f"Error posting story: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)








