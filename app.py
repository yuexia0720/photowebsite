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

# Home
@app.route('/')
def index():
    return render_template('index.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Album
@app.route('/album')
def album():
    try:
        result = cloudinary.api.subfolders('albums')
        folders = [folder['name'] for folder in result['folders']]
        return render_template('albums.html', folders=folders)
    except Exception as e:
        return f"Error fetching albums: {e}"

# View Album
@app.route('/album/<album_name>')
def view_album(album_name):
    try:
        response = cloudinary.api.resources(type="upload", prefix=f"albums/{album_name}/")
        image_urls = [img['secure_url'] for img in response['resources']]
        return render_template('view_album.html', album_name=album_name, image_urls=image_urls)
    except Exception as e:
        return f"Error: {e}"

# Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        album_name = request.form.get('album_name')
        file = request.files.get('photo')

        if not album_name or not file:
            return "Missing album name or photo", 400

        upload_result = cloudinary.uploader.upload(
            file,
            folder=f"albums/{album_name}/"
        )
        return render_template('upload.html', success=True)

    return render_template('upload.html')

# Story
@app.route('/story', methods=['GET', 'POST'])
def story():
    if request.method == 'POST':
        text = request.form.get('story_text')
        image = request.files.get('story_image')
        if not text or not image:
            return "Missing story text or image", 400
        upload_result = cloudinary.uploader.upload(image, folder="stories/")
        image_url = upload_result['secure_url']
        with open("stories.txt", "a", encoding="utf-8") as f:
            f.write(f"{image_url}||{text}\n")
        return redirect(url_for('story'))

    stories = []
    if os.path.exists("stories.txt"):
        with open("stories.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("||")
                if len(parts) == 2:
                    stories.append({"image_url": parts[0], "text": parts[1]})
    return render_template('story.html', stories=stories)

if __name__ == '__main__':
    app.run(debug=True)








