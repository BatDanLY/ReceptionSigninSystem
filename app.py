# app.py
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# File paths for JSON storage
ALL_USERS_FILE = 'all_users.json'
CURRENTLY_SIGNED_IN_FILE = 'currently_signed_in.json'


# Initialize JSON files if they don't exist
def init_files():
    if not os.path.exists(ALL_USERS_FILE):
        with open(ALL_USERS_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(CURRENTLY_SIGNED_IN_FILE):
        with open(CURRENTLY_SIGNED_IN_FILE, 'w') as f:
            json.dump([], f)


# Load all users
def load_all_users():
    try:
        with open(ALL_USERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


# Save all users
def save_all_users(users):
    with open(ALL_USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


# Load currently signed-in users
def load_currently_signed_in():
    try:
        with open(CURRENTLY_SIGNED_IN_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


# Save currently signed-in users
def save_currently_signed_in(users):
    with open(CURRENTLY_SIGNED_IN_FILE, 'w') as f:
        json.dump(users, f, indent=2)


# Sign in a user
def sign_in_user(name, company, email):
    all_users = load_all_users()
    currently_signed_in = load_currently_signed_in()

    # Check if a user exists in all users, if not add them
    existing_user = next((u for u in all_users if u['email'].lower() == email.lower()), None)
    if not existing_user:
        all_users.append({
            'name': name,
            'company': company,
            'email': email
        })
        save_all_users(all_users)

    # Add to currently sign in with timestamp
    user_signin = {
        'name': name,
        'company': company,
        'email': email,
        'signInTime': datetime.now().isoformat()
    }
    currently_signed_in.append(user_signin)
    save_currently_signed_in(currently_signed_in)

    return user_signin


# Sign out a user
def sign_out_user(identifier):
    currently_signed_in = load_currently_signed_in()

    # Find the user by name or email
    user = next((u for u in currently_signed_in
                 if u['name'].lower() == identifier.lower()
                 or u['email'].lower() == identifier.lower()), None)

    if user:
        currently_signed_in.remove(user)
        save_currently_signed_in(currently_signed_in)
        return user
    return None


# Sign out all users
def sign_out_all_users():
    save_currently_signed_in([])
    print(f"All users signed out at {datetime.now()}")


# Get currently signed-in users
def get_currently_signed_in():
    return load_currently_signed_in()


# Get all users
def get_all_users():
    return load_all_users()



# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/sign_in', methods=['POST'])
def api_sign_in():
    data = request.json
    user = sign_in_user(data['name'], data['company'], data['email'])
    return jsonify({'success': True, 'user': user})


@app.route('/api/sign_out', methods=['POST'])
def api_sign_out():
    data = request.json
    user = sign_out_user(data['identifier'])
    if user:
        return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'error': 'User not found'}), 404


@app.route('/api/get_users', methods=['GET'])
def api_get_users():
    return jsonify({
        'all_users': get_all_users(),
        'currently_signed_in': get_currently_signed_in()
    })


@app.route('/api/autocomplete_signin', methods=['POST'])
def api_autocomplete_signin():
    data = request.json
    name = data.get('name', '').lower()
    company = data.get('company', '').lower()
    email = data.get('email', '').lower()

    # Need at least 3 characters in one field
    if len(name) < 3 and len(company) < 3 and len(email) < 3:
        return jsonify({'suggestion': None})

    all_users = get_all_users()
    matches = []

    for user in all_users:
        name_match = name and name in user['name'].lower()
        company_match = company and company in user['company'].lower()
        email_match = email and email in user['email'].lower()

        if name_match or company_match or email_match:
            matches.append(user)

    # Only return if exactly one match
    if len(matches) == 1:
        return jsonify({'suggestion': matches[0]})
    return jsonify({'suggestion': None})


@app.route('/api/autocomplete_signout', methods=['POST'])
def api_autocomplete_signout():
    data = request.json
    identifier = data.get('identifier', '').lower()

    if len(identifier) < 3:
        return jsonify({'suggestion': None})

    currently_signed_in = get_currently_signed_in()
    matches = []

    for user in currently_signed_in:
        if identifier in user['name'].lower() or identifier in user['email'].lower():
            matches.append(user)

    if len(matches) == 1:
        return jsonify({'suggestion': matches[0]})
    return jsonify({'suggestion': None})


if __name__ == '__main__':
    init_files()

    app.run(debug=True, host='0.0.0.0', port=5000)

