from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

# from sqlalchemy import Column, Integer, String
from app import db

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
    admin = db.Column(db.Bool, default=False)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = bcrypt.hashpw(password, bcrypt.gensalt())

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

class Transaction(Base):
    __tablename__ = 'Transactions'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.datetime.datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    description = db.Column(db.Text(length=200), nullable=True)

    def __init__(self, description):
        self.description = description


# Create tables.
Base.metadata.create_all(bind=engine)
