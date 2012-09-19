from app import app

from flask import abort
from flask import g
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask.ext.login import current_user
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import LoginManager

from models import *

import requests
import json

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))

    #if 'assertion' not in request.form:
    #    return redirect()

    assertion = request.form['assertion']
    audience = app.config['PERSONA_AUDIENCE']

    req = requests.post('https://browserid.org/verify',
                        params={'assertion': assertion, 'audience': audience})
    body = json.loads(req.text)
    if body['status'] == 'okay':
        user = User.query.filter_by(email=body['email']).first()
        if user is not None:
            login_user(user)
        else:
            session['register'] = True
            return render_template('register.html', email=body['email'])
    else:
        return 'some error occurred'

    return redirect('/')

@app.route('/register', methods=['POST'])
def register():
    if session.get('register', None) is not True:
        return redirect(url_for('login'))

    username = request.form['username']
    name = request.form['name']
    email = request.form['email']

    new_user = User(email, username, name)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    del session['register']

    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/profile/earned-badges')
def badges(user=None, status=True):
    if user is None:
        user = g.user
    earned_badges = EarnedBadge.query.filter_by(user=user, status=status)
    return render_template('badges.html', badges=earned_badges, status=status)

@app.route('/profile/<username>/earned-badges')
def user_badges(username):
    user = User.query.filter_by(username=username).first()
    return badges(user=user)

@app.route('/profile/earned-badges/pending')
def badges_pending():
    return badges(status=False)

@app.route('/profile/earned-badges/pending/accept', methods=['POST'])
def badges_pending_accept():
    resp = {'status': 'OK'}
    if 'slug' not in request.form:
        resp['status'] = '400'

    eb = EarnedBadge.query.filter_by(slug=request.form['slug']).first()
    eb.status = True
    db.session.commit()
    return json.dumps(resp)

@app.route('/profile/<username>/earned-badges/pending')
def user_badges_bending(username):
    if username != g.user.username:
        abort(400)

    user = User.query.filter_by(username=username).first()
    return badges(user=user, status=False)

@app.route('/profile')
def profile_me():
    return profile('asd')

@app.route('/profile/<username>')
def profile(username):
    return 'profile of %s' % username

@app.route('/people_search')
def people_search(term):
    return 'something'

@app.route('/assertion/<slug>')
def assertion(slug):
    eb = EarnedBadge.query.filter_by(slug=slug).first()
    resp = make_response(json.dumps(eb.create_assertion()))
    resp.headers['Content-Type'] = 'application/json'
    return resp
