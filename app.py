from flask import Flask, render_template
import psutil
import re
import getpass
from datetime import datetime
import pytz
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask app! Go to /htop for system information."

@app.route('/htop', methods=['GET'])

def htop():
    username = getpass.getuser()
    name = "Kota Bharadwaj"

    ist = pytz.timezone('Asia/Kolkata')
    server_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    try:
        top_output = subprocess.check_output(['top', '-n', '1'], universal_newlines=True)
        
        ansi_escape = re.compile(r'\x1b\[([0-9;]*[mGKH])|\x1b\=|\x1b\(B|\x1b\[\?[0-9;]*[hl]')
        top_output_cleaned = ansi_escape.sub('', top_output)

    except subprocess.CalledProcessError as e:
        top_output_cleaned = f"Error executing top command: {str(e)}"
    
    return render_template('htop.html', name=name, username=username, server_time=server_time, top_output=top_output_cleaned)

if __name__ == "__main__":
    app.run(debug=True)