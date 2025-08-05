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
        traceback.print_exc()
        return f"Error rendering story page: {str(e)}"

@app.route("/submit_story", methods=["POST"])
def submit_story():
    try:
        story_text = request.form.get("story")
        photo = request.files.get("photo")
        image_url = None

        if photo:
            upload_result = cloudinary.uploader.upload(photo, folder="stories")
            image_url = upload_result.get("secure_url")

        print("Story submitted:", story_text)
        print("Image URL:", image_url)

        return redirect(url_for("story"))

    except Exception as e:
        traceback.print_exc()
        return f"Error submitting story: {str(e)}"

# 上传页面
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        photo = request.files.get("photo")
        folder = request.form.get("folder")

        if not photo or not folder:
            return "Missing photo or folder", 400

        try:
            cloudinary.uploader.upload(
                photo,
                folder=f"albums/{folder}"
            )
            return redirect(url_for("albums"))
        except Exception as e:
            traceback.print_exc()
            return f"Error uploading photo: {str(e)}"

    return render_template("upload.html")

# 显示用户通过网站上传的相册，删除很旧的 cloudinary 文件夹查询
@app.route("/albums")
def albums():
    try:
        response = cloudinary.api.resources(
            type="upload",
            prefix="albums/",
            max_results=100
        )
        image_urls = [item['secure_url'] for item in response['resources']]
        return render_template("albums.html", image_urls=image_urls)
    except Exception as e:
        traceback.print_exc()
        return f"Error fetching album images: {str(e)}"

# 查看某一相册内的所有图片
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
        traceback.print_exc()
        return f"Error fetching album '{album_name}': {str(e)}"










