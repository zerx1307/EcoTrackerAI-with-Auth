from app import create_app
from flask import url_for

app = create_app()
with app.app_context():
    redirect_uri = url_for('auth.google_callback', _external=True)
    print(f'Redirect URI: {redirect_uri}')
