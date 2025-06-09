from flask import Flask, request
import os
import subprocess  # Unused import (Code Style issue)
import requests  # تستخدم نسخة قديمة جداً (SCA)

app = Flask(__name__)

#  (Secret Scanning issue)
SECRET_KEY = "sk_test_1234567890abcdef"

@app.route('/')
def home():
    return "<h1>Welcome to Vulnerable App</h1>"

@app.route('/run', methods=['POST'])
def run_command():
    # ❌ SAST vulnerability - Command Injection محتمل
    cmd = request.form.get('cmd')
    os.system(cmd)
    return f"Executed: {cmd}"

if __name__ == '__main__':
    app.run(debug=True)
