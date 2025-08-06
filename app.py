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
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return "No photo part", 400
        photo = request.files['photo']
        if photo.filename == '':
            return "No selected file", 400
        try:
            upload_result = cloudinary.uploader.upload(photo)
            image_url = upload_result['secure_url']
            albums['Pittsburgh + Cook Forest'].append(image_url)
            return redirect(url_for('album'))
        except Exception as e:
            return f"Upload failed: {str(e)}", 500

    return render_template("upload.html")

# Story 页面：上传 + 展示
@app.route("/story", methods=["GET", "POST"])
def story():
    if request.method == 'POST':
        image = request.files.get('image')
        text = request.form.get('story', '')
        if image and text:
            cloudinary.uploader.upload(
                image,
                folder="story",
                context={"caption": text}
            )
            return redirect(url_for("story"))
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

if __name__ == "__main__":
    app.run(debug=True)




