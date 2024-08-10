# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .classifier import classify_playlist
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# Mock user database (replace with a real database in production)
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

@main.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('main.login'))
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('main.index'))
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))

@main.route('/classify', methods=['POST'])
def classify():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    playlist_id = request.form['playlist_id']
    try:
        classified_songs = classify_playlist(playlist_id)
        return jsonify(classified_songs)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main.route('/generate', methods=['POST'])
def generate():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    mood = request.form['mood']
    genre = request.form['genre']
    
    # This is where you'd implement the playlist generation logic
    # For now, we'll return a mock result
    new_playlist = [
        {'title': f'New {mood} {genre} Song 1'},
        {'title': f'New {mood} {genre} Song 2'},
        {'title': f'New {mood} {genre} Song 3'},
    ]
    
    return jsonify(new_playlist)