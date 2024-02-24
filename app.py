from flask import Flask, render_template, session, request, redirect, jsonify, url_for
from flask_cors import CORS
from utils import common_utils
from config.loader import configs


app = Flask(__name__, template_folder='templates/')
CORS(app=app)

# App configs
app.secret_key = '****'
app.config['users_ref'] = configs.users_ref
app.config['gemini_model'] = configs.gemini_model


@app.route('/')
def index():
    if not session.get('login'):
        return redirect(url_for('login', redirectUrl = request.url))
    
    username = session.get('username')
    user_info = common_utils.get_user_info(username=username, users_ref=app.config['users_ref'])

    page_params = {
        'user': user_info,
        'products': [],
        'result_message': f'Gợi ý món ăn hôm nay'
    }

    return render_template('index.html', **page_params)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    redirect_url = request.args.get('redirectUrl', '/')

    if request.method == 'GET':
        return render_template('login.html')
    
    username = request.form['username']
    password = request.form['password']

    result = common_utils.login(username=username, password=password, users_ref=app.config['users_ref'])

    if result['status'] == 1:
        session['login'] = True
        session['username'] = username

        page_params = {
            'message': result['message'],
            'login_status': 1,
            'redirect_url': redirect_url
        }

    else:
        page_params = {
            'message': result['message'],
            'login_status': 0
        }


    return render_template('login.html', **page_params)


@app.route('/log-out')
def log_out():
    redirect_url = request.args.get('redirectUrl', '/')
    session.pop('login', None)
    session.pop('username', None)
    
    return redirect(redirect_url)


@app.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    redirect_url = request.args.get('redirectUrl', '/')

    if request.method == 'GET':
        return render_template('sign_up.html')
    
    form_data = request.form

    result = common_utils.sign_up(form_data=form_data, users_ref=app.config['users_ref'])

    if result['status'] == 1:
        session['login'] = True
        session['username'] = form_data['username']

        page_params = {
            'sign_up_status': 1,
            'message': result['message'],
            'redirect_url': redirect_url
        }

    else:
        page_params = {
            'sign_up_status': 0,
            'message': result['message']
        }

    return render_template('sign_up.html', **page_params)


@app.route('/search', methods = ['GET'])
def search():

    if not session.get('login'):
        return redirect(url_for('login', redirectUrl = request.url))
    
    username = session.get('username')
    user_info = common_utils.get_user_info(username=username, users_ref=app.config['users_ref'])

    query = request.args.get('query', '')

    if query == '':
        return redirect('/')
    

    products = common_utils.search(query=query, health_conditions=user_info['health_conditions'],
                                gemini_model=app.config['gemini_model'])
    

    page_params = {
        'user': user_info,
        'products': products,
        'result_message': f'{query} phù hợp nhất dành cho bạn:'
    }
    

    return render_template('index.html', **page_params)


@app.route('/my-profile')
def view_profile():
    user_info = common_utils.get_user_info(username=session.get('username'), users_ref=app.config['users_ref'])

    page_params = {
        'user': user_info
    }

    return render_template('profile.html', **page_params)