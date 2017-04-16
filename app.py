#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import logging
from logging import Formatter, FileHandler
from forms import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import models

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
models.Base.query = session.query_property()
models.Base.metadata.create_all(engine)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def admin_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'admin' in session and 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need admin privileges to view this page.')
            return redirect(url_for('/'))
'''

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/leaderboard')
def leaderboard():
     data = [{
         "name": "bootstrap-table",
         "amount": "10"
         },  {
         "name": "multiple-select",
         "amount": "288"
         }, {
         "name": "Testing",
         "amount": "340"
        }]
     # for usser models.User.querry.all():
         # data = user.transactions.
     return render_template('pages/leaderboard.html', data = data)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/transactions')
def transactions():
    transactions = models.Transaction.query.order_by(models.Transaction.timestamp.desc())
    return render_template('pages/transactions.html', transactions=transactions)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
