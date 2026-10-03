import os
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "change_this_to_a_very_random_unique_string_78234"

# (Keep your existing app initialization and other routes...)

@app.route('/api/book', methods=['POST'])
def book():
    try:
        # Get the JSON data sent from your frontend form
        data = request.get_json()
        
        # Grab Supabase credentials from environment variables
        supabase_url = "https://eryvwusmaswlqsydifwi.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyeXZ3dXNtYXN3bHFzeWRpZndpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODY3ODMyMDMsImV4cCI6MjEwMjM1OTIwM30.8mlxIRjQLtyPNJtgPb-cKSo6_j2qZEnp7WL952ZLTHM"
        
        # Set up headers for Supabase REST API
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

        payload = {
        "full_name": data.get("fullName") or data.get("name") or data.get("full_name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "guests": data.get("guests") or data.get("guest_count") or data.get("partySize") or 1,
        "booking_date": data.get("bookingDate") or data.get("booking_date"),
        "booking_time": data.get("bookingTime") or data.get("booking_time"),
        "special_requests": data.get("specialRequests") or data.get("special_requests") or ""
    }

        # Forward the booking data to your Supabase 'bookings' table
        supabase_response = requests.post(
        f"{supabase_url}/rest/v1/bookings",
        json=payload,
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


@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # 1. If already logged in, show the admin dashboard
    if session.get('staff_logged_in'):
        return render_template('admin.html')
    
    # 2. If the login form was submitted
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Change these to whatever email and password you want your staff to use
        if email == "staff@thelounge.com" and password == "your_secure_password":
            session['staff_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Invalid email or password, please go back and try again.", 401

    # 3. If not logged in, show the login screen/page
    return render_template('admin.html')



@app.route('/logout')
def logout():
    # Clear the staff login session
    session.pop('staff_logged_in', None)
    return redirect(url_for('admin_panel')) # Sends them back to the admin page, which will now show the login screen again
  


if __name__ == '__main__':
  app.run(debug=True)