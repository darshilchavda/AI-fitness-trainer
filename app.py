import os, json

if not os.path.exists('data'):
    os.makedirs('data')

if not os.path.exists('data/users.json'):
    with open('data/users.json', 'w') as f:
        json.dump({}, f)
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import json, os
from datetime import date
from model.logic import (calculate_bmi, get_workout_plan, chatbot_response,
                         get_diet_plan, get_weekly_planner, get_exercise_library)
#from camera import generate_frames, get_rep_count, reset_rep_count

app = Flask(__name__)
app.secret_key = 'ai_fitness_secret_2024'

DATA_DIR      = 'data'
USERS_FILE    = os.path.join(DATA_DIR, 'users.json')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')

# ── Defaults used when no profile is set ─────────────────────────────────────
DEFAULT_DATA = {
    'age': 22, 'height': 170.0, 'weight': 70.0,
    'goal': 'general', 'bmi': 24.2, 'category': 'Normal',
    'workout_plan': []
}

def load_json(fp, default):
    if not os.path.exists(fp): return default
    with open(fp) as f: return json.load(f)

def save_json(fp, data):
    with open(fp, 'w') as f: json.dump(data, f, indent=2)

def get_data():
    """Return fitness_data from session, or DEFAULT_DATA so pages never crash."""
    return session.get('fitness_data') or DEFAULT_DATA

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user' not in session:
        return render_template('landing.html')
    return render_template('index.html', user=session['user'],
                           has_profile=bool(session.get('fitness_data')))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        u = request.form.get('username','').strip()
        p = request.form.get('password','').strip()
        if not u or not p:
            return render_template('register.html', error='All fields required.')
        users = load_json(USERS_FILE, {})
        if u in users:
            return render_template('register.html', error='Username taken.')
        users[u] = {'password': p}
        save_json(USERS_FILE, users)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('username','').strip()
        p = request.form.get('password','').strip()
        users = load_json(USERS_FILE, {})
        if u in users and users[u]['password'] == p:
            session['user'] = u
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── Profile & Result ──────────────────────────────────────────────────────────
@app.route('/input', methods=['POST'])
def input_form():
    if 'user' not in session: return redirect(url_for('login'))
    age    = int(request.form['age'])
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    goal   = request.form['goal']
    bmi, category = calculate_bmi(weight, height)
    session['fitness_data'] = {
        'age': age, 'height': height, 'weight': weight, 'goal': goal,
        'bmi': round(bmi, 2), 'category': category,
        'workout_plan': get_workout_plan(bmi, goal, age),
    }
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'user' not in session: return redirect(url_for('login'))
    if not session.get('fitness_data'): return redirect(url_for('index'))
    return render_template('result.html', data=session['fitness_data'], user=session['user'])

# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect(url_for('login'))
    prog = load_json(PROGRESS_FILE, {}).get(session['user'], [])
    return render_template('dashboard.html',
        data=get_data(), user=session['user'],
        has_profile=bool(session.get('fitness_data')),
        progress=prog,
        total_reps=sum(e['reps'] for e in prog),
        total_sessions=len(prog),
        best_reps=max((e['reps'] for e in prog), default=0))

# ── Chatbot ───────────────────────────────────────────────────────────────────
@app.route('/chatbot')
def chatbot():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('chatbot.html', user=session['user'])

@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'response': chatbot_response(request.json.get('message',''))})

# ── Camera ────────────────────────────────────────────────────────────────────
#@app.route('/camera')
#def camera_page():
   # if 'user' not in session: return redirect(url_for('login'))
   # return render_template('camera.html', user=session['user'])

#@app.route('/video_feed')
#def video_feed():
    #return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_reps')
def get_reps():
    return jsonify({'reps': get_rep_count()})

@app.route('/reset_reps', methods=['POST'])
def reset_reps():
    reset_rep_count()
    return jsonify({'status': 'ok'})

@app.route('/save_progress', methods=['POST'])
def save_progress():
    if 'user' not in session: return jsonify({'status': 'error'})
    pl    = request.json
    reps  = pl.get('reps', 0)
    ex    = pl.get('exercise', 'Push-up')
    sets  = pl.get('sets', 1)
    today = str(date.today())
    all_p = load_json(PROGRESS_FILE, {})
    user_p = all_p.setdefault(session['user'], [])
    for entry in user_p:
        if entry['date'] == today and entry.get('exercise') == ex:
            entry['reps'] = max(entry['reps'], reps)
            entry['sets'] = sets
            break
    else:
        user_p.append({'date': today, 'reps': reps, 'exercise': ex, 'sets': sets})
    save_json(PROGRESS_FILE, all_p)
    return jsonify({'status': 'saved'})

# ── Diet — works with or without profile ─────────────────────────────────────
@app.route('/diet')
def diet():
    if 'user' not in session: return redirect(url_for('login'))
    data = get_data()
    diet_plan = get_diet_plan(data['goal'], data['bmi'], data['weight'])
    return render_template('diet.html', user=session['user'],
                           data=data, diet=diet_plan,
                           has_profile=bool(session.get('fitness_data')))

# ── Planner — works with or without profile ───────────────────────────────────
@app.route('/planner')
def planner():
    if 'user' not in session: return redirect(url_for('login'))
    data = get_data()
    return render_template('planner.html', user=session['user'],
                           data=data, weekly_plan=get_weekly_planner(data['goal']),
                           has_profile=bool(session.get('fitness_data')))

# ── Exercises — no profile needed ─────────────────────────────────────────────
@app.route('/exercises')
def exercises():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('exercises.html', user=session['user'],
                           library=get_exercise_library())

# ── Timer — no profile needed ─────────────────────────────────────────────────
@app.route('/timer')
def timer():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template('timer.html', user=session['user'])

# ─────────────────────────────────────────────────────────────────────────────
import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
