from flask import Flask, render_template, redirect
from flask import request, session, flash, send_from_directory, jsonify, abort
from process import *
from config import FOLDER_NAME
from datetime import datetime
import time, os

app = Flask(__name__)
app.secret_key = os.urandom(12)
debug_mode = False
fetch_realtime = True
app.config['UPLOAD_FOLDER'] = 'dst/files'

@app.route("/")
def page_home():
    # return render_template('Login.html')
    if not session.get('logged_in'):
        return render_template('Login.html')
    else:
        return render_template('Home.html')

@app.route("/bat-status")
def page_bat_status():
    if session.get('logged_in'):
        data = get_bat_status()
        return render_template('BAT Status.html', data = data)
    else:
        return page_home()

@app.route("/docker-status")
def page_docker_status():
    if session.get('logged_in'):
        docker_status = get_docker_status()
        return render_template('Docker Status.html', data = docker_status)
    else:
        return page_home()

@app.route("/restartservices")
def restartservices():
    if session.get('logged_in'):
        data = do_restart_services()
        return render_template("Restartresponse.html", data = data)
    else:
        return page_home()

@app.route("/download/<filename>")
def download(filename):
    if session.get('logged_in'):
        path = os.path.join(FOLDER_NAME, filename)
        if os.path.isfile(path):
            return send_from_directory(FOLDER_NAME, filename, as_attachment=True)
        else:
            listfiles = os.listdir(FOLDER_NAME)
            return f"""file {filename} not found. \nFile found: {listfiles}"""
    else:
        return page_home()
    
@app.route("/download")
def downloadpage():
    if session.get('logged_in'):
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        file_list = []
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                file_size = round(os.path.getsize(file_path) / 1024, 2)
                file_last_modified = os.path.getmtime(file_path)
                file_last_modified_str = datetime.fromtimestamp(file_last_modified).strftime('%Y-%m-%d %H:%M:%S')
                file_list.append({'name': file, 'size': file_size, 'last_modified': file_last_modified_str})
        return render_template('Download.html', files=file_list)
    else:
        return page_home()

@app.route("/upload", methods=['GET','POST'])
def page_upload():
    if session.get('logged_in'):
        if request.method == 'GET':
            return render_template('Upload.html')
        else:
            alert = {'type':'danger','message':''}
            try:
                if not os.path.isdir(FOLDER_NAME): os.makedirs(FOLDER_NAME)
                filename = request.form['filename']
                if filename == '': filename = time.strftime('%Y-%m-%d %H%M%S')
                
                file = request.files['fileinput']
                fileext = ''
                if '.' not in filename:
                    if '.' in file.filename:
                        fileext = '.' + file.filename.split('.')[-1]
                path = os.path.join(FOLDER_NAME, filename + fileext)
                file.save(path)
                alert['type'] = 'success'
                alert['message'] = f"File <strong>{file.filename}</strong> berhasil disimpan dengan nama <strong>{filename + fileext}</strong> !"
            except Exception as E:
                alert['message'] = str(E)
            return render_template('Upload.html', alert=alert)
    else:
        return page_home()

@app.route('/login', methods=['POST'])
def login_proses():
    login = request.form

    userName = login['username']
    passWord = login['password']
    # session['logged_in'] = False

    # data = pd.read_csv(r'D:\SML Tech\Monitoring BAT\bat_infrastructure_monitoring\user.csv')   
    data = pd.read_csv('user.csv')
    df = pd.DataFrame(data, columns=['user', 'password'])

    for i in df.index:
        user, pas = df.iloc[i]
        if user == userName and pas == passWord:
            session['logged_in'] = True
            session['last_active'] = time.time()  # set last_active variable

    return page_home()
    
@app.route('/restart', methods=['POST'])
def restart_docker():
    payload = request.json
    # Extract the data from the payload and do something with it
    value1 = payload['data']['value1']
    value2 = payload['data']['value2']

    do_restart_individual_service(value1)
    
    # Return a JSON response
    response = {'message': 'Success', 'datasend':payload}
    return jsonify(response)

    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()  # clear session data
    # return render_template('Login.html')
    return page_home()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run('0.0.0.0', port=5003, debug=debug_mode)