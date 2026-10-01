from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from supabase import create_client, Client
import os 

app = Flask(__name__)
CORS(app)  # Allows your frontend to talk to this backend

# Supabase configuration
SUPABASE_URL = "https://eryvwusmaswlqsydifwi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVyeXZ3dXNtYXN3bHFzeWRpZndpIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4Njc4MzIwMywiZXhwIjoyMTAyMzU5MjAzfQ.MRdrBVbGMxr4akscT2z7g81sLH578NK0AW6SArpZhCQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu_page():
    return render_template('menu.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/gallery')
def gallery_page():
    return render_template('gallery.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/privacy')
def privacy_page():
    return render_template('privacy.html')

# Serve the admin dashboard HTML page
@app.route('/admin')
def admin_page():
    return render_template('admin.html')


@app.route('/api/book', methods=['GET', 'POST'])
def create_booking():
    if request.method == 'GET':
        return jsonify({"message": "The booking API endpoint is running!"}), 200

    try:
        data = request.get_json()
        
        booking_data = {
            "full_name": data.get("fullName"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "booking_date": data.get("bookingDate"),
            "booking_time": data.get("bookingTime"),
            "guests": int(data.get("guests", 1)),
            "special_requests": data.get("specialRequests", "")
        }

        response = supabase.table("bookings").insert(booking_data).execute()

        return jsonify({"success": True, "message": "Booking saved successfully!", "data": response.data}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        # Fetch all bookings from your Supabase table
        response = supabase.table('bookings').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    email = data.get("username")
    password = data.get("password")

    try:
        # Authenticate staff member with Supabase Auth
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # Return the secure access token back to the frontend
        return jsonify({
            "success": True, 
            "access_token": response.session.access_token
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": "Invalid login credentials"}), 401


@app.route('/api/bookings/<booking_id>/status', methods=['PUT'])
def update_booking_status(booking_id):
    data = request.get_json()
    new_status = data.get('status') # e.g., 'confirmed', 'rejected', 'completed'
    
    try:
        # Update the status column in your Supabase 'bookings' table
        response = supabase.table('bookings').update({'status': new_status}).eq('id', booking_id).execute()
        return jsonify({"message": "Booking status updated successfully", "data": response.data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)