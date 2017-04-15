from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/dionysos'

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/
db = SQLAlchemy(app)


class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description
# aber 
    # def __repr__(self):
        # return '<Thing %r>' % self.name

@app.route("/")
def hello():
  #things = Thing.query.all()
  # return render_template('index.html', var='Das ist der erste Test', things=things)
  return render_template('index.html', var='Das ist der erste Test')
  
@app.route('/dist/<path:path>')
def send_path(path):
   return send_from_directory('dist', path)
	
@app.route('/assets/<path:path>')
def send_assets(path):
   return send_from_directory('assets', path)

if __name__ == "__main__":
  app.run(host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', 8080), debug=True)
