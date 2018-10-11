from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   flash)


from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secret_last.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Connect to Database and create database session
engine = create_engine('sqlite:///catalogitems.db', connect_args={'check_same_thread': False})  # noqa
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret_last.json', scope='')  # noqa
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),  # noqa
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
        login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category and items Information
@app.route('/catalog/JSON')
def CategorysJSON():
    Categorys = session.query(Category).all()
    items = session.query(Item).all()
    return jsonify(Categorys=[r.serialize for r in Categorys], Items=[i.serialize for i in items])  # noqa


# Show all categories in catalog
@app.route('/')
def categoryMenuIndex():
    categories = session.query(Category)
    items = session.query(Item).order_by(desc(Item.created_date)).limit(9)
    if 'username' not in login_session:
        return render_template('publicindex.html', categories=categories, items=items)  # noqa
    else:
        return render_template('index.html', categories=categories, items=items)  # noqa


# Show all items in specific category
@app.route('/catalog/<string:category_name>/items/', methods=['GET', 'POST'])
def categoryitems(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(cat_id=category.id)
    no_items = session.query(Item).filter_by(cat_id=category.id).count()
    return render_template('items.html', category=category, items=items, no_items=no_items)  # noqa


# View the details for one item
@app.route('/catalog/<string:category_name>/<string:item_title>/', methods=['GET', 'POST'])  # noqa
def viewItem(item_title, category_name):
    item = session.query(Item).filter_by(title=item_title).one()
    if 'username' not in login_session or 'user_id' != item.user_id:
        return render_template('publicviewItem.html', item=item)
    else:
        return render_template('viewItem.html', item=item)


# Creat new item
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/')
    categories = session.query(Category)
    if request.method == 'POST':
        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       cat_id=request.form['cat_id'],
                       user_id='user_id')
        session.add(newItem)
        session.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.title))
        return redirect(url_for('categoryMenuIndex'))
    else:
        return render_template('newItem.html', categories=categories)


# Edit an item
@app.route('/catalog/<string:item_title>/edit/', methods=['GET', 'POST'])
def editItem(item_title):
    editedItem = session.query(Item).filter_by(title=item_title).one()
    if 'username' not in login_session or 'user_id' != editedItem.user_id:
        return redirect('/')
    category = session.query(Category).filter_by(id=editedItem.cat_id).one()
    categories = session.query(Category)
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['cat_id']:
            editedItem.cat_id = request.form['cat_id']
        session.add(editedItem)
        session.commit()
        flash("Menu item has been edited!")
        return redirect(url_for('categoryMenuIndex'))
    else:
        return render_template('editItem.html', category=category, item=editedItem, categories=categories)  # noqa


# Delete an item
@app.route('/catalog/<string:item_title>/delete/', methods=['GET', 'POST'])
def deleteItem(item_title):
    deletedItem = session.query(Item).filter_by(title=item_title).one()
    if 'username' not in login_session or 'user_id' != deletedItem.user_id:
        return redirect('/')
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("Item has been deleted!")
        return redirect(url_for('categoryMenuIndex'))
    else:
        return render_template('deleteItem.html', item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
