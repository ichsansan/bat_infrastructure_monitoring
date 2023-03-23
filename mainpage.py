from flask import Flask, render_template, redirect
from flask import request, session, flash, send_from_directory, jsonify, abort
from process import *
from config import FOLDER_NAME
from flask_session import Session
from datetime import timedelta
import time, os

app = Flask(__name__)
app.secret_key = os.urandom(12)
debug_mode = False
fetch_realtime = True

@app.route("/")
def page_home():
    # return render_template('Login.html')
    if not session.get('logged_in'):
        return render_template('Login.html')
    else:
        if check_session_timeout():
            return redirect('/login')
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

@app.route('/login', methods=['POST'])
def login_proses():
    login = request.form

    userName = login['username']
    passWord = login['password']
    # session['logged_in'] = False

    data = pd.read_csv(r'D:\SML Tech\Monitoring BAT\bat_infrastructure_monitoring\user.csv')   
    df = pd.DataFrame(data, columns=['user', 'password'])

    for i in df.index:
        user, pas = df.iloc[i]
        if user == userName and pas == passWord:
            session['logged_in'] = True
            session['last_active'] = time.time()  # set last_active variable

    return page_home()
    
@app.route('/restart', methods=['POST'])
def edit_new():
    payload = request.json
    # Extract the data from the payload and do something with it
    value1 = payload['data']['value1']
    value2 = payload['data']['value2']

    do_restart_individual_service(value1)

    # restart loading
    # for i in range(5): 
    #     time.sleep(1)
    
    # Return a JSON response
    response = {'message': 'Success', 'datasend':payload}
    return jsonify(response)

    
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()  # clear session data
    # return render_template('Login.html')
    return page_home()


def check_session_timeout():
    if 'logged_in' in session:
        if 'last_active' in session and time.time() - session['last_active'] > 3600: # 3600 detik = 60 menit
            session.pop('logged_in', None)
            flash('Your session has timed out. Please log in again.', 'error')
            return True
    else:
        if not request.path.startswith('/static') and not request.path.startswith('/login'):
            flash('Your session has timed out. Please log in again.', 'error')
            return redirect('/login')
    session['last_active'] = time.time()
    return False

@app.before_request
def before_request():
    if 'last_active' in session:
        now = time.time()
        if now - session['last_active'] > 3600: # 3600 detik = 60 menit
            session.pop('logged_in', None)
            flash('Your session has timed out. Please log in again.', 'error')
            return redirect('/login')
    session['last_active'] = time.time()

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
    Session(app)
    app.run('0.0.0.0', port=5003, debug=debug_mode)