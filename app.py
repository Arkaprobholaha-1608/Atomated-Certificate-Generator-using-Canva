from flask import Flask, render_template, request, redirect, url_for, session
import os
import base64
import hashlib
import requests
from cert_gen import generate_templates, rename_certificates
from dotenv import load_dotenv  # Correct import statement

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CERTIFICATES_FOLDER = "certificates"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CERTIFICATES_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CERTIFICATES_FOLDER'] = CERTIFICATES_FOLDER
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')  # Use environment variable for secret key

# Canva API details
CANVA_CLIENT_ID = os.getenv('CANVA_CLIENT_ID', 'default_client_id')  # Use environment variable for client ID
CANVA_CLIENT_SECRET = os.getenv('CANVA_CLIENT_SECRET', 'default_client_secret')  # Use environment variable for client secret
CANVA_REDIRECT_URI = 'http://127.0.0.1:5000/oauth/callback'
CANVA_AUTH_URL = 'https://www.canva.com/api/oauth/authorize'
CANVA_TOKEN_URL = 'https://www.canva.com/api/oauth/token'

# Print environment variables to verify they are loaded correctly
print(f"CANVA_CLIENT_ID: {CANVA_CLIENT_ID}")
print(f"CANVA_CLIENT_SECRET: {CANVA_CLIENT_SECRET}")

def generate_code_challenge():
    """Generate code verifier and code challenge for PKCE."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(64)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/login')
def login():
    """Redirect to Canva login for OAuth."""
    # Generate PKCE code challenge and store code verifier in session
    code_verifier, code_challenge = generate_code_challenge()
    session['code_verifier'] = code_verifier

    # Create the authorization URL
    auth_url = (f"{CANVA_AUTH_URL}?response_type=code&client_id={CANVA_CLIENT_ID}"
                f"&redirect_uri={CANVA_REDIRECT_URI}&code_challenge_method=S256&code_challenge={code_challenge}")
    return redirect(auth_url)

@app.route('/oauth/callback')
def oauth_callback():
    """Handle OAuth callback and exchange code for access token."""
    auth_code = request.args.get('code')
    if not auth_code:
        return "Authorization failed. Please try again."

    code_verifier = session.get('code_verifier')
    if not code_verifier:
        return "Code verifier not found. Restart the login process."

    # Exchange authorization code for access token
    token_response = requests.post(CANVA_TOKEN_URL, data={
        'grant_type': 'authorization_code',
        'client_id': CANVA_CLIENT_ID,
        'client_secret': CANVA_CLIENT_SECRET,  # Include client secret in the token request
        'redirect_uri': CANVA_REDIRECT_URI,
        'code': auth_code,
        'code_verifier': code_verifier,
    })

    token_data = token_response.json()
    session['access_token'] = token_data.get('access_token')

    if 'access_token' not in token_data:
        return f"Failed to obtain access token: {token_data.get('error_description', 'Unknown error')}"

    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and generate templates."""
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], "participants.xlsx")
        file.save(filepath)

        template_url = request.form['template_url']
        access_token = session.get('access_token')
        if not access_token:
            return redirect(url_for('login'))

        generate_templates(filepath, template_url, access_token)
        return redirect(url_for('home'))

@app.route('/rename', methods=['POST'])
def rename_files():
    """Rename certificates based on participant data."""
    confirm = request.form.get('confirm_downloads')
    if confirm == 'on':
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], "participants.xlsx")
        rename_certificates(filepath, app.config['CERTIFICATES_FOLDER'])
        return "Certificates renamed successfully!"
    else:
        return "Please confirm downloads before renaming."

if __name__ == '__main__':
    app.run(debug=True)
