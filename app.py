from flask import Flask, render_template, request, send_from_directory, url_for, redirect
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 上傳文件
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/')
def home():
    file_list = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', file_list=file_list)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    # 儲存原始檔名
    original_filename = secure_filename(file.filename)
    # 檔案名稱＝uuid+原始檔案名稱
    filename = str(uuid.uuid4()) + '_' + original_filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # 加入URL到File List
    file_url = url_for('uploaded_file', filename=filename)
    
    # 回到/
    return redirect('/', code=302)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/delete/<filename>', methods=['GET'])
def delete_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        # 删除後回到/
        return redirect('/', code=302)
    else:
        return 'File not found'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
