from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import db,login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id =  db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id= db.Column(db.Integer,primary_key=True)
    user_name = db.Column(db.String(64),unique=True,index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)



    @property
    def passoword(self):
        raise AttributeError('password is not a readable attribute')

    @passoword.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return '<USER {}>'.format(self.user_name)

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        token =s.dumps({'confirm':self.id})
        token = token.decode('utf-8')
        return token

    def confirm(self,token):
        s= Serializer(current_app.config['SECRET_KEY'])
        try:
            data =s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)

        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))