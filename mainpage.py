from flask import Flask, render_template, redirect
from flask import request, send_from_directory
from process import *
from config import FOLDER_NAME
import time, os

app = Flask(__name__)
debug_mode = True
fetch_realtime = True

@app.route("/")
def page_home():
    return render_template('Home.html')

@app.route("/bat-status")
def page_bat_status():
    data = get_bat_status()
    return render_template('BAT Status.html', data = data)

@app.route("/docker-status")
def page_docker_status():
    docker_status = get_docker_status()
    return render_template('Docker Status.html', data = docker_status)

@app.route("/restartservices")
def restartservices():
    data = do_restart_services()
    return render_template("Restartresponse.html", data = data)

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(FOLDER_NAME, filename)
    if os.path.isfile(path):
        return send_from_directory(FOLDER_NAME, filename, as_attachment=True)
    else:
        listfiles = os.listdir(FOLDER_NAME)
        return f"""file {filename} not found. \nFile found: {listfiles}"""

if __name__ == "__main__":
    app.run('0.0.0.0', port=5003, debug=False)