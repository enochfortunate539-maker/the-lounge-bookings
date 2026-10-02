from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/menu')
def menu():
  return render_template('menu.html')


@app.route('/about')
def about():
  return render_template('about.html')


@app.route('/gallery')
def gallery():
  return render_template('gallery.html')


@app.route('/contact')
def contact():
  return render_template('contact.html')


@app.route('/privacy')
def privacy():
  return render_template('privacy.html')


@app.route('/admin')
def admin_panel():
  return render_template('admin.html')


if __name__ == '__main__':
  app.run(debug=True)