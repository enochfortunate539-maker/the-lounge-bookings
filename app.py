import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# (Keep your existing app initialization and other routes...)

@app.route('/api/book', methods=['POST'])
def book():
    try:
        # Get the JSON data sent from your frontend form
        data = request.get_json()
        
        # Grab Supabase credentials from environment variables
        supabase_url = os.environ.get("https://eryvwusmaswlqsydifwi.supabase.co")
        supabase_key = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyeXZ3dXNtYXN3bHFzeWRpZndpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3ODMyMDMsImV4cCI6MjEwMjM1OTIwM30.8mlxIRjQLtyPNJtgPb-cKSo6_j2qZEnp7WL952ZLTHM")
        
        # Set up headers for Supabase REST API
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        
        # Forward the booking data to your Supabase 'bookings' table
        supabase_response = requests.post(
            f"{supabase_url}/rest/v1/bookings", 
            json=data, 
            headers=headers
        )
        
        # Check if Supabase rejected the insert
        if supabase_response.status_code >= 400:
            return jsonify({"success": False, "error": supabase_response.text}), 400
            
        return jsonify({"success": True, "message": "Booking successfully saved to database!"}), 200
        
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