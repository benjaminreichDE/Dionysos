from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app
import bcrypt

# from sqlalchemy import Column, Integer, String

db = SQLAlchemy(app)

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64))  # bcrypt requires 59 or 60 characters
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, name=None, password=None, is_admin=False):
        self.email = email
        self.name = name
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())
        self.is_admin = is_admin
        self.id = 0

    @staticmethod
    def verify(username, password):
        """Returns true, if a user with the specified username and password exists.
        If no user exists with the given username or the password was incorrectly entered,
        false is returned.
        
        :argument username: Username, which should be checked.
        :argument password: Password, which should be checked.
        """
        user = User.query.filter_by(username=username).first()
        return bcrypt.checkpw(password, user.password)

    def __repr__(self):
        return "<User (name: {0}, email: {1})>".format(self.name, self.email)


class Transaction(Base):
    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    description = db.Column(db.Text(length=200), nullable=True)

    def __init__(self, user, description):
        self.description = description
        self.user_id = user.id
        self.timestamp = datetime.utcnow()
        self.id = 0

    @property
    def user(self):
        """Returns the user who created the transaction."""
        return User.query.filter_by(id=self.user_id).first()

    @property
    def time(self):
        # TODO
        return "Not yet implemented."

    def __repr__(self):
        return '<Transaction (id: {0}, user: {1}, time: {2}, description: {3})>'.format(self.id, self.username, self.time, self.description)


# Create tables.
Base.metadata.create_all(bind=engine)


# db.create_all()
#
# admin = User("admin@example.com", "Admin", "password", is_admin=True)
# db.session.add(admin)
#
# db.session.commit()
#
# t1 = Transaction(admin, "Hello World")
# t2 = Transaction(admin, "Here come dat boi")
# db.session.add(t1)
# db.session.add(t2)
#
# db.session.commit()
