from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    # Passes in a user id to this function and the function queries
    #  the database and gets a user's id as a response

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255), index = True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_hash = db.Column(db.String(255))
    blogpost = db.relationship('Blogpost', backref='user', lazy="dynamic")
    comments = db.relationship("Comment", backref="user", lazy="dynamic")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    is_admin = db.column(db.Boolean)

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)



class Blogpost(db.Model):

    __tablename__ = 'blogpost'

    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(300), index=True)
    content = db.Column(db.String(300), index=True)
    category_id = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = db.relationship('Comment', backref='blogpost', lazy="dynamic")

    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_blogpost(self, blogpost):
        ''' Save the blogpost '''
        db.session.add(blogpost)
        db.session.commit()

    # display blogpost
    @classmethod
    def get_blogposts(id):
        blogposts = Blogpost.query.filter_by(category_id = id).all()
        return blogposts

    def __repr__(self):
        return f"Blogpost('{self.id}', '{self.time}')"

class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    post_comment = db.Column(db.String(255), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blogposts = db.Column(db.Integer, db.ForeignKey('blogpost.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        ''' Save the comments '''
        db.session.add(self)
        db.session.commit()

    # display comments

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(blogpost_id=id).all()
        return comments
