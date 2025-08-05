import os
from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)

# 配置 Cloudinary
cloudinary.config(
    cloud_name='dpr0pl2tf',
    api_key='548549517251566',
    api_secret='9o-PlPBRQzQPfuVCQfaGrUV3_IE'
)

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 相册页面
@app.route('/album')
def album():
    try:
        folders = cloudinary.api.sub_folders('albums')
        albums = []
        for folder in folders['folders']:
            folder_name = folder['name']
            resources = cloudinary.api.resources(type='upload', prefix=f'albums/{folder_name}/', max_results=1)
            cover_url = resources['resources'][0]['secure_url'] if resources['resources'] else None
            albums.append({'name': folder_name, 'cover_url': cover_url})
        return render_template('albums.html', albums=albums)
    except Exception as e:
        return f"Error fetching albums: {e}", 500

# 查看具体相册
@app.route('/album/<album_name>')
def view_album(album_name):
    try:
        resources = cloudinary.api.resources(type='upload', prefix=f'albums/{album_name}/')
        image_urls = [res['secure_url'] for res in resources['resources']]
        return render_template('view_album.html', album_name=album_name, image_urls=image_urls)
    except Exception as e:
        return f"Error fetching album '{album_name}': {e}", 500

# 上传页面
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            file = request.files['photo']
            folder = request.form['folder']
            upload_result = cloudinary.uploader.upload(file, folder=f"albums/{folder}")
            return redirect(url_for('view_album', album_name=folder))
        except Exception as e:
            return f"Error uploading file: {e}", 500
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)









