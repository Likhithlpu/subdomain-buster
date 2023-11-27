# app.py
from flask import Flask, render_template, request
import sys
from dns_enum import perform_dns_enum

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        domain = request.form['domain']
        results = perform_dns_enum(domain)
        return render_template('index.html', domain=domain, results=results, submitted=True)

    return render_template('index.html', domain='', results=[], submitted=False)

if __name__ == "__main__":
    app.run(debug=True)
