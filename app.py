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
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/story')
def story():
    return render_template('story.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        album_name = request.form.get('album')
        file = request.files['photo']
        if album_name and file:
            folder_path = f"albums/{album_name}"
            cloudinary.uploader.upload(file, folder=folder_path)
        return render_template('upload.html', success=True)
    return render_template('upload.html')

@app.route('/album')
def album():
    try:
        # 获取 albums/ 下所有资源，获取所有文件夹名称
        result = cloudinary.api.resources(type='upload', prefix='albums/', resource_type='image')
        albums = set()
        for item in result['resources']:
            folder = item['public_id'].split('/')[1] if '/' in item['public_id'] else 'default'
            albums.add(folder)
        return render_template('albums.html', albums=sorted(list(albums)))
    except Exception as e:
        return f"Error fetching albums: {e}"

@app.route('/album/<album_name>')
def view_album(album_name):
    try:
        prefix = f"albums/{album_name}/"
        result = cloudinary.api.resources(type='upload', prefix=prefix, resource_type='image')
        image_urls = [item['secure_url'] for item in result['resources']]
        return render_template('view_album.html', album_name=album_name, image_urls=image_urls)
    except Exception as e:
        return f"Error fetching album images: {e}"

if __name__ == '__main__':
    app.run(debug=True)








