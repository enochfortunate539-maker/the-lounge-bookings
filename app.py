from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Route to serve the admin dashboard
@app.route('/')
@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)