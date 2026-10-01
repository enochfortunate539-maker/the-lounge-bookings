import os
from functools import wraps

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError(
        "Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variable."
    )

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)


# ---------------------------------------------------------
# Authentication
# ---------------------------------------------------------

def get_authenticated_user():
    """Validate the Supabase access token supplied by the browser."""
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()

    if not token:
        return None

    try:
        response = supabase.auth.get_user(token)
        return response.user
    except Exception:
        return None


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = get_authenticated_user()

        if user is None:
            return jsonify({"success": False, "error": "Unauthorized"}), 401

        return view(*args, **kwargs)

    return wrapped


# ---------------------------------------------------------
# Website pages
# ---------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu_page():
    return render_template("menu.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/gallery")
def gallery_page():
    return render_template("gallery.html")


@app.route("/contact")
def contact_page():
    return render_template("contact.html")


@app.route("/privacy")
def privacy_page():
    return render_template("privacy.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


# ---------------------------------------------------------
# Public booking creation
# ---------------------------------------------------------

@app.route("/api/book", methods=["GET", "POST"])
def create_booking():

    if request.method == "GET":
        return jsonify({
            "message": "The booking API endpoint is running!"
        }), 200

    try:
        data = request.get_json(silent=True) or {}

        full_name = str(data.get("fullName", "")).strip()
        email = str(data.get("email", "")).strip()
        phone = str(data.get("phone", "")).strip()
        booking_date = data.get("bookingDate")
        booking_time = data.get("bookingTime")
        special_requests = str(
            data.get("specialRequests", "")
        ).strip()

        if not full_name or not email or not booking_date:
            return jsonify({
                "success": False,
                "error": "Name, email and booking date are required."
            }), 400

        try:
            guests = int(data.get("guests", 1))
        except (TypeError, ValueError):
            return jsonify({
                "success": False,
                "error": "Guests must be a valid number."
            }), 400

        if guests < 1:
            return jsonify({
                "success": False,
                "error": "Guests must be at least 1."
            }), 400

        booking_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "booking_date": booking_date,
            "booking_time": booking_time,
            "guests": guests,
            "special_requests": special_requests,
            "status": "pending"
        }

        response = (
            supabase
            .table("bookings")
            .insert(booking_data)
            .execute()
        )

        return jsonify({
            "success": True,
            "message": "Booking saved successfully!",
            "data": response.data
        }), 201

    except Exception as e:
        app.logger.exception("Booking creation failed")
        return jsonify({
            "success": False,
            "error": "Unable to save booking."
        }), 500


# ---------------------------------------------------------
# Protected admin booking endpoints
# ---------------------------------------------------------

@app.route("/api/bookings", methods=["GET"])
@require_auth
def get_bookings():

    try:
        response = (
            supabase
            .table("bookings")
            .select("*")
            .order("booking_date", desc=False)
            .execute()
        )

        return jsonify(response.data), 200

    except Exception:
        app.logger.exception("Could not fetch bookings")
        return jsonify({
            "success": False,
            "error": "Unable to load bookings."
        }), 500


@app.route("/api/bookings/<booking_id>/status", methods=["PUT"])
@require_auth
def update_booking_status(booking_id):

    data = request.get_json(silent=True) or {}
    new_status = str(data.get("status", "")).lower().strip()

    allowed_statuses = {
        "pending",
        "confirmed",
        "completed",
        "cancelled"
    }

    # Old frontend/database value "rejected" is migrated to "cancelled".
    if new_status == "rejected":
        new_status = "cancelled"

    if new_status not in allowed_statuses:
        return jsonify({
            "success": False,
            "error": "Invalid booking status."
        }), 400

    try:
        response = (
            supabase
            .table("bookings")
            .update({"status": new_status})
            .eq("id", booking_id)
            .execute()
        )

        return jsonify({
            "success": True,
            "message": "Booking status updated successfully.",
            "data": response.data
        }), 200

    except Exception:
        app.logger.exception("Could not update booking status")
        return jsonify({
            "success": False,
            "error": "Unable to update booking status."
        }), 500


# ---------------------------------------------------------
# Admin login
# ---------------------------------------------------------

@app.route("/api/login", methods=["POST"])
def admin_login():

    data = request.get_json(silent=True) or {}

    email = str(data.get("username", "")).strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({
            "success": False,
            "error": "Email and password are required."
        }), 400

    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if not response.session:
            return jsonify({
                "success": False,
                "error": "Invalid login credentials."
            }), 401

        return jsonify({
            "success": True,
            "access_token": response.session.access_token
        }), 200

    except Exception:
        return jsonify({
            "success": False,
            "error": "Invalid login credentials."
        }), 401


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
