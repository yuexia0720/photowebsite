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

# 存储所有故事
stories = []

@app.route('/story', methods=['GET', 'POST'])
def story():
    global stories
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        stories.append({'title': title, 'content': content, 'image_url': image_url})
        return redirect(url_for('story'))

    return render_template('story.html', stories=stories)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    message = ''
    if request.method == 'POST':
        folder = request.form['folder']
        image = request.files['image']
        try:
            cloudinary.uploader.upload(image, folder=f'albums/{folder}')
            message = '上传成功！'
        except Exception as e:
            message = f'上传失败: {str(e)}'
    return render_template('upload.html', message=message)

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








