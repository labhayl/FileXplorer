from flask import Flask, render_template, request, send_from_directory
import os
import pandas as pd

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

#Homepage
@app.route('/')
def index():
    return render_template('index.html')

#File Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully!'
    return render_template('upload.html')

#Admin panel login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    uname="abhay"
    pword="Abhay"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == uname and password == pword:
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return render_template('admin.html', files=files)
        else:
            return 'Invalid credentials'
    return render_template('login.html')

#File download
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

#File open
@app.route('/open/<filename>')
def open_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        return 'File format not supported'
    table = df.to_html(index=False)
    return render_template('table.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)