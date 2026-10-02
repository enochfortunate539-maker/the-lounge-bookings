from flask import Flask, render_template

app = Flask(__name__)



from flask import Flask, request, jsonify

@app.route('/api/book', methods=['POST'])
def book():
    try:
        # Get the JSON data sent from your JavaScript frontend
        data = request.get_json()
        
        # Here you can process the booking data 
        # (e.g., insert it into Supabase from the backend, or save it as needed)
        
        return jsonify({"success": True, "message": "Booking received!"}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



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