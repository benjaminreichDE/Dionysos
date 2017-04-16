from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import *
import pytz
import tzlocal
import bcrypt

# from sqlalchemy import Column, Integer, String

# engine = create_engine('sqlite:///database.db', echo=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                      autoflush=False,
#                                      bind=engine))
Base = declarative_base()
# Base.query = db.query_property()
# Base = db.Model

# Set your classes here.
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(64))  # bcrypt requires 59 or 60 characters
    is_admin = Column(Boolean, default=False)

    def __init__(self, email, name=None, password=None, is_admin=False):
        self.email = email
        self.name = name
        self.password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.is_admin = is_admin

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

    @property
    def transactions(self):
        return Transaction.query.filter_by(user_id=self.id).all()

    def __repr__(self):
        return "<User (name: {0}, email: {1})>".format(self.name, self.email)


class Transaction(Base):
    __tablename__ = 'Transactions'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    description = Column(Text(length=200), nullable=True)

    def __init__(self, amount, user, description):
        self.description = description
        self.user_id = user.id
        self.timestamp = datetime.utcnow()
        self.amount = amount

    @property
    def user(self):
        """Returns the user who created the transaction."""
        return User.query.filter_by(id=self.user_id).first()

    @property
    def time(self):
        to = tzlocal.get_localzone()
        return self.timestamp.replace(tzinfo=pytz.utc).astimezone(to).strftime("%H:%M:%S, %d. %b. %Y")

    def __repr__(self):
        return '<Transaction (id: {0}, user: {1}, time: {2}, description: {3})>'.format(self.id, self.username, self.time, self.description)

